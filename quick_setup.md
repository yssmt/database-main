# Quick Setup Guide

## Prerequisites

- Node.js (v14 or later)
- MongoDB installed locally or a MongoDB Atlas account

## Installation

1.  **Navigate to the `mongodb` directory:**

    ```bash
    cd mongodb
    ```

2.  **Install dependencies:**

    ```bash
    npm install
    ```

3.  **Configure your environment:**

    Create a `.env` file by copying the example:

    ```bash
    cp .env.example .env
    ```

    Update the `.env` file with your MongoDB connection string and database name:

    ```
    MONGO_URL=mongodb://localhost:27017/
    DB_NAME=real_estate_db
    ```

4.  **Initialize the database:**

    ```bash
    node init_db.js
    ```

    This will create all the necessary collections and indexes in your database.

## Running the Examples

To see the database in action, you can run the example script:

```bash
node examples.js
```

This will demonstrate how to perform various CRUD operations using the provided database operations module.
