const { getDatabase, closeConnection } = require('./config');

async function createIndexes(db) {
  console.log('\n=== Creating Database Indexes ===\n');

  console.log("Creating indexes for 'users' collection...");
  await db.collection('users').createIndex({ firebase_uid: 1 }, { unique: true });
  await db.collection('users').createIndex({ email: 1 });
  await db.collection('users').createIndex({ role: 1 });
  console.log('✓ Users indexes created');

  console.log("Creating indexes for 'properties' collection...");
  await db.collection('properties').createIndex({ property_type: 1 });
  await db.collection('properties').createIndex({ current_price: 1 });
  await db.collection('properties').createIndex({ 'location.geo': '2dsphere' });
  await db.collection('properties').createIndex({ title: 'text', description: 'text' });
  console.log('✓ Properties indexes created');

  console.log("Creating indexes for 'listings' collection...");
  await db.collection('listings').createIndex({ property_id: 1 });
  await db.collection('listings').createIndex({ lister_firebase_uid: 1 });
  await db.collection('listings').createIndex({ status: 1 });
  console.log('✓ Listings indexes created');

  console.log("Creating indexes for 'verification_documents' collection...");
  await db.collection('verification_documents').createIndex({ user_firebase_uid: 1 });
  await db.collection('verification_documents').createIndex({ status: 1 });
  console.log('✓ Verification documents indexes created');

  console.log("Creating indexes for 'saved_listings' collection...");
  await db.collection('saved_listings').createIndex({ user_firebase_uid: 1 });
  await db.collection('saved_listings').createIndex({ user_firebase_uid: 1, listing_id: 1 }, { unique: true });
  console.log('✓ Saved listings indexes created');

  console.log("Creating indexes for 'property_comparisons' collection...");
  await db.collection('property_comparisons').createIndex({ user_firebase_uid: 1 });
  console.log('✓ Property comparisons indexes created');

  console.log("Creating indexes for 'reviews' collection...");
  await db.collection('reviews').createIndex({ target_id: 1 });
  await db.collection('reviews').createIndex({ target_type: 1, target_id: 1 });
  console.log('✓ Reviews indexes created');

  console.log("Creating indexes for 'notifications' collection...");
  await db.collection('notifications').createIndex({ user_firebase_uid: 1 });
  console.log('✓ Notifications indexes created');

  console.log("Creating indexes for 'audit_logs' collection...");
  await db.collection('audit_logs').createIndex({ user_firebase_uid: 1 });
  await db.collection('audit_logs').createIndex({ timestamp: 1 });
  await db.collection('audit_logs').createIndex({ action: 1 });
  console.log('✓ Audit logs indexes created');

  console.log('\n=== All indexes created successfully! ===\n');
}

async function listCollections(db) {
  console.log('\n=== Database Collections ===\n');
  const collections = await db.listCollections().toArray();
  if (collections.length > 0) {
    for (let i = 0; i < collections.length; i++) {
      const collection = collections[i];
      const count = await db.collection(collection.name).countDocuments();
      console.log(`${i + 1}. ${collection.name} (${count} documents)`);
    }
  } else {
    console.log('No collections found');
  }
  console.log();
}

async function initializeDatabase() {
  console.log('=== MongoDB Database Initialization ===');
  console.log('Real Estate Listing Database\n');

  let client;
  try {
    const { client: connectedClient, db } = await getDatabase();
    client = connectedClient;
    await createIndexes(db);
    await listCollections(db);
  } catch (err) {
    console.error('Error initializing database:', err);
  } finally {
    if (client) {
      closeConnection(client);
    }
  }

  console.log('✓ Database initialization complete!');
}

initializeDatabase();
