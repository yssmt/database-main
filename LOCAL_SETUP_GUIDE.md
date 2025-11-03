# 🚀 Local Setup Guide - MongoDB Real Estate Database

Complete step-by-step guide to run this project on your Windows laptop.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Install MongoDB](#install-mongodb)
3. [Install Python](#install-python)
4. [Setup the Project](#setup-the-project)
5. [Run the Database](#run-the-database)
6. [Common Issues & Solutions](#common-issues--solutions)

---

## ✅ Prerequisites

Before starting, you need:
- Windows 10/11
- Administrator access
- Internet connection

---

## 📦 Step 1: Install MongoDB

### Option A: MongoDB Community Edition (Local)

#### 1.1 Download MongoDB

1. Go to: https://www.mongodb.com/try/download/community
2. Select:
   - **Version**: Latest (e.g., 7.0.x)
   - **Platform**: Windows
   - **Package**: MSI
3. Click **Download**

#### 1.2 Install MongoDB

1. Run the downloaded `.msi` file
2. Choose **Complete** installation
3. **Important**: Check "Install MongoDB as a Service"
4. **Important**: Check "Install MongoDB Compass" (GUI tool)
5. Click **Install**
6. Wait for installation to complete

#### 1.3 Verify MongoDB Installation

Open PowerShell and run:

```powershell
mongod --version
```

You should see MongoDB version information.

#### 1.4 Start MongoDB Service

MongoDB should start automatically. If not:

```powershell
# Start MongoDB service
net start MongoDB
```

---

### Option B: MongoDB Atlas (Cloud - Free)

If you prefer cloud database:

1. Go to: https://www.mongodb.com/cloud/atlas/register
2. Sign up for free
3. Create a free cluster (M0)
4. Click "Connect" → "Connect your application"
5. Copy the connection string (we'll use it later)

---

## 🐍 Step 2: Install Python

### 2.1 Download Python

1. Go to: https://www.python.org/downloads/
2. Download **Python 3.11** or **Python 3.12**
3. Run the installer

### 2.2 Install Python

**⚠️ IMPORTANT**: Check these boxes during installation:
- ✅ **"Add Python to PATH"** (very important!)
- ✅ **"Install pip"**

Then click **Install Now**

### 2.3 Verify Python Installation

Open PowerShell and run:

```powershell
python --version
pip --version
```

You should see version numbers for both.

---

## 🔧 Step 3: Setup the Project

### 3.1 Open PowerShell in Project Directory

1. Open File Explorer
2. Navigate to: `D:\Downloads\database-main\database-main`
3. Hold **Shift** + **Right-click** in the folder
4. Select **"Open PowerShell window here"**

### 3.2 Navigate to MongoDB Folder

```powershell
cd mongodb
```

### 3.3 Install Python Dependencies

```powershell
pip install -r requirements.txt
```

This will install:
- `pymongo` (MongoDB driver)
- `python-dotenv` (environment variables)

### 3.4 Create Configuration File

Create `.env` file from template:

```powershell
Copy-Item .env.example .env
```

### 3.5 Edit Configuration

Open `.env` file in Notepad:

```powershell
notepad .env
```

**For Local MongoDB:**
```env
MONGO_URL=mongodb://localhost:27017/
DB_NAME=real_estate_db
```

**For MongoDB Atlas (Cloud):**
```env
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=real_estate_db
```

Replace `username` and `password` with your Atlas credentials.

**Save and close** the file.

---

## ▶️ Step 4: Run the Database

### 4.1 Initialize Database

This creates all collections and indexes:

```powershell
python init_db.py
```

**Expected Output:**
```
=== MongoDB Database Initialization ===
Real Estate Listing Database

✓ Successfully connected to MongoDB at mongodb://localhost:27017/
✓ Using database: real_estate_db

=== Creating Database Indexes ===

Creating indexes for 'users' collection...
✓ Users indexes created
Creating indexes for 'properties' collection...
✓ Properties indexes created
[... more collections ...]

=== All indexes created successfully! ===

=== Database Collections ===

1. users (0 documents)
2. properties (0 documents)
[... more collections ...]

✓ Database initialization complete!
```

### 4.2 Load Sample Data (Optional)

To test with sample data:

```powershell
python sample_data.py
```

**Expected Output:**
```
============================================================
       POPULATING DATABASE WITH SAMPLE DATA       
============================================================

Inserting sample users...
  ✓ Created user: Alice Johnson
  ✓ Created user: Bob Williams
  [... more users ...]

Inserting sample properties...
  ✓ Created property: Modern 3BR House in Downtown Austin
  [... more properties ...]

============================================================
              DATABASE SUMMARY              
============================================================

  Total Users: 5
  Total Properties: 5
  Total Listings: 5
  Active Listings: 3
  Pending Verifications: 0

============================================================
       SAMPLE DATA LOADED SUCCESSFULLY!       
============================================================
```

### 4.3 Run Examples

See all features in action:

```powershell
python examples.py
```

This will demonstrate:
- Creating users
- Adding properties
- Creating listings
- Verification workflows
- Messaging
- Analytics

---

## 💻 Step 5: Use the Database

### 5.1 Interactive Python Shell

Start Python shell:

```powershell
python
```

Then try this:

```python
from operations import DatabaseOperations

# Initialize database operations
db = DatabaseOperations()

# Create a user
user = db.create_user({
    "firebase_uid": "test_user_001",
    "email": "test@example.com",
    "name": "Test User",
    "role": "buyer",
    "phone": "+1234567890"
})

print(f"Created user: {user['name']}")

# Search properties
properties = db.search_properties({
    "city": "Austin",
    "min_price": 300000
})

print(f"Found {len(properties)} properties")

# Get statistics
stats = db.get_analytics()
print(f"Total users: {stats['total_users']}")
print(f"Total properties: {stats['total_properties']}")

# Exit Python
exit()
```

### 5.2 Create Your Own Script

Create `my_script.py`:

```powershell
notepad my_script.py
```

Add this code:

```python
from operations import DatabaseOperations

db = DatabaseOperations()

# Your database operations here
print("Database is working!")

# Example: Get all users
users = db.get_users_by_role("buyer", limit=10)
print(f"Found {len(users)} buyers")
```

Run it:

```powershell
python my_script.py
```

---

## 🔍 Step 6: View Your Data

### Option 1: MongoDB Compass (GUI)

1. Open **MongoDB Compass** (installed with MongoDB)
2. Connection string: `mongodb://localhost:27017`
3. Click **Connect**
4. You'll see `real_estate_db` database
5. Click on it to explore collections

### Option 2: Mongo Shell

```powershell
# Connect to MongoDB
mongosh

# Switch to your database
use real_estate_db

# View collections
show collections

# Query examples
db.users.find()
db.properties.find({property_type: "residential"})
db.listings.find({status: "active"})

# Count documents
db.users.countDocuments()

# Exit
exit
```

---

## 🛠️ Common Issues & Solutions

### Issue 1: "Python is not recognized"

**Problem**: Python not in PATH

**Solution**:
1. Reinstall Python
2. ✅ Check "Add Python to PATH"
3. Or add manually to System Environment Variables

### Issue 2: "Cannot connect to MongoDB"

**Problem**: MongoDB service not running

**Solution**:
```powershell
# Check if MongoDB is running
Get-Service MongoDB

# Start MongoDB
net start MongoDB
```

### Issue 3: "ModuleNotFoundError: No module named 'pymongo'"

**Problem**: Dependencies not installed

**Solution**:
```powershell
cd mongodb
pip install -r requirements.txt
```

### Issue 4: "Connection refused" or "Connection timeout"

**Problem**: Wrong connection string

**Solution**:
- For local: Use `mongodb://localhost:27017/`
- For Atlas: Check your connection string in Atlas dashboard
- Check firewall settings

### Issue 5: ".env file not found"

**Problem**: Environment file missing

**Solution**:
```powershell
Copy-Item .env.example .env
notepad .env
```

### Issue 6: "Permission denied" when creating indexes

**Problem**: Database permissions

**Solution**:
- For local MongoDB: Run PowerShell as Administrator
- For Atlas: Check user permissions in Atlas dashboard

---

## 📚 Quick Reference Commands

### Navigate to project:
```powershell
cd D:\Downloads\database-main\database-main\mongodb
```

### Initialize database:
```powershell
python init_db.py
```

### Load sample data:
```powershell
python sample_data.py
```

### Run examples:
```powershell
python examples.py
```

### Start Python shell:
```powershell
python
```

### Check MongoDB status:
```powershell
Get-Service MongoDB
```

### Start MongoDB:
```powershell
net start MongoDB
```

### Stop MongoDB:
```powershell
net stop MongoDB
```

---

## 📁 Project Structure (After Cleanup)

```
database-main/
│
├── mongodb/                      ⭐ YOUR WORK FOLDER
│   ├── config.py                # Database connection
│   ├── models.py                # Data schemas
│   ├── operations.py            # CRUD operations
│   ├── init_db.py              # Database setup script
│   ├── examples.py             # Usage examples
│   ├── sample_data.py          # Sample data loader
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Config template
│   ├── .env                    # Your config (create this)
│   ├── __init__.py             # Package file
│   └── README.md               # Full documentation
│
├── DATABASE_DOCUMENTATION.md    # Schema documentation
├── DATABASE_QUICK_REFERENCE.md  # Quick reference
├── DATABASE_SCHEMA_VISUAL.md    # Visual diagrams
├── DATABASE_WALKTHROUGH.md      # Walkthrough guide
├── PROJECT_SUMMARY.md           # Project summary
├── QUICKSTART.md               # Quick start
├── LOCAL_SETUP_GUIDE.md        # This file
└── .gitignore                  # Git ignore file
```

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] MongoDB is installed and running
- [ ] Python is installed (python --version works)
- [ ] Dependencies installed (pip list shows pymongo)
- [ ] .env file created and configured
- [ ] Database initialized (python init_db.py works)
- [ ] Sample data loaded (optional)
- [ ] Examples run successfully (python examples.py)
- [ ] Can create users and properties in Python shell

---

## 🎓 Next Steps

1. **Learn the basics**: Read `QUICKSTART.md`
2. **Understand the code**: Read `mongodb/README.md`
3. **Explore examples**: Run `python examples.py`
4. **Try operations**: Use Python shell to test CRUD operations
5. **Build your app**: Start creating your own scripts

---

## 📞 Need Help?

1. Check the error message carefully
2. Review the "Common Issues" section above
3. Read `mongodb/README.md` for detailed documentation
4. Check MongoDB documentation: https://docs.mongodb.com
5. Check PyMongo documentation: https://pymongo.readthedocs.io

---

## 🎉 You're Ready!

Once you've completed all steps and verifications pass, you're ready to start working with your MongoDB database!

**Test it now:**

```powershell
cd mongodb
python examples.py
```

If you see success messages, congratulations! Your database is working perfectly! 🚀

---

**Last Updated**: 2025-11-03
