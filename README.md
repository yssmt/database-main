# MongoDB Real Estate Database

## Overview

This repository contains a complete and production-ready MongoDB database implementation for a real estate listing platform. It's designed to be easily integrated with a MERN stack application, providing a robust backend for user management, property listings, and more.

## Key Features

- **10 Collections with Full CRUD:** Manages users, properties, listings, and more.
- **Automatic Price History:** Tracks all price changes for a property.
- **View Counting:** Automatically increments listing views.
- **Verification Workflow:** Streamlines the user and document verification process.
- **Optimized Indexes:** Ensures fast and efficient queries.
- **Firebase Integration:** Uses Firebase UIDs for authentication.
- **Message Threading:** Manages conversations between users.
- **Broadcast Notifications:** Allows for system-wide announcements.
- **Analytics:** Provides database statistics and metrics.

## Database Schema

The database consists of 10 collections:

1.  **users:** Stores user data and roles.
2.  **properties:** Contains detailed property information.
3.  **listings:** Manages the lifecycle of property listings.
4.  **verification_documents:** Stores documents for user and property verification.
5.  **saved_listings:** Allows users to save their favorite properties.
6.  **property_comparisons:** Enables side-by-side property comparisons.
7.  **reviews:** Manages reviews for properties and listers.
8.  **messages:** Facilitates internal messaging between users.
9.  **notifications:** Handles system notifications and alerts.
10. **audit_logs:** Tracks user activity for security and analytics.

For a detailed breakdown of each collection's schema, please refer to the `DATABASE_DOCUMENTATION.md` file. A visual representation of the schema can be found in `DATABASE_SCHEMA_VISUAL.md`.

## API Reference

The database is designed to be accessed through a REST API. A quick reference of the available endpoints can be found in `DATABASE_QUICK_REFERENCE.md`.

## User Journeys

To understand how the different parts of the database work together, refer to the user journey examples in `DATABASE_WALKTHROUGH.md`. These examples cover common scenarios like user registration, property listing creation, and property searching.
