const mongoose = require('mongoose');
const User = require('./models/user');
const Property = require('./models/property');
const Listing = require('./models/listing');
const VerificationDocument = require('./models/verificationDocument');
const SavedListing = require('./models/savedListing');
const PropertyComparison = require('./models/propertyComparison');
const Review = require('./models/review');
const Message = require('./models/message');
const Notification = require('./models/notification');
const AuditLog = require('./models/auditLog');

class DatabaseOperations {
  // ==================== USER OPERATIONS ====================

  async createUser(userData) {
    const user = new User(userData);
    await user.save();
    return user;
  }

  async getUserByFirebaseUid(firebase_uid) {
    return await User.findOne({ firebase_uid });
  }

  async getUsersByRole(role, limit = 100) {
    return await User.find({ role }).limit(limit);
  }

  async updateUser(firebase_uid, update_data) {
    update_data.updated_at = new Date();
    const result = await User.updateOne({ firebase_uid }, { $set: update_data });
    return result.modifiedCount > 0;
  }

  async deleteUser(firebase_uid) {
    const result = await User.deleteOne({ firebase_uid });
    return result.deletedCount > 0;
  }

  // ==================== PROPERTY OPERATIONS ====================

  async createProperty(propertyData) {
    if (propertyData.current_price && !propertyData.price_history) {
      propertyData.price_history = [{
        price: propertyData.current_price,
        reason: 'Initial listing'
      }];
    }
    const property = new Property(propertyData);
    await property.save();
    return property;
  }

  async getPropertyById(property_id) {
    return await Property.findOne({ property_id });
  }

  async searchProperties(filters, limit = 100) {
    const query = {};
    if (filters.search_term) {
      query.$text = { $search: filters.search_term };
    }
    if (filters.near_lon && filters.near_lat) {
      query['location.geo'] = {
        $near: {
          $geometry: {
            type: "Point",
            coordinates: [filters.near_lon, filters.near_lat]
          },
          $maxDistance: filters.max_dist_meters || 10000
        }
      };
    }
    if (filters.property_type) {
      query.property_type = filters.property_type;
    }
    if (filters.min_price || filters.max_price) {
      query.current_price = {};
      if (filters.min_price) {
        query.current_price.$gte = filters.min_price;
      }
      if (filters.max_price) {
        query.current_price.$lte = filters.max_price;
      }
    }
    if (filters.city) {
      query['location.city'] = new RegExp(filters.city, 'i');
    }
    if (filters.state) {
      query['location.state'] = new RegExp(filters.state, 'i');
    }
    if (filters.bedrooms) {
      query.bedrooms = filters.bedrooms;
    }
    if (filters.min_bedrooms) {
      query.bedrooms = { $gte: filters.min_bedrooms };
    }
    return await Property.find(query).limit(limit);
  }

  async updateProperty(property_id, update_data) {
    update_data.updated_at = new Date();
    if (update_data.current_price) {
      const property = await this.getPropertyById(property_id);
      if (property && property.current_price !== update_data.current_price) {
        await Property.updateOne(
          { property_id },
          {
            $push: {
              price_history: {
                price: update_data.current_price,
                reason: update_data.price_change_reason || 'Price updated'
              }
            }
          }
        );
      }
    }
    const result = await Property.updateOne({ property_id }, { $set: update_data });
    return result.modifiedCount > 0;
  }

  async deleteProperty(property_id) {
    const result = await Property.deleteOne({ property_id });
    return result.deletedCount > 0;
  }

  // ==================== LISTING OPERATIONS ====================

  async createListing(listingData) {
    const listing = new Listing(listingData);
    await listing.save();
    return listing;
  }

  async getListingById(listing_id, increment_view = false) {
    if (increment_view) {
      await Listing.updateOne({ listing_id }, { $inc: { views_count: 1 } });
    }
    return await Listing.findOne({ listing_id });
  }

  async getListingsByStatus(status, limit = 100) {
    return await Listing.find({ status }).limit(limit);
  }

  async getListingsByLister(lister_firebase_uid, limit = 100) {
    return await Listing.find({ lister_firebase_uid }).limit(limit);
  }

  async updateListing(listing_id, update_data) {
    update_data.updated_at = new Date();
    if (update_data.status === 'verified' && !update_data.verified_at) {
      update_data.verified_at = new Date();
    }
    const result = await Listing.updateOne({ listing_id }, { $set: update_data });
    return result.modifiedCount > 0;
  }

  async deleteListing(listing_id) {
    const result = await Listing.deleteOne({ listing_id });
    return result.deletedCount > 0;
  }

  // ==================== VERIFICATION DOCUMENT OPERATIONS ====================

  async createVerificationDocument(docData) {
    const doc = new VerificationDocument(docData);
    await doc.save();
    return doc;
  }

  async verifyDocument(document_id, admin_uid, status, rejection_reason = null) {
    const session = await mongoose.startSession();
    session.startTransaction();
    try {
      const update_data = {
        status,
        verified_by_admin_uid: admin_uid,
        verified_at: new Date(),
      };
      if (rejection_reason) {
        update_data.rejection_reason = rejection_reason;
      }
      const docResult = await VerificationDocument.updateOne({ document_id }, { $set: update_data }, { session });
      if (docResult.modifiedCount === 0) {
        throw new Error(`Document ${document_id} not found or not modified.`);
      }

      if (status === 'verified') {
        const doc = await VerificationDocument.findOne({ document_id }).session(session);
        if (doc && doc.document_type === 'identity_proof') {
          await User.updateOne(
            { firebase_uid: doc.user_firebase_uid },
            { $set: { verification_status: 'verified' } },
            { session }
          );
        }
      }

      await session.commitTransaction();
      return true;
    } catch (error) {
      await session.abortTransaction();
      console.error('Transaction failed:', error);
      return false;
    } finally {
      session.endSession();
    }
  }

  async getPendingVerifications(limit = 100) {
    return await VerificationDocument.find({ status: 'pending' }).limit(limit);
  }

  // ==================== SAVED LISTING OPERATIONS ====================

  async saveListing(user_firebase_uid, listing_id, notes = null) {
    const existing = await SavedListing.findOne({ user_firebase_uid, listing_id });
    if (existing) {
      return existing;
    }
    const savedListing = new SavedListing({ user_firebase_uid, listing_id, notes });
    await savedListing.save();
    return savedListing;
  }

  async getSavedListings(user_firebase_uid) {
    return await SavedListing.find({ user_firebase_uid });
  }

  async removeSavedListing(saved_id) {
    const result = await SavedListing.deleteOne({ saved_id });
    return result.deletedCount > 0;
  }

  // ==================== NOTIFICATION OPERATIONS ====================

  async createNotification(notificationData) {
    const notification = new Notification(notificationData);
    await notification.save();
    return notification;
  }

  async getNotifications(user_firebase_uid) {
    const query = {
      $or: [
        { user_firebase_uid },
        { user_firebase_uid: null }
      ]
    };
    return await Notification.find(query).sort({ created_at: -1 });
  }

  async markNotificationRead(notification_id) {
    const result = await Notification.updateOne({ notification_id }, { $set: { is_read: true } });
    return result.modifiedCount > 0;
  }

  // ==================== AUDIT LOG OPERATIONS ====================

  async createAuditLog(logData) {
    const auditLog = new AuditLog(logData);
    await auditLog.save();
    return auditLog;
  }

  async getAuditLogs(filters = {}, limit = 100) {
    return await AuditLog.find(filters).sort({ timestamp: -1 }).limit(limit);
  }

  // ==================== ANALYTICS OPERATIONS ====================

  async getAnalytics() {
    const total_users = await User.countDocuments();
    const total_properties = await Property.countDocuments();
    const total_listings = await Listing.countDocuments();
    const active_listings = await Listing.countDocuments({ status: 'active' });
    const pending_verifications = await VerificationDocument.countDocuments({ status: 'pending' });
    return {
      total_users,
      total_properties,
      total_listings,
      active_listings,
      pending_verifications,
    };
  }
}

module.exports = new DatabaseOperations();
