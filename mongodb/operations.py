"""
MongoDB CRUD Operations
Real Estate Listing Database
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from config import get_database

class DatabaseOperations:
    """Class containing all database CRUD operations"""
    
    def __init__(self):
        self.db = get_database()
    
    # ==================== USER OPERATIONS ====================
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        user_data['created_at'] = datetime.utcnow()
        user_data['updated_at'] = datetime.utcnow()
        
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
        update_data['updated_at'] = datetime.utcnow()
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
        property_data['created_at'] = datetime.utcnow()
        property_data['updated_at'] = datetime.utcnow()
        
        # Initialize price history
        if 'price_history' not in property_data:
            property_data['price_history'] = [{
                'price': property_data['current_price'],
                'changed_at': datetime.utcnow(),
                'reason': 'Initial listing'
            }]
        
        result = self.db.properties.insert_one(property_data)
        property_data['_id'] = result.inserted_id
        return property_data
    
    def get_property_by_id(self, property_id: str) -> Optional[Dict[str, Any]]:
        """Get property by ID"""
        return self.db.properties.find_one({"property_id": property_id})
    
    def search_properties(self, filters: Dict[str, Any], limit: int = 100) -> List[Dict[str, Any]]:
        """
        Search properties with filters
        Filters can include: property_type, min_price, max_price, city, bedrooms, etc.
        """
        query = {}
        
        # Property type filter
        if 'property_type' in filters:
            query['property_type'] = filters['property_type']
        
        # Price range filter
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
        
        # Bedrooms/Bathrooms filter
        if 'bedrooms' in filters:
            query['bedrooms'] = filters['bedrooms']
        if 'min_bedrooms' in filters:
            query['bedrooms'] = {"$gte": filters['min_bedrooms']}
        
        return list(self.db.properties.find(query).limit(limit))
    
    def update_property(self, property_id: str, update_data: Dict[str, Any]) -> bool:
        """Update property (handles price history automatically)"""
        update_data['updated_at'] = datetime.utcnow()
        
        # Handle price change - add to price history
        if 'current_price' in update_data:
            property = self.get_property_by_id(property_id)
            if property and property['current_price'] != update_data['current_price']:
                self.db.properties.update_one(
                    {"property_id": property_id},
                    {"$push": {
                        "price_history": {
                            "price": update_data['current_price'],
                            "changed_at": datetime.utcnow(),
                            "reason": update_data.get('price_change_reason', 'Price updated')
                        }
                    }}
                )
        
        result = self.db.properties.update_one(
            {"property_id": property_id},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    def delete_property(self, property_id: str) -> bool:
        """Delete a property"""
        result = self.db.properties.delete_one({"property_id": property_id})
        return result.deleted_count > 0
    
    # ==================== LISTING OPERATIONS ====================
    
    def create_listing(self, listing_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new listing"""
        listing_data['created_at'] = datetime.utcnow()
        listing_data['updated_at'] = datetime.utcnow()
        listing_data.setdefault('status', 'pending')
        listing_data.setdefault('views_count', 0)
        
        result = self.db.listings.insert_one(listing_data)
        listing_data['_id'] = result.inserted_id
        return listing_data
    
    def get_listing_by_id(self, listing_id: str, increment_view: bool = False) -> Optional[Dict[str, Any]]:
        """Get listing by ID (optionally increment view count)"""
        if increment_view:
            self.db.listings.update_one(
                {"listing_id": listing_id},
                {"$inc": {"views_count": 1}}
            )
        return self.db.listings.find_one({"listing_id": listing_id})
    
    def get_listings_by_status(self, status: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get listings by status"""
        return list(self.db.listings.find({"status": status}).limit(limit))
    
    def get_listings_by_lister(self, lister_firebase_uid: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get listings by lister"""
        return list(self.db.listings.find({"lister_firebase_uid": lister_firebase_uid}).limit(limit))
    
    def update_listing(self, listing_id: str, update_data: Dict[str, Any]) -> bool:
        """Update listing"""
        update_data['updated_at'] = datetime.utcnow()
        
        # Set verification time if status is verified
        if update_data.get('status') == 'verified' and 'verified_at' not in update_data:
            update_data['verified_at'] = datetime.utcnow()
        
        result = self.db.listings.update_one(
            {"listing_id": listing_id},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    def delete_listing(self, listing_id: str) -> bool:
        """Delete a listing"""
        result = self.db.listings.delete_one({"listing_id": listing_id})
        return result.deleted_count > 0
    
    # ==================== VERIFICATION DOCUMENT OPERATIONS ====================
    
    def create_verification_document(self, doc_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create verification document"""
        doc_data['created_at'] = datetime.utcnow()
        doc_data.setdefault('status', 'pending')
        
        result = self.db.verification_documents.insert_one(doc_data)
        doc_data['_id'] = result.inserted_id
        return doc_data
    
    def verify_document(self, document_id: str, admin_uid: str, status: str, rejection_reason: str = None) -> bool:
        """Verify or reject a document"""
        update_data = {
            'status': status,
            'verified_by_admin_uid': admin_uid,
            'verified_at': datetime.utcnow()
        }
        
        if rejection_reason:
            update_data['rejection_reason'] = rejection_reason
        
        result = self.db.verification_documents.update_one(
            {"document_id": document_id},
            {"$set": update_data}
        )
        
        # If identity proof is verified, update user status
        if status == 'verified':
            doc = self.db.verification_documents.find_one({"document_id": document_id})
            if doc and doc['document_type'] == 'identity_proof':
                self.db.users.update_one(
                    {"firebase_uid": doc['user_firebase_uid']},
                    {"$set": {"verification_status": "verified"}}
                )
        
        return result.modified_count > 0
    
    def get_pending_verifications(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all pending verification documents"""
        return list(self.db.verification_documents.find({"status": "pending"}).limit(limit))
    
    # ==================== SAVED LISTING OPERATIONS ====================
    
    def save_listing(self, user_firebase_uid: str, listing_id: str, notes: str = None) -> Dict[str, Any]:
        """Save a listing for a user"""
        # Check if already saved
        existing = self.db.saved_listings.find_one({
            "user_firebase_uid": user_firebase_uid,
            "listing_id": listing_id
        })
        
        if existing:
            return existing
        
        saved_data = {
            "saved_id": f"saved_{user_firebase_uid}_{listing_id}_{int(datetime.utcnow().timestamp())}",
            "user_firebase_uid": user_firebase_uid,
            "listing_id": listing_id,
            "notes": notes,
            "saved_at": datetime.utcnow()
        }
        
        result = self.db.saved_listings.insert_one(saved_data)
        saved_data['_id'] = result.inserted_id
        return saved_data
    
    def get_saved_listings(self, user_firebase_uid: str) -> List[Dict[str, Any]]:
        """Get all saved listings for a user"""
        return list(self.db.saved_listings.find({"user_firebase_uid": user_firebase_uid}))
    
    def remove_saved_listing(self, saved_id: str) -> bool:
        """Remove a saved listing"""
        result = self.db.saved_listings.delete_one({"saved_id": saved_id})
        return result.deleted_count > 0
    
    # ==================== NOTIFICATION OPERATIONS ====================
    
    def create_notification(self, notification_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a notification"""
        notification_data['created_at'] = datetime.utcnow()
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
            {"notification_id": notification_id},
            {"$set": {"is_read": True}}
        )
        return result.modified_count > 0
    
    # ==================== AUDIT LOG OPERATIONS ====================
    
    def create_audit_log(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create an audit log entry"""
        log_data['timestamp'] = datetime.utcnow()
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
