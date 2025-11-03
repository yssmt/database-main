"""
MongoDB Database Initialization Script
Creates collections and indexes for the Real Estate Listing Database
"""

from config import get_database, close_connection, get_mongo_client
from pymongo import ASCENDING, DESCENDING

def create_indexes(db):
    """
    Create all database indexes for optimized querying
    
    Args:
        db: MongoDB database instance
    """
    print("\n=== Creating Database Indexes ===\n")
    
    # Users Collection Indexes
    print("Creating indexes for 'users' collection...")
    db.users.create_index("firebase_uid", unique=True)
    db.users.create_index("email")
    db.users.create_index("role")
    print("✓ Users indexes created")
    
    # Properties Collection Indexes
    print("Creating indexes for 'properties' collection...")
    db.properties.create_index("property_id", unique=True)
    db.properties.create_index("property_type")
    db.properties.create_index("current_price")
    db.properties.create_index([("location.city", ASCENDING), ("location.state", ASCENDING)])
    print("✓ Properties indexes created")
    
    # Listings Collection Indexes
    print("Creating indexes for 'listings' collection...")
    db.listings.create_index("listing_id", unique=True)
    db.listings.create_index("property_id")
    db.listings.create_index("lister_firebase_uid")
    db.listings.create_index("status")
    print("✓ Listings indexes created")
    
    # Verification Documents Collection Indexes
    print("Creating indexes for 'verification_documents' collection...")
    db.verification_documents.create_index("document_id", unique=True)
    db.verification_documents.create_index("user_firebase_uid")
    db.verification_documents.create_index("status")
    print("✓ Verification documents indexes created")
    
    # Saved Listings Collection Indexes
    print("Creating indexes for 'saved_listings' collection...")
    db.saved_listings.create_index("saved_id", unique=True)
    db.saved_listings.create_index("user_firebase_uid")
    db.saved_listings.create_index([("user_firebase_uid", ASCENDING), ("listing_id", ASCENDING)], unique=True)
    print("✓ Saved listings indexes created")
    
    # Property Comparisons Collection Indexes
    print("Creating indexes for 'property_comparisons' collection...")
    db.property_comparisons.create_index("comparison_id", unique=True)
    db.property_comparisons.create_index("user_firebase_uid")
    print("✓ Property comparisons indexes created")
    
    # Reviews Collection Indexes
    print("Creating indexes for 'reviews' collection...")
    db.reviews.create_index("review_id", unique=True)
    db.reviews.create_index("target_id")
    db.reviews.create_index([("target_type", ASCENDING), ("target_id", ASCENDING)])
    print("✓ Reviews indexes created")
    
    # Notifications Collection Indexes
    print("Creating indexes for 'notifications' collection...")
    db.notifications.create_index("notification_id", unique=True)
    db.notifications.create_index("user_firebase_uid")
    print("✓ Notifications indexes created")
    
    # Audit Logs Collection Indexes
    print("Creating indexes for 'audit_logs' collection...")
    db.audit_logs.create_index("log_id", unique=True)
    db.audit_logs.create_index("user_firebase_uid")
    db.audit_logs.create_index("timestamp")
    db.audit_logs.create_index("action")
    print("✓ Audit logs indexes created")
    
    print("\n=== All indexes created successfully! ===\n")

def list_collections(db):
    """
    List all collections in the database
    
    Args:
        db: MongoDB database instance
    """
    print("\n=== Database Collections ===\n")
    collections = db.list_collection_names()
    if collections:
        for i, collection in enumerate(collections, 1):
            count = db[collection].count_documents({})
            print(f"{i}. {collection} ({count} documents)")
    else:
        print("No collections found")
    print()

def initialize_database():
    """
    Main function to initialize the database
    """
    print("=== MongoDB Database Initialization ===")
    print("Real Estate Listing Database\n")
    
    client = get_mongo_client()
    db = get_database()
    
    # Create indexes
    create_indexes(db)
    
    # List collections
    list_collections(db)
    
    # Close connection
    close_connection(client)
    
    print("✓ Database initialization complete!")

if __name__ == "__main__":
    initialize_database()
