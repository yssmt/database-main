# MongoDB Database Schema - Updated

## 📊 Collections Overview

This database contains **9 collections** for the real estate listing platform.

---

## 🗄️ Collections List

### Core Collections

1. **users** - User accounts with Firebase authentication
2. **properties** - Property details with embedded price history
3. **listings** - Property listings lifecycle management
4. **verification_documents** - Document verification for users/properties

### Feature Collections

5. **saved_listings** - User's bookmarked properties
6. **property_comparisons** - Side-by-side property comparisons
7. **reviews** - Property and lister ratings/reviews

### System Collections

8. **notifications** - System notifications and alerts
9. **audit_logs** - Activity tracking and analytics

---

## 📝 Detailed Schema

### 1. users Collection

```javascript
{
  firebase_uid: "firebase_uid_123",          // Unique Firebase ID
  email: "user@example.com",
  name: "John Doe",
  role: "buyer",                             // visitor|buyer|renter|lister|admin
  phone: "+1234567890",                      // Optional
  profile_picture: "https://...",            // Optional
  verification_status: "verified",           // pending|verified|rejected|not_submitted
  two_factor_enabled: false,
  is_suspended: false,
  is_banned: false,
  created_at: ISODate("2025-01-15"),
  updated_at: ISODate("2025-01-15")
}
```

**Indexes:**
- `firebase_uid` (unique)
- `email`
- `role`

---

### 2. properties Collection

```javascript
{
  property_id: "prop_001",
  title: "Beautiful 3BR House",
  description: "Spacious family home...",
  property_type: "residential",              // residential|commercial|land|rental
  current_price: 450000.00,
  
  // Embedded price history array
  price_history: [
    {
      price: 450000.00,
      changed_at: ISODate("2025-01-15"),
      reason: "Initial listing"
    },
    {
      price: 425000.00,
      changed_at: ISODate("2025-02-01"),
      reason: "Price reduced for quick sale"
    }
  ],
  
  // Embedded location
  location: {
    street: "123 Main St",
    city: "Austin",
    state: "TX",
    zip_code: "78701",
    country: "USA",
    latitude: 30.2672,
    longitude: -97.7431
  },
  
  bedrooms: 3,
  bathrooms: 2.5,
  area_sqft: 2200,
  year_built: 2019,
  amenities: ["pool", "garage", "gym"],
  images: ["https://...", "https://..."],
  documents: ["https://..."],
  virtual_tour_url: "https://...",
  created_at: ISODate("2025-01-15"),
  updated_at: ISODate("2025-02-01")
}
```

**Indexes:**
- `property_id` (unique)
- `property_type`
- `current_price`
- `location.city` + `location.state` (compound)

**Note:** Price history is embedded in the property document. When price is updated, new entry is automatically added to price_history array with timestamp and reason.

---

### 3. listings Collection

```javascript
{
  listing_id: "listing_001",
  property_id: "prop_001",                   // References properties
  lister_firebase_uid: "firebase_uid_123",   // References users
  status: "active",                          // active|hidden|pending|verified|rejected|expired
  views_count: 156,                          // Auto-incremented
  verified_at: ISODate("2025-01-20"),
  verified_by_admin_uid: "admin_uid",
  rejection_reason: null,
  expires_at: ISODate("2025-12-31"),
  created_at: ISODate("2025-01-15"),
  updated_at: ISODate("2025-01-20")
}
```

**Indexes:**
- `listing_id` (unique)
- `property_id`
- `lister_firebase_uid`
- `status`

**Features:**
- View count auto-increments on each view
- Status workflow: pending → verified → active

---

### 4. verification_documents Collection

```javascript
{
  document_id: "doc_001",
  user_firebase_uid: "firebase_uid_123",
  document_type: "identity_proof",           // identity_proof|property_ownership|business_license
  document_url: "https://storage.../doc.pdf",
  status: "verified",                        // pending|verified|rejected
  verified_at: ISODate("2025-01-18"),
  verified_by_admin_uid: "admin_uid",
  rejection_reason: null,
  created_at: ISODate("2025-01-15")
}
```

**Indexes:**
- `document_id` (unique)
- `user_firebase_uid`
- `status`

**Features:**
- When identity_proof is verified, user's verification_status auto-updates to "verified"

---

### 5. saved_listings Collection

```javascript
{
  saved_id: "saved_001",
  user_firebase_uid: "firebase_uid_123",
  listing_id: "listing_001",
  notes: "Great location for family",        // Optional personal notes
  saved_at: ISODate("2025-01-20")
}
```

**Indexes:**
- `saved_id` (unique)
- `user_firebase_uid`
- `user_firebase_uid` + `listing_id` (compound, unique) - Prevents duplicate saves

---

### 6. property_comparisons Collection

```javascript
{
  comparison_id: "comp_001",
  user_firebase_uid: "firebase_uid_123",
  property_ids: ["prop_001", "prop_002", "prop_003"],  // Array of property IDs
  created_at: ISODate("2025-01-22")
}
```

**Indexes:**
- `comparison_id` (unique)
- `user_firebase_uid`

**Purpose:**
- Users can save comparison lists for later
- Share comparison links with others
- Track which properties are compared together

---

### 7. reviews Collection

```javascript
{
  review_id: "review_001",
  reviewer_firebase_uid: "firebase_uid_123",
  target_type: "property",                   // property|lister
  target_id: "prop_001",                     // property_id or firebase_uid
  rating: 4.5,                               // 1-5 stars
  comment: "Great property, excellent location!",
  created_at: ISODate("2025-01-25"),
  updated_at: ISODate("2025-01-25")
}
```

**Indexes:**
- `review_id` (unique)
- `target_id`
- `target_type` + `target_id` (compound)

**Use Cases:**
- Review properties after viewing
- Review listers based on experience
- Calculate average ratings

---

### 8. notifications Collection

```javascript
{
  notification_id: "notif_001",
  user_firebase_uid: "firebase_uid_123",     // null for broadcast
  title: "Document Verified",
  message: "Your identity document has been verified!",
  notification_type: "verification",         // system|listing_update|verification|price_drop
  is_read: false,
  created_at: ISODate("2025-01-18")
}
```

**Indexes:**
- `notification_id` (unique)
- `user_firebase_uid`

**Features:**
- Set `user_firebase_uid: null` for broadcast to all users
- Track read/unread status
- Multiple notification types

**Use Cases:**
- Document verification updates
- Listing approval/rejection
- Price drop alerts
- System announcements

---

### 9. audit_logs Collection

```javascript
{
  log_id: "log_001",
  user_firebase_uid: "firebase_uid_123",     // Optional
  action: "property_viewed",                 // user_login|property_viewed|search_performed
  resource_type: "property",                 // property|user|listing
  resource_id: "prop_001",
  metadata: {
    ip_address: "192.168.1.1",
    search_filters: {"city": "Austin"},
    user_agent: "Mozilla/5.0..."
  },
  timestamp: ISODate("2025-01-22T14:30:00Z")
}
```

**Indexes:**
- `log_id` (unique)
- `user_firebase_uid`
- `timestamp`
- `action`

**Common Actions:**
- `user_login`, `user_logout`
- `property_viewed`, `property_created`
- `search_performed`
- `listing_created`, `document_uploaded`

**Use Cases:**
- Security auditing
- User behavior analytics
- Popular properties tracking
- Search pattern analysis

---

## 🔗 Relationships

```
users
  ├─> listings (via lister_firebase_uid)
  │     └─> properties (via property_id)
  ├─> saved_listings (via user_firebase_uid)
  ├─> property_comparisons (via user_firebase_uid)
  ├─> reviews (via reviewer_firebase_uid)
  ├─> notifications (via user_firebase_uid)
  ├─> audit_logs (via user_firebase_uid)
  └─> verification_documents (via user_firebase_uid)
```

---

## ⚡ Key Features

### 1. Automatic Price History
When updating property price, old price is automatically saved to `price_history` array:

```python
db.update_property("prop_001", {
    "current_price": 425000.00,
    "price_change_reason": "Price reduced"
})
# Automatically adds to price_history array
```

### 2. View Tracking
Listing view count auto-increments:

```python
listing = db.get_listing_by_id("listing_001", increment_view=True)
# views_count automatically increases by 1
```

### 3. Verification Workflow
When identity proof is verified, user status auto-updates:

```python
db.verify_document("doc_001", "admin_uid", "verified")
# User's verification_status automatically updates to "verified"
```

---

## 🎯 For Node.js/Express Backend

### Connection Example

```javascript
const { MongoClient } = require('mongodb');

const url = 'mongodb://localhost:27017';
const dbName = 'real_estate_db';

const client = new MongoClient(url);

async function connect() {
  await client.connect();
  const db = client.db(dbName);
  return db;
}
```

### Creating Indexes (Run Once)

```javascript
async function createIndexes(db) {
  // Users
  await db.collection('users').createIndex({ firebase_uid: 1 }, { unique: true });
  await db.collection('users').createIndex({ email: 1 });
  
  // Properties
  await db.collection('properties').createIndex({ property_id: 1 }, { unique: true });
  await db.collection('properties').createIndex({ current_price: 1 });
  await db.collection('properties').createIndex({ 'location.city': 1, 'location.state': 1 });
  
  // Continue for all collections...
}
```

### Example Operations

```javascript
// Create user
async function createUser(db, userData) {
  const users = db.collection('users');
  userData.created_at = new Date();
  userData.updated_at = new Date();
  const result = await users.insertOne(userData);
  return result;
}

// Search properties
async function searchProperties(db, filters) {
  const properties = db.collection('properties');
  const query = {};
  
  if (filters.city) {
    query['location.city'] = new RegExp(filters.city, 'i');
  }
  if (filters.min_price) {
    query.current_price = { $gte: filters.min_price };
  }
  
  return await properties.find(query).limit(100).toArray();
}
```

---

## 📊 Database Statistics

- **Collections:** 9
- **Total Indexes:** ~25
- **Embedded Documents:** location, price_history
- **Reference Fields:** firebase_uid, property_id, listing_id

---

## ✅ What's Removed

- ❌ **messages collection** - In-app messaging removed as requested

---

## 🎓 Next Steps for Your Team

1. **Set up MongoDB** (local or Atlas)
2. **Run initialization** to create indexes
3. **Implement Node.js CRUD** operations based on this schema
4. **Use Python code** as reference for logic
5. **Test with sample data**

---

**Last Updated:** 2025-11-03
**Status:** Ready for Node.js implementation
