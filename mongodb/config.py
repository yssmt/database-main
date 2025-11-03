"""
MongoDB Configuration Module
Real Estate Listing Database
"""

import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Configuration
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "real_estate_db")

def get_mongo_client():
    """
    Create and return MongoDB client
    
    Returns:
        MongoClient: MongoDB client instance
    """
    try:
        client = MongoClient(MONGO_URL)
        # Test connection
        client.admin.command('ping')
        print(f"✓ Successfully connected to MongoDB at {MONGO_URL}")
        return client
    except ConnectionFailure as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        raise

def get_database():
    """
    Get database instance
    
    Returns:
        Database: MongoDB database instance
    """
    client = get_mongo_client()
    db = client[DB_NAME]
    print(f"✓ Using database: {DB_NAME}")
    return db

def close_connection(client):
    """
    Close MongoDB connection
    
    Args:
        client: MongoDB client instance
    """
    if client:
        client.close()
        print("✓ MongoDB connection closed")
