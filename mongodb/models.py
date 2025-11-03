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
        "_id": "ObjectId (PK)",
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
        "_id": "ObjectId (PK)",
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
            "geo": {  # For 2dsphere index
                "type": "string ('Point')",
                "coordinates": "[longitude, latitude]"
            }
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
        "_id": "ObjectId (PK)",
        "property_id": "ObjectId", # References properties._id
        "lister_firebase_uid": "string", # References users.firebase_uid
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
        "_id": "ObjectId (PK)",
        "user_firebase_uid": "string", # References users.firebase_uid
        "document_type": "string",
        "document_url": "string",
        "status": "string (pending|verified|rejected)",
        "verified_at": "datetime (optional)",
        "verified_by_admin_uid": "string (optional)",
        "rejection_reason": "string (optional)",
        "created_at": "datetime"
    },
    
    "saved_listings": {
        "_id": "ObjectId (PK)",
        "user_firebase_uid": "string", # References users.firebase_uid
        "listing_id": "ObjectId", # References listings._id
        "notes": "string (optional)",
        "saved_at": "datetime"
    },
    
    "property_comparisons": {
        "_id": "ObjectId (PK)",
        "user_firebase_uid": "string", # References users.firebase_uid
        "property_ids": ["ObjectId"], # References properties._id
        "created_at": "datetime"
    },
    
    "reviews": {
        "_id": "ObjectId (PK)",
        "reviewer_firebase_uid": "string", # References users.firebase_uid
        "target_type": "string (property|lister)",
        "target_id": "string", # Can be ObjectId (property) or string (firebase_uid)
        "rating": "float (1-5)",
        "comment": "string",
        "created_at": "datetime",
        "updated_at": "datetime"
    },
    
    "notifications": {
        "_id": "ObjectId (PK)",
        "user_firebase_uid": "string (optional, null for broadcast)",
        "title": "string",
        "message": "string",
        "notification_type": "string",
        "is_read": "boolean",
        "created_at": "datetime"
    },
    
    "audit_logs": {
        "_id": "ObjectId (PK)",
        "user_firebase_uid": "string (optional)",
        "action": "string",
        "resource_type": "string (optional)",
        "resource_id": "string (optional)",
        "metadata": "object",
        "timestamp": "datetime"
    }
}
