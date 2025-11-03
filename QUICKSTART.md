# Quick Start Guide - MongoDB Database Implementation

## 🚀 Get Started in 5 Minutes

This guide will help you quickly set up and use the MongoDB Real Estate Database.

---

## Prerequisites

- Python 3.7+
- MongoDB installed (or MongoDB Atlas account)

---

## Installation Steps

### 1. Navigate to MongoDB Directory

```bash
cd mongodb
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Database Connection

Create a `.env` file:

```bash
copy .env.example .env
```

Edit `.env` with your MongoDB connection:

```env
MONGO_URL=mongodb://localhost:27017/
DB_NAME=real_estate_db
```

### 4. Initialize Database

```bash
python init_db.py
```

### 5. (Optional) Load Sample Data

```bash
python sample_data.py
```

---

## Quick Test

Run the examples to see everything in action:

```bash
python examples.py
```

---

## Basic Usage

```python
from operations import DatabaseOperations

# Initialize
db_ops = DatabaseOperations()

# Create a user
user = db_ops.create_user({
    "firebase_uid": "user_001",
    "email": "test@example.com",
    "name": "Test User",
    "role": "buyer",
    "phone": "+1234567890"
})

# Create a property
property = db_ops.create_property({
    "property_id": "prop_001",
    "title": "Beautiful House",
    "description": "Great location",
    "property_type": "residential",
    "current_price": 500000.00,
    "location": {
        "street": "123 Main St",
        "city": "Austin",
        "state": "TX",
        "zip_code": "78701",
        "country": "USA"
    },
    "bedrooms": 3,
    "bathrooms": 2,
    "area_sqft": 2000
})

# Search properties
results = db_ops.search_properties({
    "city": "Austin",
    "min_price": 400000,
    "max_price": 600000
})

# Get statistics
stats = db_ops.get_analytics()
print(f"Total properties: {stats['total_properties']}")
```

---

## What's Included

### 📁 Files

- `config.py` - Database connection setup
- `models.py` - Data schemas and constants
- `operations.py` - All CRUD operations
- `init_db.py` - Database initialization
- `examples.py` - Usage demonstrations
- `sample_data.py` - Sample data loader
- `README.md` - Complete documentation

### 🗄️ Collections

1. users
2. properties
3. listings
4. verification_documents
5. saved_listings
6. property_comparisons
7. reviews
8. messages
9. notifications
10. audit_logs

### ⚡ Features

- ✅ Complete CRUD operations
- ✅ Automatic price history tracking
- ✅ View count tracking
- ✅ Verification workflows
- ✅ Optimized indexes
- ✅ Firebase integration ready

---

## Need Help?

1. Check `README.md` for detailed documentation
2. Run `python examples.py` to see working examples
3. Load sample data with `python sample_data.py`

---

## Next Steps

1. Review the complete README in the mongodb folder
2. Explore the DATABASE_DOCUMENTATION.md for schema details
3. Customize the operations for your specific needs
4. Integrate with your API or application

---

**You're ready to go! 🎉**
