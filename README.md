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

The database uses Mongoose to define schemas for the following 10 collections:

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

The Mongoose models for these schemas can be found in the `mongodb/models` directory.

## Database Operations

A comprehensive set of CRUD operations for all collections is available in the `mongodb/operations.js` file. These operations can be used to interact with the database from your application.

## Data Seeding and Examples

-   **`mongodb/seed.js`:** A script to populate the database with sample data.
-   **`mongodb/examples.js`:** A script that demonstrates the usage of the database operations.
