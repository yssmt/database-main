"""
Sample Data Insertion Script
Populates the Real Estate database with sample data for testing
"""

from operations import DatabaseOperations
from models import UserRole, PropertyType, ListingStatus
import uuid

# def generate_id(prefix): # <-- REMOVED
#     """Generate unique ID"""
#     return f"{prefix}_{uuid.uuid4().hex[:8]}"

def insert_sample_users(db_ops):
    """Insert sample users"""
    print("\nInserting sample users...")
    
    users = [
        # ... (user data is fine, no _id needed)
        {
            "firebase_uid": "firebase_buyer_001",
            "email": "alice@example.com",
            "name": "Alice Johnson",
            "role": UserRole.BUYER,
            "phone": "+1234567890",
            "verification_status": "verified"
        },
        {
            "firebase_uid": "firebase_buyer_002",
            "email": "bob@example.com",
            "name": "Bob Williams",
            "role": UserRole.BUYER,
            "phone": "+1234567891"
        },
        {
            "firebase_uid": "firebase_lister_001",
            "email": "agent1@realty.com",
            "name": "Sarah Agent",
            "role": UserRole.LISTER,
            "phone": "+1234567892",
            "verification_status": "verified"
        },
        {
            "firebase_uid": "firebase_lister_002",
            "email": "agent2@realty.com",
            "name": "Mike Broker",
            "role": UserRole.LISTER,
            "phone": "+1234567893",
            "verification_status": "verified"
        },
        {
            "firebase_uid": "firebase_admin_001",
            "email": "admin@realestate.com",
            "name": "Admin User",
            "role": UserRole.ADMIN,
            "verification_status": "verified"
        }
    ]
    
    for user_data in users:
        try:
            # Check if user already exists
            if not db_ops.get_user_by_firebase_uid(user_data["firebase_uid"]):
                db_ops.create_user(user_data)
                print(f"  ✓ Created user: {user_data['name']}")
            else:
                print(f"  - Skipping user (already exists): {user_data['name']}")
        except Exception as e:
            print(f"  ✗ Failed to create {user_data['name']}: {e}")

def insert_sample_properties(db_ops):
    """Insert sample properties"""
    print("\nInserting sample properties...")
    
    properties = [
        {
            # "property_id": "prop_austin_001", # <-- REMOVED
            "title": "Modern 3BR House in Downtown Austin",
            "description": "Beautiful modern home with open floor plan, granite countertops, and stainless steel appliances. Walking distance to restaurants and shops.",
            "property_type": PropertyType.RESIDENTIAL,
            "current_price": 525000.00,
            "location": {
                "street": "456 Congress Ave",
                "city": "Austin",
                "state": "TX",
                "zip_code": "78701",
                "country": "USA",
                "latitude": 30.2672,  # <-- ADDED
                "longitude": -97.7431 # <-- ADDED
            },
            "bedrooms": 3,
            "bathrooms": 2.5,
            "area_sqft": 2200,
            "year_built": 2019,
            "amenities": ["pool", "garage", "central_ac", "hardwood_floors"]
        },
        {
            # "property_id": "prop_dallas_001", # <-- REMOVED
            "title": "Luxury 4BR Villa with Pool",
            "description": "Stunning luxury villa in prestigious Dallas neighborhood. Features include chef's kitchen, wine cellar, and resort-style pool.",
            "property_type": PropertyType.RESIDENTIAL,
            "current_price": 875000.00,
            "location": {
                "street": "789 Highland Park",
                "city": "Dallas",
                "state": "TX",
                "zip_code": "75205",
                "country": "USA",
                "latitude": 32.7767,  # <-- ADDED
                "longitude": -96.7970 # <-- ADDED
            },
            "bedrooms": 4,
            "bathrooms": 3.5,
            "area_sqft": 3800,
            "year_built": 2020,
            "amenities": ["pool", "garage", "wine_cellar", "smart_home", "security_system"]
        },
        # ... (add lat/lon to other properties as well)
        {
            # "property_id": "prop_houston_001", # <-- REMOVED
            "title": "Cozy 2BR Apartment in Houston",
            "description": "Perfect starter home or investment property. Recently renovated with new appliances and flooring.",
            "property_type": PropertyType.RENTAL,
            "current_price": 1800.00,
            "location": {
                "street": "123 Montrose Blvd",
                "city": "Houston",
                "state": "TX",
                "zip_code": "77006",
                "country": "USA",
                "latitude": 29.7604,  # <-- ADDED
                "longitude": -95.3698 # <-- ADDED
            },
            "bedrooms": 2,
            "bathrooms": 2,
            "area_sqft": 1200,
            "year_built": 2015,
            "amenities": ["parking", "gym", "laundry"]
        },
    ]
    
    # Store created property _ids for listings
    created_property_ids = {}

    for prop_data in properties:
        try:
            # Simple check to avoid duplicates on re-run
            existing = db_ops.db.properties.find_one({"title": prop_data["title"]})
            if not existing:
                created_prop = db_ops.create_property(prop_data)
                print(f"  ✓ Created property: {created_prop['title']}")
                # Store the string _id for use in listings
                created_property_ids[prop_data['title']] = str(created_prop['_id'])
            else:
                print(f"  - Skipping property (already exists): {prop_data['title']}")
                created_property_ids[prop_data['title']] = str(existing['_id'])
        except Exception as e:
            print(f"  ✗ Failed to create {prop_data['title']}: {e}")
            
    return created_property_ids


def insert_sample_listings(db_ops, created_property_ids):
    """Insert sample listings"""
    print("\nInserting sample listings...")
    
    # Need to map old hardcoded IDs to new _ids
    prop_id_map = {
        "prop_austin_001": created_property_ids.get("Modern 3BR House in Downtown Austin"),
        "prop_dallas_001": created_property_ids.get("Luxury 4BR Villa with Pool"),
        "prop_houston_001": created_property_ids.get("Cozy 2BR Apartment in Houston")
    }

    listings = [
        {
            "property_id_key": "prop_austin_001",
            "lister_firebase_uid": "firebase_lister_001",
            "status": ListingStatus.ACTIVE
        },
        {
            "property_id_key": "prop_dallas_001",
            "lister_firebase_uid": "firebase_lister_001",
            "status": ListingStatus.ACTIVE
        },
        {
            "property_id_key": "prop_houston_001",
            "lister_firebase_uid": "firebase_lister_002",
            "status": ListingStatus.ACTIVE
        },
    ]
    
    for listing_data in listings:
        try:
            # Get the new _id
            prop_id = prop_id_map.get(listing_data["property_id_key"])
            if not prop_id:
                print(f"  - Skipping listing, property not found: {listing_data['property_id_key']}")
                continue
                
            listing_data["property_id"] = prop_id
            del listing_data["property_id_key"] # clean up
            
            # Check if listing already exists
            existing = db_ops.db.listings.find_one({
                "property_id": ObjectId(prop_id),
                "lister_firebase_uid": listing_data["lister_firebase_uid"]
            })
            
            if not existing:
                db_ops.create_listing(listing_data)
                print(f"  ✓ Created listing for property: {prop_id}")
            else:
                print(f"  - Skipping listing (already exists) for property: {prop_id}")
        except Exception as e:
            print(f"  ✗ Failed to create listing: {e}")


def insert_sample_reviews(db_ops):
    """Insert sample reviews"""
    print("\nInserting sample reviews...")
    # (Reviews use _id, so this would require fetching properties/listers first)
    print("  (Review insertion skipped - requires fetching live _ids)")

def populate_database():
    """Main function to populate database with sample data"""
    print("="*60)
    print(" POPULATING DATABASE WITH SAMPLE DATA ".center(60))
    print("="*60)
    
    try:
        # db_ops = DatabaseOperations()
        # This will auto-connect via its __init__
        db_ops = DatabaseOperations()
        
        # Insert data
        insert_sample_users(db_ops)
        created_property_ids = insert_sample_properties(db_ops)
        insert_sample_listings(db_ops, created_property_ids)
        insert_sample_reviews(db_ops)
        
        # Show analytics
        print("\n" + "="*60)
        print(" DATABASE SUMMARY ".center(60))
        print("="*60)
        
        analytics = db_ops.get_analytics()
        print(f"\n  Total Users: {analytics['total_users']}")
        print(f"  Total Properties: {analytics['total_properties']}")
        print(f"  Total Listings: {analytics['total_listings']}")
        print(f"  Active Listings: {analytics['active_listings']}")
        print(f"  Pending Verifications: {analytics['pending_verifications']}")
        
        print("\n" + "="*60)
        print(" SAMPLE DATA LOADED SUCCESSFULLY! ".center(60))
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error populating database: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Close the connection
        if 'db_ops' in locals() and db_ops.client:
            db_ops.client.close()
            print("✓ MongoDB connection closed.")


if __name__ == "__main__":
    populate_database()
