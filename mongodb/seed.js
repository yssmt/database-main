const path = require('path');
const mongoose = require('mongoose');
const dbOperations = require('./operations');
require('dotenv').config({ path: path.resolve(__dirname, '.env') });

const sampleUsers = [
  {
    firebase_uid: 'firebase_buyer_001',
    email: 'alice@example.com',
    name: 'Alice Johnson',
    role: 'buyer',
    phone: '+1234567890',
    verification_status: 'verified',
  },
  {
    firebase_uid: 'firebase_lister_001',
    email: 'agent1@realty.com',
    name: 'Sarah Agent',
    role: 'lister',
    phone: '+1234567892',
    verification_status: 'verified',
  },
];

const sampleProperties = [
  {
    property_id: 'prop_austin_001',
    title: 'Modern 3BR House in Downtown Austin',
    description: 'Beautiful modern home with open floor plan...',
    property_type: 'residential',
    current_price: 525000.00,
    location: {
      street: '456 Congress Ave',
      city: 'Austin',
      state: 'TX',
      zip_code: '78701',
      country: 'USA',
      latitude: 30.2672,
      longitude: -97.7431,
    },
    bedrooms: 3,
    bathrooms: 2.5,
    area_sqft: 2200,
    year_built: 2019,
    amenities: ['pool', 'garage', 'central_ac'],
  },
];

const sampleListings = [
  {
    listing_id: 'listing_001',
    property_id: 'prop_austin_001',
    lister_firebase_uid: 'firebase_lister_001',
    status: 'active',
  },
];

async function populateDatabase() {
  console.log('============================================================');
  console.log('       POPULATING DATABASE WITH SAMPLE DATA       ');
  console.log('============================================================');

  try {
    await mongoose.connect(process.env.MONGO_URL, { dbName: process.env.DB_NAME });

    console.log('\nInserting sample users...');
    for (const userData of sampleUsers) {
      const existing = await dbOperations.getUserByFirebaseUid(userData.firebase_uid);
      if (!existing) {
        await dbOperations.createUser(userData);
        console.log(`  ✓ Created user: ${userData.name}`);
      } else {
        console.log(`  - Skipping user (already exists): ${userData.name}`);
      }
    }

    console.log('\nInserting sample properties...');
    for (const propData of sampleProperties) {
      const existing = await dbOperations.getPropertyById(propData.property_id);
      if (!existing) {
        await dbOperations.createProperty(propData);
        console.log(`  ✓ Created property: ${propData.title}`);
      } else {
        console.log(`  - Skipping property (already exists): ${propData.title}`);
      }
    }

    console.log('\nInserting sample listings...');
    for (const listingData of sampleListings) {
      const existing = await dbOperations.getListingById(listingData.listing_id);
      if (!existing) {
        await dbOperations.createListing(listingData);
        console.log(`  ✓ Created listing for property: ${listingData.property_id}`);
      } else {
        console.log(`  - Skipping listing (already exists): ${listingData.listing_id}`);
      }
    }

    console.log('\n============================================================');
    console.log('              DATABASE SUMMARY              ');
    console.log('============================================================');

    const analytics = await dbOperations.getAnalytics();
    console.log(`\n  Total Users: ${analytics.total_users}`);
    console.log(`  Total Properties: ${analytics.total_properties}`);
    console.log(`  Total Listings: ${analytics.total_listings}`);
    console.log(`  Active Listings: ${analytics.active_listings}`);
    console.log(`  Pending Verifications: ${analytics.pending_verifications}`);

    console.log('\n============================================================');
    console.log('       SAMPLE DATA LOADED SUCCESSFULLY!       ');
    console.log('============================================================\n');
  } catch (error) {
    console.error('\n✗ Error populating database:', error);
  } finally {
    await mongoose.connection.close();
    console.log('✓ MongoDB connection closed.');
  }
}

populateDatabase();
