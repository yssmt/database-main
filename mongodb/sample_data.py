"""
Sample Data Insertion Script
Populates the Real Estate database with sample data for testing
"""

from operations import DatabaseOperations
from models import UserRole, PropertyType, ListingStatus
import uuid

def generate_id(prefix):
    """Generate unique ID"""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def insert_sample_users(db_ops):
    """Insert sample users"""
    print("\nInserting sample users...")
    
    users = [
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
            db_ops.create_user(user_data)
            print(f"  ✓ Created user: {user_data['name']}")
        except Exception as e:
            print(f"  ✗ Failed to create {user_data['name']}: {e}")

def insert_sample_properties(db_ops):
    """Insert sample properties"""
    print("\nInserting sample properties...")
    
    properties = [
        {
            "property_id": "prop_austin_001",
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
                "latitude": 30.2672,
                "longitude": -97.7431
            },
            "bedrooms": 3,
            "bathrooms": 2.5,
            "area_sqft": 2200,
            "year_built": 2019,
            "amenities": ["pool", "garage", "central_ac", "hardwood_floors"]
        },
        {
            "property_id": "prop_dallas_001",
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
                "latitude": 32.7767,
                "longitude": -96.7970
            },
            "bedrooms": 4,
            "bathrooms": 3.5,
            "area_sqft": 3800,
            "year_built": 2020,
            "amenities": ["pool", "garage", "wine_cellar", "smart_home", "security_system"]
        },
        {
            "property_id": "prop_houston_001",
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
                "latitude": 29.7604,
                "longitude": -95.3698
            },
            "bedrooms": 2,
            "bathrooms": 2,
            "area_sqft": 1200,
            "year_built": 2015,
            "amenities": ["parking", "gym", "laundry"]
        },
        {
            "property_id": "prop_commercial_001",
            "title": "Prime Retail Space Downtown",
            "description": "Excellent location for retail business. High foot traffic area with ample parking.",
            "property_type": PropertyType.COMMERCIAL,
            "current_price": 3500.00,
            "location": {
                "street": "555 Main Street",
                "city": "Austin",
                "state": "TX",
                "zip_code": "78701",
                "country": "USA"
            },
            "area_sqft": 2500,
            "year_built": 2010,
            "amenities": ["parking", "security", "accessible"]
        },
        {
            "property_id": "prop_land_001",
            "title": "5 Acre Land Plot - Hill Country",
            "description": "Beautiful undeveloped land with hill country views. Perfect for custom home or ranch.",
            "property_type": PropertyType.LAND,
            "current_price": 250000.00,
            "location": {
                "street": "County Road 123",
                "city": "Dripping Springs",
                "state": "TX",
                "zip_code": "78620",
                "country": "USA"
            },
            "area_sqft": 217800,
            "amenities": ["utilities_available", "creek"]
        }
    ]
    
    for prop_data in properties:
        try:
            db_ops.create_property(prop_data)
            print(f"  ✓ Created property: {prop_data['title']}")
        except Exception as e:
            print(f"  ✗ Failed to create {prop_data['title']}: {e}")

def insert_sample_listings(db_ops):
    """Insert sample listings"""
    print("\nInserting sample listings...")
    
    listings = [
        {
            "listing_id": "listing_001",
            "property_id": "prop_austin_001",
            "lister_firebase_uid": "firebase_lister_001",
            "status": ListingStatus.ACTIVE
        },
        {
            "listing_id": "listing_002",
            "property_id": "prop_dallas_001",
            "lister_firebase_uid": "firebase_lister_001",
            "status": ListingStatus.ACTIVE
        },
        {
            "listing_id": "listing_003",
            "property_id": "prop_houston_001",
            "lister_firebase_uid": "firebase_lister_002",
            "status": ListingStatus.ACTIVE
        },
        {
            "listing_id": "listing_004",
            "property_id": "prop_commercial_001",
            "lister_firebase_uid": "firebase_lister_002",
            "status": ListingStatus.PENDING
        },
        {
            "listing_id": "listing_005",
            "property_id": "prop_land_001",
            "lister_firebase_uid": "firebase_lister_001",
            "status": ListingStatus.VERIFIED
        }
    ]
    
    for listing_data in listings:
        try:
            db_ops.create_listing(listing_data)
            print(f"  ✓ Created listing: {listing_data['listing_id']}")
        except Exception as e:
            print(f"  ✗ Failed to create {listing_data['listing_id']}: {e}")


def insert_sample_reviews(db_ops):
    """Insert sample reviews"""
    print("\nInserting sample reviews...")
    
    # Note: Reviews would be added via the reviews collection
    # This is just a placeholder to show the structure
    print("  (Review insertion to be implemented)")

def populate_database():
    """Main function to populate database with sample data"""
    print("="*60)
    print(" POPULATING DATABASE WITH SAMPLE DATA ".center(60))
    print("="*60)
    
    try:
        db_ops = DatabaseOperations()
        
        # Insert data
        insert_sample_users(db_ops)
        insert_sample_properties(db_ops)
        insert_sample_listings(db_ops)
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

if __name__ == "__main__":
    populate_database()
