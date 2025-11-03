"""
MongoDB Data Models
Real Estate Listing Database Schema
"""

from datetime import datetime
from typing import List, Optional, Dict, Any

class UserRole:
    VISITOR = "visitor"
    BUYER = "buyer"
    RENTER = "renter"
    LISTER = "lister"
    ADMIN = "admin"

class VerificationStatus:
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    NOT_SUBMITTED = "not_submitted"

class ListingStatus:
    ACTIVE = "active"
    HIDDEN = "hidden"
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    EXPIRED = "expired"

class PropertyType:
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    LAND = "land"
    RENTAL = "rental"


# Collection Schemas (for reference)
COLLECTIONS_SCHEMA = {
    "users": {
        "firebase_uid": "string (unique)",
        "email": "string",
        "name": "string",
        "role": "string (visitor|buyer|renter|lister|admin)",
        "phone": "string (optional)",
        "profile_picture": "string (optional)",
        "verification_status": "string (pending|verified|rejected|not_submitted)",
        "two_factor_enabled": "boolean",
        "is_suspended": "boolean",
        "is_banned": "boolean",
        "created_at": "datetime",
        "updated_at": "datetime"
    },
    
    "properties": {
        "property_id": "string (unique)",
        "title": "string",
        "description": "string",
        "property_type": "string (residential|commercial|land|rental)",
        "current_price": "float",
        "price_history": [
            {
                "price": "float",
                "changed_at": "datetime",
                "reason": "string"
            }
        ],
        "location": {
            "street": "string",
            "city": "string",
            "state": "string",
            "zip_code": "string",
            "country": "string",
            "latitude": "float (optional)",
            "longitude": "float (optional)"
        },
        "bedrooms": "int (optional)",
        "bathrooms": "float (optional)",
        "area_sqft": "float (optional)",
        "year_built": "int (optional)",
        "amenities": ["string"],
        "images": ["string"],
        "documents": ["string"],
        "virtual_tour_url": "string (optional)",
        "created_at": "datetime",
        "updated_at": "datetime"
    },
    
    "listings": {
        "listing_id": "string (unique)",
        "property_id": "string",
        "lister_firebase_uid": "string",
        "status": "string (active|hidden|pending|verified|rejected|expired)",
        "views_count": "int",
        "verified_at": "datetime (optional)",
        "verified_by_admin_uid": "string (optional)",
        "rejection_reason": "string (optional)",
        "expires_at": "datetime (optional)",
        "created_at": "datetime",
        "updated_at": "datetime"
    },
    
    "verification_documents": {
        "document_id": "string (unique)",
        "user_firebase_uid": "string",
        "document_type": "string",
        "document_url": "string",
        "status": "string (pending|verified|rejected)",
        "verified_at": "datetime (optional)",
        "verified_by_admin_uid": "string (optional)",
        "rejection_reason": "string (optional)",
        "created_at": "datetime"
    },
    
    "saved_listings": {
        "saved_id": "string (unique)",
        "user_firebase_uid": "string",
        "listing_id": "string",
        "notes": "string (optional)",
        "saved_at": "datetime"
    },
    
    "property_comparisons": {
        "comparison_id": "string (unique)",
        "user_firebase_uid": "string",
        "property_ids": ["string"],
        "created_at": "datetime"
    },
    
    "reviews": {
        "review_id": "string (unique)",
        "reviewer_firebase_uid": "string",
        "target_type": "string (property|lister)",
        "target_id": "string",
        "rating": "float (1-5)",
        "comment": "string",
        "created_at": "datetime",
        "updated_at": "datetime"
    },
    
    "notifications": {
        "notification_id": "string (unique)",
        "user_firebase_uid": "string (optional, null for broadcast)",
        "title": "string",
        "message": "string",
        "notification_type": "string",
        "is_read": "boolean",
        "created_at": "datetime"
    },
    
    "audit_logs": {
        "log_id": "string (unique)",
        "user_firebase_uid": "string (optional)",
        "action": "string",
        "resource_type": "string (optional)",
        "resource_id": "string (optional)",
        "metadata": "object",
        "timestamp": "datetime"
    }
}
