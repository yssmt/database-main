# MongoDB Real Estate Listing Database

Complete MongoDB implementation for a Real Estate Listing Platform with Firebase authentication integration.

## 📋 Table of Contents

- [Overview](#overview)
- [Database Schema](#database-schema)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [API Operations](#api-operations)
- [Examples](#examples)
- [Testing](#testing)

---

## 🎯 Overview

This is a comprehensive MongoDB database implementation for a real estate listing platform. It includes:

- **10 Collections**: Users, Properties, Listings, Verification Documents, Saved Listings, Property Comparisons, Reviews, Messages, Notifications, and Audit Logs
- **Complete CRUD Operations**: Full create, read, update, delete functionality for all collections
- **Automatic Features**: Price history tracking, view counting, verification workflows
- **Optimized Performance**: Strategic indexing for fast queries
- **Firebase Integration**: Uses Firebase UIDs for user authentication

---

## 📊 Database Schema

### Collections

1. **users** - User accounts with roles (visitor, buyer, renter, lister, admin)
2. **properties** - Property details with embedded location and price history
3. **listings** - Active/inactive property listings linked to properties and listers
4. **verification_documents** - Document verification for users and properties
5. **saved_listings** - User's saved properties for later reference
6. **property_comparisons** - Side-by-side property comparisons
7. **reviews** - Ratings and reviews for properties and listers
8. **messages** - Internal messaging between users
9. **notifications** - System notifications and broadcasts
10. **audit_logs** - Activity tracking for security and analytics

### Key Relationships

```
users
  ├─> listings (via lister_firebase_uid)
  │     └─> properties (via property_id)
  ├─> saved_listings (via user_firebase_uid)
  ├─> messages (via sender/receiver_firebase_uid)
  └─> verification_documents (via user_firebase_uid)
```

---

## 🚀 Setup Instructions

### Prerequisites

- Python 3.7+
- MongoDB installed locally OR MongoDB Atlas account
- pip (Python package manager)

### Step 1: Install MongoDB

**Option A: Local Installation**
- Download and install MongoDB from [mongodb.com/download](https://www.mongodb.com/try/download/community)
- Start MongoDB service:
  ```bash
  # Windows
  net start MongoDB
  
  # macOS
  brew services start mongodb-community
  
  # Linux
  sudo systemctl start mongod
  ```

**Option B: MongoDB Atlas (Cloud)**
- Create free account at [mongodb.com/atlas](https://www.mongodb.com/cloud/atlas)
- Create a cluster
- Get your connection string

### Step 2: Install Python Dependencies

```bash
cd mongodb
pip install -r requirements.txt
```

### Step 3: Configure Environment

1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` file:
   ```env
   # For local MongoDB
   MONGO_URL=mongodb://localhost:27017/
   DB_NAME=real_estate_db
   
   # OR for MongoDB Atlas
   MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
   DB_NAME=real_estate_db
   ```

### Step 4: Initialize Database

Run the initialization script to create indexes:

```bash
python init_db.py
```

This will:
- Connect to MongoDB
- Create all necessary indexes for optimal performance
- Display collection status

### Step 5: (Optional) Load Sample Data

```bash
python sample_data.py
```

This populates the database with sample users, properties, and listings for testing.

---

## 📖 Usage Guide

### Basic Usage

```python
from operations import DatabaseOperations

# Initialize database operations
db_ops = DatabaseOperations()

# Create a user
user_data = {
    "firebase_uid": "user_12345",
    "email": "john@example.com",
    "name": "John Doe",
    "role": "buyer",
    "phone": "+1234567890"
}
user = db_ops.create_user(user_data)

# Search properties
properties = db_ops.search_properties({
    "city": "Austin",
    "min_price": 300000,
    "max_price": 500000,
    "min_bedrooms": 3
})

# Get analytics
stats = db_ops.get_analytics()
print(f"Total properties: {stats['total_properties']}")
```

---

## 🔧 API Operations

### User Operations

```python
# Create user
user = db_ops.create_user(user_data)

# Get user by Firebase UID
user = db_ops.get_user_by_firebase_uid("firebase_uid_123")

# Get users by role
buyers = db_ops.get_users_by_role("buyer", limit=100)

# Update user
success = db_ops.update_user("firebase_uid_123", {"phone": "+9876543210"})

# Delete user
success = db_ops.delete_user("firebase_uid_123")
```

### Property Operations

```python
# Create property
property_data = {
    "property_id": "prop_001",
    "title": "Beautiful 3BR House",
    "description": "Spacious family home",
    "property_type": "residential",
    "current_price": 450000.00,
    "location": {
        "street": "123 Main St",
        "city": "Austin",
        "state": "TX",
        "zip_code": "78701",
        "country": "USA"
    },
    "bedrooms": 3,
    "bathrooms": 2.5,
    "area_sqft": 2200
}
property = db_ops.create_property(property_data)

# Search properties with filters
results = db_ops.search_properties({
    "city": "Austin",
    "property_type": "residential",
    "min_price": 300000,
    "max_price": 600000,
    "min_bedrooms": 3
})

# Update property (automatically tracks price history)
db_ops.update_property("prop_001", {
    "current_price": 425000.00,
    "price_change_reason": "Price reduced"
})

# Get property
property = db_ops.get_property_by_id("prop_001")

# Delete property
success = db_ops.delete_property("prop_001")
```

### Listing Operations

```python
# Create listing
listing_data = {
    "listing_id": "listing_001",
    "property_id": "prop_001",
    "lister_firebase_uid": "firebase_lister_123"
}
listing = db_ops.create_listing(listing_data)

# Get listing (with view tracking)
listing = db_ops.get_listing_by_id("listing_001", increment_view=True)

# Update listing status
success = db_ops.update_listing("listing_001", {"status": "active"})

# Get listings by status
active_listings = db_ops.get_listings_by_status("active")

# Get listings by lister
my_listings = db_ops.get_listings_by_lister("firebase_lister_123")
```

### Verification Operations

```python
# Create verification document
doc_data = {
    "document_id": "doc_001",
    "user_firebase_uid": "firebase_user_123",
    "document_type": "identity_proof",
    "document_url": "https://storage.example.com/id.pdf"
}
doc = db_ops.create_verification_document(doc_data)

# Get pending verifications (admin)
pending = db_ops.get_pending_verifications()

# Verify document (automatically updates user status if identity_proof)
success = db_ops.verify_document("doc_001", "admin_uid", "verified")

# Reject document
success = db_ops.verify_document("doc_001", "admin_uid", "rejected", 
                                  "Document not clear")
```

### Saved Listings Operations

```python
# Save a listing
saved = db_ops.save_listing("user_uid", "listing_001", 
                             notes="Great house for family!")

# Get user's saved listings
saved_listings = db_ops.get_saved_listings("user_uid")

# Remove saved listing
success = db_ops.remove_saved_listing("saved_001")
```

### Messaging Operations

```python
# Send message
message_data = {
    "message_id": "msg_001",
    "sender_firebase_uid": "buyer_uid",
    "receiver_firebase_uid": "lister_uid",
    "listing_id": "listing_001",
    "subject": "Interested in property",
    "content": "When can I view this property?"
}
msg = db_ops.send_message(message_data)

# Get conversation between two users
conversation = db_ops.get_messages("user1_uid", "user2_uid")

# Get all messages for a user
all_messages = db_ops.get_messages("user_uid")

# Mark message as read
success = db_ops.mark_message_read("msg_001")
```

### Notification Operations

```python
# Create user notification
notification_data = {
    "notification_id": "notif_001",
    "user_firebase_uid": "user_uid",
    "title": "New Message",
    "message": "You have a new message about your listing",
    "notification_type": "message"
}
notif = db_ops.create_notification(notification_data)

# Create broadcast notification (to all users)
broadcast_data = {
    "notification_id": "notif_002",
    "user_firebase_uid": None,  # None = broadcast
    "title": "System Maintenance",
    "message": "Scheduled maintenance tonight at 11 PM",
    "notification_type": "system"
}
notif = db_ops.create_notification(broadcast_data)

# Get notifications for user
notifications = db_ops.get_notifications("user_uid")

# Mark as read
success = db_ops.mark_notification_read("notif_001")
```

### Audit Log Operations

```python
# Create audit log
log_data = {
    "log_id": "log_001",
    "user_firebase_uid": "user_uid",
    "action": "property_viewed",
    "resource_type": "property",
    "resource_id": "prop_001",
    "metadata": {"ip_address": "192.168.1.1"}
}
log = db_ops.create_audit_log(log_data)

# Get audit logs with filters
logs = db_ops.get_audit_logs({
    "user_firebase_uid": "user_uid",
    "action": "search_performed"
}, limit=50)
```

### Analytics Operations

```python
# Get database statistics
stats = db_ops.get_analytics()

# Returns:
# {
#     "total_users": 150,
#     "total_properties": 75,
#     "total_listings": 60,
#     "active_listings": 45,
#     "pending_verifications": 5
# }
```

---

## 💡 Examples

### Complete Workflow Example

Run the examples script to see all operations in action:

```bash
python examples.py
```

This demonstrates:
- Creating users with different roles
- Adding properties with full details
- Creating and managing listings
- Verification workflow
- Saving listings
- Messaging between users
- Database analytics

### Custom Example

```python
from operations import DatabaseOperations
from models import UserRole, PropertyType, ListingStatus

db_ops = DatabaseOperations()

# 1. Create a lister
lister = db_ops.create_user({
    "firebase_uid": "lister_001",
    "email": "agent@realty.com",
    "name": "Real Estate Agent",
    "role": UserRole.LISTER,
    "phone": "+1234567890"
})

# 2. Create a property
property = db_ops.create_property({
    "property_id": "prop_001",
    "title": "Modern Downtown Apartment",
    "description": "Luxury 2BR apartment in prime location",
    "property_type": PropertyType.RESIDENTIAL,
    "current_price": 350000.00,
    "location": {
        "street": "100 Main St",
        "city": "Austin",
        "state": "TX",
        "zip_code": "78701",
        "country": "USA"
    },
    "bedrooms": 2,
    "bathrooms": 2,
    "area_sqft": 1500
})

# 3. Create a listing
listing = db_ops.create_listing({
    "listing_id": "listing_001",
    "property_id": property["property_id"],
    "lister_firebase_uid": lister["firebase_uid"]
})

# 4. Update listing to active
db_ops.update_listing(listing["listing_id"], {
    "status": ListingStatus.ACTIVE
})

# 5. Buyer searches and views
properties = db_ops.search_properties({
    "city": "Austin",
    "max_price": 400000
})

# 6. Track the view
db_ops.get_listing_by_id(listing["listing_id"], increment_view=True)

print(f"Created listing for: {property['title']}")
print(f"Status: {listing['status']}")
```

---

## 🧪 Testing

### Run All Examples

```bash
python examples.py
```

### Load Sample Data

```bash
python sample_data.py
```

### Manual Testing with MongoDB Shell

```bash
# Connect to MongoDB
mongo

# Switch to database
use real_estate_db

# View collections
show collections

# Query examples
db.users.find({role: "buyer"})
db.properties.find({property_type: "residential"})
db.listings.find({status: "active"})

# Check indexes
db.users.getIndexes()
db.properties.getIndexes()
```

---

## 📁 File Structure

```
mongodb/
├── config.py           # MongoDB connection configuration
├── models.py           # Data models and schema definitions
├── operations.py       # CRUD operations for all collections
├── init_db.py          # Database initialization script
├── examples.py         # Usage examples and demonstrations
├── sample_data.py      # Sample data insertion script
├── requirements.txt    # Python dependencies
├── .env.example        # Environment configuration template
└── README.md           # This file
```

---

## 🔑 Key Features

### 1. Automatic Price History Tracking
When you update a property's price, the old price is automatically saved to the price_history array with timestamp and reason.

### 2. View Count Tracking
Every time someone views a listing (with `increment_view=True`), the view count automatically increments.

### 3. Verification Workflow
When an identity_proof document is verified, the user's verification_status automatically updates to "verified".

### 4. Compound Indexes
Strategic compound indexes on frequently-queried fields like (city + state) for fast property searches.

### 5. Broadcast Notifications
Set `user_firebase_uid: None` to send notifications to all users.

### 6. Message Threading
Easily retrieve entire conversations between two users with conversation filtering.

---

## 🛠️ Troubleshooting

### Connection Issues

**Problem**: Cannot connect to MongoDB

**Solution**:
- Verify MongoDB is running: `mongod --version`
- Check connection string in `.env`
- For Atlas, ensure IP address is whitelisted

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'pymongo'`

**Solution**:
```bash
pip install -r requirements.txt
```

### Index Creation Errors

**Problem**: Index already exists with different options

**Solution**:
```python
# Drop existing indexes
db.users.drop_indexes()
# Then rerun init_db.py
python init_db.py
```

---

## 📝 Notes

- All datetime fields are stored in UTC
- Price history is automatically maintained
- Unique indexes prevent duplicate entries
- Compound indexes optimize multi-field queries
- Use Firebase UIDs for authentication integration

---

## 🤝 Contributing

This is a standalone MongoDB implementation that can be:
- Integrated with REST APIs (FastAPI, Flask, etc.)
- Used with GraphQL
- Extended with additional collections
- Modified for different use cases

---

## 📄 License

This database implementation is part of an educational project.

---

## 🆘 Support

For questions or issues:
1. Check the troubleshooting section
2. Review the examples in `examples.py`
3. Examine sample data in `sample_data.py`
4. Refer to MongoDB documentation: [docs.mongodb.com](https://docs.mongodb.com)

---

**Happy Coding! 🚀**
