"""
MongoDB CRUD Operations
Real Estate Listing Database
"""

from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from config import get_database
from bson.objectid import ObjectId  # <-- For converting string IDs to ObjectIds
from pymongo.errors import PyMongoError  # <-- For transaction error handling


class DatabaseOperations:
    """Class containing all database CRUD operations"""

    def __init__(self):
        self.client, self.db = get_database()  # Store client for transactions

    # ==================== USER OPERATIONS ====================

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        user_data['created_at'] = datetime.now(timezone.utc)
        user_data['updated_at'] = datetime.now(timezone.utc)

        # Set defaults
        user_data.setdefault('verification_status', 'not_submitted')
        user_data.setdefault('two_factor_enabled', False)
        user_data.setdefault('is_suspended', False)
        user_data.setdefault('is_banned', False)

        result = self.db.users.insert_one(user_data)
        user_data['_id'] = result.inserted_id
        return user_data

    def get_user_by_firebase_uid(self, firebase_uid: str) -> Optional[Dict[str, Any]]:
        """Get user by Firebase UID"""
        return self.db.users.find_one({"firebase_uid": firebase_uid})

    def get_users_by_role(self, role: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get users by role"""
        return list(self.db.users.find({"role": role}).limit(limit))

    def update_user(self, firebase_uid: str, update_data: Dict[str, Any]) -> bool:
        """Update user information"""
        update_data['updated_at'] = datetime.now(timezone.utc)
        result = self.db.users.update_one(
            {"firebase_uid": firebase_uid},
            {"$set": update_data}
        )
        return result.modified_count > 0

    def delete_user(self, firebase_uid: str) -> bool:
        """Delete a user"""
        result = self.db.users.delete_one({"firebase_uid": firebase_uid})
        return result.deleted_count > 0

    # ==================== PROPERTY OPERATIONS ====================

    def create_property(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new property"""
        property_data['created_at'] = datetime.now(timezone.utc)
        property_data['updated_at'] = datetime.now(timezone.utc)

        # Initialize price history
        if 'price_history' not in property_data and 'current_price' in property_data:
            property_data['price_history'] = [{
                'price': property_data['current_price'],
                'changed_at': datetime.now(timezone.utc),
                'reason': 'Initial listing'
            }]

        # Add GeoJSON field if coordinates exist
        if (
            'location' in property_data
            and 'latitude' in property_data['location']
            and 'longitude' in property_data['location']
        ):
            property_data['location']['geo'] = {
                'type': 'Point',
                'coordinates': [
                    property_data['location']['longitude'],
                    property_data['location']['latitude']
                ]
            }

        result = self.db.properties.insert_one(property_data)
        property_data['_id'] = result.inserted_id
        return property_data

    def get_property_by_id(self, property_id: str) -> Optional[Dict[str, Any]]:
        """Get property by ID"""
        return self.db.properties.find_one({"_id": ObjectId(property_id)})

    def search_properties(self, filters: Dict[str, Any], limit: int = 100) -> List[Dict[str, Any]]:
        """
        Search properties with filters.
        Supports: property_type, price range, city/state, text search, and geospatial.
        """
        query = {}

        # Full-text search
        if 'search_term' in filters:
            query['$text'] = {'$search': filters['search_term']}

        # Geospatial search
        if 'near_lon' in filters and 'near_lat' in filters:
            query['location.geo'] = {
                '$near': {
                    '$geometry': {
                        'type': "Point",
                        'coordinates': [filters['near_lon'], filters['near_lat']]
                    },
                    '$maxDistance': filters.get('max_dist_meters', 10000)
                }
            }

        # Property type
        if 'property_type' in filters:
            query['property_type'] = filters['property_type']

        # Price range
        if 'min_price' in filters or 'max_price' in filters:
            query['current_price'] = {}
            if 'min_price' in filters:
                query['current_price']['$gte'] = filters['min_price']
            if 'max_price' in filters:
                query['current_price']['$lte'] = filters['max_price']

        # Location filters
        if 'city' in filters:
            query['location.city'] = {"$regex": filters['city'], "$options": "i"}
        if 'state' in filters:
            query['location.state'] = {"$regex": filters['state'], "$options": "i"}

        # Bedroom filters
        if 'bedrooms' in filters:
            query['bedrooms'] = filters['bedrooms']
        if 'min_bedrooms' in filters:
            query['bedrooms'] = {"$gte": filters['min_bedrooms']}

        return list(self.db.properties.find(query).limit(limit))

    def update_property(self, property_id: str, update_data: Dict[str, Any]) -> bool:
        """Update property and manage price history"""
        update_data['updated_at'] = datetime.now(timezone.utc)

        # Handle price change
        if 'current_price' in update_data:
            property = self.get_property_by_id(property_id)
            if property and property['current_price'] != update_data['current_price']:
                self.db.properties.update_one(
                    {"_id": ObjectId(property_id)},
                    {"$push": {
                        "price_history": {
                            "price": update_data['current_price'],
                            "changed_at": datetime.now(timezone.utc),
                            "reason": update_data.get('price_change_reason', 'Price updated')
                        }
                    }}
                )

        # Update GeoJSON if location changes
        if (
            'location' in update_data
            and 'latitude' in update_data['location']
            and 'longitude' in update_data['location']
        ):
            update_data['location']['geo'] = {
                'type': 'Point',
                'coordinates': [
                    update_data['location']['longitude'],
                    update_data['location']['latitude']
                ]
            }

        result = self.db.properties.update_one(
            {"_id": ObjectId(property_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    def delete_property(self, property_id: str) -> bool:
        """Delete a property"""
        result = self.db.properties.delete_one({"_id": ObjectId(property_id)})
        return result.deleted_count > 0

    # ==================== LISTING OPERATIONS ====================

    def create_listing(self, listing_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new listing"""
        listing_data['created_at'] = datetime.now(timezone.utc)
        listing_data['updated_at'] = datetime.now(timezone.utc)
        listing_data.setdefault('status', 'pending')
        listing_data.setdefault('views_count', 0)

        if 'property_id' in listing_data and isinstance(listing_data['property_id'], str):
            listing_data['property_id'] = ObjectId(listing_data['property_id'])

        result = self.db.listings.insert_one(listing_data)
        listing_data['_id'] = result.inserted_id
        return listing_data

    def get_listing_by_id(self, listing_id: str, increment_view: bool = False) -> Optional[Dict[str, Any]]:
        """Get listing by ID (optionally increment view count)"""
        if increment_view:
            self.db.listings.update_one(
                {"_id": ObjectId(listing_id)},
                {"$inc": {"views_count": 1}}
            )
        return self.db.listings.find_one({"_id": ObjectId(listing_id)})

    def get_listings_by_status(self, status: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get listings by status"""
        return list(self.db.listings.find({"status": status}).limit(limit))

    def get_listings_by_lister(self, lister_firebase_uid: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get listings by lister"""
        return list(self.db.listings.find({"lister_firebase_uid": lister_firebase_uid}).limit(limit))

    def update_listing(self, listing_id: str, update_data: Dict[str, Any]) -> bool:
        """Update listing"""
        update_data['updated_at'] = datetime.now(timezone.utc)

        if update_data.get('status') == 'verified' and 'verified_at' not in update_data:
            update_data['verified_at'] = datetime.now(timezone.utc)

        result = self.db.listings.update_one(
            {"_id": ObjectId(listing_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    def delete_listing(self, listing_id: str) -> bool:
        """Delete a listing"""
        result = self.db.listings.delete_one({"_id": ObjectId(listing_id)})
        return result.deleted_count > 0

    # ==================== VERIFICATION DOCUMENT OPERATIONS ====================

    def create_verification_document(self, doc_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create verification document"""
        doc_data['created_at'] = datetime.now(timezone.utc)
        doc_data.setdefault('status', 'pending')

        result = self.db.verification_documents.insert_one(doc_data)
        doc_data['_id'] = result.inserted_id
        return doc_data

    def verify_document(self, document_id: str, admin_uid: str, status: str, rejection_reason: str = None) -> bool:
        """Verify or reject a document using transaction-safe logic"""
        try:
            def transaction_callback(session):
                update_data = {
                    'status': status,
                    'verified_by_admin_uid': admin_uid,
                    'verified_at': datetime.now(timezone.utc)
                }
                if rejection_reason:
                    update_data['rejection_reason'] = rejection_reason

                # Update verification document
                result = self.db.verification_documents.update_one(
                    {"_id": ObjectId(document_id)},
                    {"$set": update_data},
                    session=session
                )

                if result.modified_count == 0:
                    raise PyMongoError(f"Document {document_id} not found or not modified.")

                # If identity proof verified, update user verification status
                if status == 'verified':
                    doc = self.db.verification_documents.find_one(
                        {"_id": ObjectId(document_id)},
                        session=session
                    )
                    if doc and doc.get('document_type') == 'identity_proof':
                        user_update_result = self.db.users.update_one(
                            {"firebase_uid": doc['user_firebase_uid']},
                            {"$set": {"verification_status": "verified"}},
                            session=session
                        )
                        if user_update_result.modified_count == 0:
                            print(f"⚠️ User {doc['user_firebase_uid']} may already be verified.")

            with self.client.start_session() as session:
                session.with_transaction(transaction_callback)

            print("✓ Transaction successful: Document and User updated.")
            return True

        except PyMongoError as e:
            print(f"✗ Transaction failed: {e}")
            return False

    def get_pending_verifications(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all pending verification documents"""
        return list(self.db.verification_documents.find({"status": "pending"}).limit(limit))

    # ==================== SAVED LISTING OPERATIONS ====================

    def save_listing(self, user_firebase_uid: str, listing_id: str, notes: str = None) -> Dict[str, Any]:
        """Save a listing for a user"""
        listing_obj_id = ObjectId(listing_id)

        existing = self.db.saved_listings.find_one({
            "user_firebase_uid": user_firebase_uid,
            "listing_id": listing_obj_id
        })

        if existing:
            return existing

        saved_data = {
            "user_firebase_uid": user_firebase_uid,
            "listing_id": listing_obj_id,
            "notes": notes,
            "saved_at": datetime.now(timezone.utc)
        }

        result = self.db.saved_listings.insert_one(saved_data)
        saved_data['_id'] = result.inserted_id
        return saved_data

    def get_saved_listings(self, user_firebase_uid: str) -> List[Dict[str, Any]]:
        """Get all saved listings for a user"""
        return list(self.db.saved_listings.find({"user_firebase_uid": user_firebase_uid}))

    def remove_saved_listing(self, saved_id: str) -> bool:
        """Remove a saved listing"""
        result = self.db.saved_listings.delete_one({"_id": ObjectId(saved_id)})
        return result.deleted_count > 0

    # ==================== NOTIFICATION OPERATIONS ====================

    def create_notification(self, notification_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a notification"""
        notification_data['created_at'] = datetime.now(timezone.utc)
        notification_data.setdefault('is_read', False)

        result = self.db.notifications.insert_one(notification_data)
        notification_data['_id'] = result.inserted_id
        return notification_data

    def get_notifications(self, user_firebase_uid: str) -> List[Dict[str, Any]]:
        """Get notifications for a user (includes broadcasts)"""
        query = {
            "$or": [
                {"user_firebase_uid": user_firebase_uid},
                {"user_firebase_uid": None}
            ]
        }
        return list(self.db.notifications.find(query).sort("created_at", -1))

    def mark_notification_read(self, notification_id: str) -> bool:
        """Mark notification as read"""
        result = self.db.notifications.update_one(
            {"_id": ObjectId(notification_id)},
            {"$set": {"is_read": True}}
        )
        return result.modified_count > 0

    # ==================== AUDIT LOG OPERATIONS ====================

    def create_audit_log(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create an audit log entry"""
        log_data['timestamp'] = datetime.now(timezone.utc)
        log_data.setdefault('metadata', {})

        result = self.db.audit_logs.insert_one(log_data)
        log_data['_id'] = result.inserted_id
        return log_data

    def get_audit_logs(self, filters: Dict[str, Any] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get audit logs with optional filters"""
        query = filters if filters else {}
        return list(self.db.audit_logs.find(query).sort("timestamp", -1).limit(limit))

    # ==================== ANALYTICS OPERATIONS ====================

    def get_analytics(self) -> Dict[str, int]:
        """Get database analytics"""
        return {
            "total_users": self.db.users.count_documents({}),
            "total_properties": self.db.properties.count_documents({}),
            "total_listings": self.db.listings.count_documents({}),
            "active_listings": self.db.listings.count_documents({"status": "active"}),
            "pending_verifications": self.db.verification_documents.count_documents({"status": "pending"})
        }
