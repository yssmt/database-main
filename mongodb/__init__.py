"""
MongoDB Real Estate Database Package
Complete database implementation with CRUD operations
"""

from .config import get_database, get_mongo_client, close_connection
from .operations import DatabaseOperations
from .models import (
    UserRole,
    VerificationStatus,
    ListingStatus,
    PropertyType,
    COLLECTIONS_SCHEMA
)

__version__ = "1.0.0"
__author__ = "Real Estate Database Team"

__all__ = [
    'get_database',
    'get_mongo_client',
    'close_connection',
    'DatabaseOperations',
    'UserRole',
    'VerificationStatus',
    'ListingStatus',
    'PropertyType',
    'COLLECTIONS_SCHEMA'
]
