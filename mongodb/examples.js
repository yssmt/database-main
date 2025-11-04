const path = require('path');
const mongoose = require('mongoose');
const { v4: uuidv4 } = require('uuid');
const dbOperations = require('./operations');
require('dotenv').config({ path: path.resolve(__dirname, '.env') });

async function exampleUserOperations() {
  console.log('\n============================================================');
  console.log('                 USER OPERATIONS EXAMPLES                 ');
  console.log('============================================================\n');

  console.log('1. Creating a new user...');
  const userData = {
    firebase_uid: `user_${uuidv4()}`,
    email: 'john.doe@example.com',
    name: 'John Doe',
    role: 'buyer',
    phone: '+1234567890',
  };
  const user = await dbOperations.createUser(userData);
  console.log(`✓ User created: ${user.name} (${user.email})`);

  console.log('\n2. Retrieving user...');
  const retrievedUser = await dbOperations.getUserByFirebaseUid(user.firebase_uid);
  console.log(`✓ Retrieved: ${retrievedUser.name}`);

  console.log('\n3. Updating user...');
  await dbOperations.updateUser(user.firebase_uid, { phone: '+9876543210' });
  console.log('✓ User updated');

  console.log('\n4. Getting all buyers...');
  const buyers = await dbOperations.getUsersByRole('buyer');
  console.log(`✓ Found ${buyers.length} buyer(s)`);

  return user.firebase_uid;
}

async function examplePropertyOperations() {
  console.log('\n============================================================');
  console.log('               PROPERTY OPERATIONS EXAMPLES               ');
  console.log('============================================================\n');

  console.log('1. Creating a new property...');
  const propertyData = {
    property_id: `prop_${uuidv4()}`,
    title: 'Beautiful 3BR House in Austin',
    description: 'Spacious family home with modern amenities and a pool',
    property_type: 'residential',
    current_price: 450000.00,
    location: {
      street: '123 Main Street',
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
    year_built: 2018,
    amenities: ['pool', 'garage', 'garden'],
  };
  const property = await dbOperations.createProperty(propertyData);
  console.log(`✓ Property created: ${property.title}`);

  console.log("\n2a. Searching properties with text 'pool'...");
  const results = await dbOperations.searchProperties({ search_term: 'pool' });
  console.log(`✓ Found ${results.length} propert(y/ies) matching 'pool'`);

  console.log('\n3. Updating property price...');
  await dbOperations.updateProperty(property.property_id, {
    current_price: 425000.00,
    price_change_reason: 'Price reduced for quick sale',
  });
  console.log('✓ Price updated');

  return property.property_id;
}

async function runAllExamples() {
  try {
    await mongoose.connect(process.env.MONGO_URL, { dbName: process.env.DB_NAME });
    await exampleUserOperations();
    await examplePropertyOperations();
  } catch (error) {
    console.error('An error occurred:', error);
  } finally {
    await mongoose.connection.close();
  }
}

runAllExamples();
