"""
MongoDB Usage Examples
Demonstrates CRUD operations for Real Estate Listing Database
"""

from operations import DatabaseOperations
from models import UserRole, PropertyType, ListingStatus
import uuid

def generate_id(prefix):
    """Generate unique ID"""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def example_user_operations():
    """Example: User CRUD operations"""
    print("\n" + "="*50)
    print("USER OPERATIONS EXAMPLES")
    print("="*50 + "\n")
    
    db_ops = DatabaseOperations()
    
    # Create a user
    print("1. Creating a new user...")
    user_data = {
        "firebase_uid": generate_id("user"),
        "email": "john.doe@example.com",
        "name": "John Doe",
        "role": UserRole.BUYER,
        "phone": "+1234567890"
    }
    user = db_ops.create_user(user_data)
    print(f"✓ User created: {user['name']} ({user['email']})")
    
    # Get user
    print("\n2. Retrieving user...")
    retrieved_user = db_ops.get_user_by_firebase_uid(user['firebase_uid'])
    print(f"✓ Retrieved: {retrieved_user['name']}")
    
    # Update user
    print("\n3. Updating user...")
    db_ops.update_user(user['firebase_uid'], {"phone": "+9876543210"})
    print("✓ User updated")
    
    # Get users by role
    print("\n4. Getting all buyers...")
    buyers = db_ops.get_users_by_role(UserRole.BUYER)
    print(f"✓ Found {len(buyers)} buyer(s)")
    
    return user['firebase_uid']

def example_property_operations():
    """Example: Property CRUD operations"""
    print("\n" + "="*50)
    print("PROPERTY OPERATIONS EXAMPLES")
    print("="*50 + "\n")
    
    db_ops = DatabaseOperations()
    
    # Create a property
    print("1. Creating a new property...")
    property_data = {
        "property_id": generate_id("prop"),
        "title": "Beautiful 3BR House in Austin",
        "description": "Spacious family home with modern amenities",
        "property_type": PropertyType.RESIDENTIAL,
        "current_price": 450000.00,
        "location": {
            "street": "123 Main Street",
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
        "year_built": 2018,
        "amenities": ["pool", "garage", "garden", "gym"],
        "images": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"]
    }
    property = db_ops.create_property(property_data)
    print(f"✓ Property created: {property['title']}")
    print(f"  Price: ${property['current_price']:,.2f}")
    
    # Search properties
    print("\n2. Searching properties in Austin...")
    results = db_ops.search_properties({
        "city": "Austin",
        "min_price": 300000,
        "max_price": 500000,
        "min_bedrooms": 3
    })
    print(f"✓ Found {len(results)} propert(y/ies)")
    
    # Update property price
    print("\n3. Updating property price...")
    db_ops.update_property(property['property_id'], {
        "current_price": 425000.00,
        "price_change_reason": "Price reduced for quick sale"
    })
    print("✓ Price updated (price history tracked automatically)")
    
    # Get updated property
    updated = db_ops.get_property_by_id(property['property_id'])
    print(f"  New price: ${updated['current_price']:,.2f}")
    print(f"  Price history entries: {len(updated['price_history'])}")
    
    return property['property_id']

def example_listing_operations(property_id, lister_uid):
    """Example: Listing CRUD operations"""
    print("\n" + "="*50)
    print("LISTING OPERATIONS EXAMPLES")
    print("="*50 + "\n")
    
    db_ops = DatabaseOperations()
    
    # Create a listing
    print("1. Creating a listing...")
    listing_data = {
        "listing_id": generate_id("listing"),
        "property_id": property_id,
        "lister_firebase_uid": lister_uid
    }
    listing = db_ops.create_listing(listing_data)
    print(f"✓ Listing created with status: {listing['status']}")
    
    # Get listing (with view increment)
    print("\n2. Viewing listing (increments view count)...")
    viewed = db_ops.get_listing_by_id(listing['listing_id'], increment_view=True)
    print(f"✓ Views: {viewed['views_count']}")
    
    # Update listing status
    print("\n3. Updating listing status to 'active'...")
    db_ops.update_listing(listing['listing_id'], {"status": ListingStatus.ACTIVE})
    print("✓ Listing is now active")
    
    # Get active listings
    print("\n4. Getting all active listings...")
    active_listings = db_ops.get_listings_by_status(ListingStatus.ACTIVE)
    print(f"✓ Found {len(active_listings)} active listing(s)")
    
    return listing['listing_id']

def example_verification_workflow(user_uid):
    """Example: Document verification workflow"""
    print("\n" + "="*50)
    print("VERIFICATION WORKFLOW EXAMPLE")
    print("="*50 + "\n")
    
    db_ops = DatabaseOperations()
    
    # User uploads identity proof
    print("1. User uploading identity proof...")
    doc_data = {
        "document_id": generate_id("doc"),
        "user_firebase_uid": user_uid,
        "document_type": "identity_proof",
        "document_url": "https://storage.example.com/id_proof.pdf"
    }
    doc = db_ops.create_verification_document(doc_data)
    print(f"✓ Document uploaded with status: {doc['status']}")
    
    # Get pending verifications
    print("\n2. Admin checking pending verifications...")
    pending = db_ops.get_pending_verifications()
    print(f"✓ Found {len(pending)} pending document(s)")
    
    # Admin verifies document
    print("\n3. Admin verifying document...")
    admin_uid = "admin_" + uuid.uuid4().hex[:8]
    db_ops.verify_document(doc['document_id'], admin_uid, "verified")
    print("✓ Document verified")
    print("  User verification status automatically updated!")
    
    # Check user status
    user = db_ops.get_user_by_firebase_uid(user_uid)
    print(f"  User verification status: {user['verification_status']}")

def example_saved_listings(user_uid, listing_id):
    """Example: Saved listings operations"""
    print("\n" + "="*50)
    print("SAVED LISTINGS EXAMPLE")
    print("="*50 + "\n")
    
    db_ops = DatabaseOperations()
    
    # Save a listing
    print("1. User saving a listing...")
    saved = db_ops.save_listing(user_uid, listing_id, "Great house for my family!")
    print(f"✓ Listing saved with ID: {saved['saved_id']}")
    
    # Get saved listings
    print("\n2. Getting user's saved listings...")
    saved_listings = db_ops.get_saved_listings(user_uid)
    print(f"✓ User has {len(saved_listings)} saved listing(s)")


def example_analytics():
    """Example: Database analytics"""
    print("\n" + "="*50)
    print("DATABASE ANALYTICS")
    print("="*50 + "\n")
    
    db_ops = DatabaseOperations()
    
    analytics = db_ops.get_analytics()
    
    print("Database Statistics:")
    print(f"  Total Users: {analytics['total_users']}")
    print(f"  Total Properties: {analytics['total_properties']}")
    print(f"  Total Listings: {analytics['total_listings']}")
    print(f"  Active Listings: {analytics['active_listings']}")
    print(f"  Pending Verifications: {analytics['pending_verifications']}")

def run_all_examples():
    """Run all example workflows"""
    print("\n" + "="*70)
    print(" MONGODB REAL ESTATE DATABASE - COMPLETE EXAMPLES ".center(70))
    print("="*70)
    
    try:
        # Create sample user (buyer)
        buyer_uid = example_user_operations()
        
        # Create lister
        print("\n\nCreating a lister user...")
        db_ops = DatabaseOperations()
        lister_data = {
            "firebase_uid": generate_id("lister"),
            "email": "agent@realty.com",
            "name": "Jane Agent",
            "role": UserRole.LISTER,
            "phone": "+1555000000"
        }
        lister = db_ops.create_user(lister_data)
        lister_uid = lister['firebase_uid']
        print(f"✓ Lister created: {lister['name']}")
        
        # Create property and listing
        property_id = example_property_operations()
        listing_id = example_listing_operations(property_id, lister_uid)
        
        # Verification workflow
        example_verification_workflow(lister_uid)
        
        # Saved listings
        example_saved_listings(buyer_uid, listing_id)
        
        # Analytics
        example_analytics()
        
        print("\n" + "="*70)
        print(" ALL EXAMPLES COMPLETED SUCCESSFULLY! ".center(70))
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_examples()
