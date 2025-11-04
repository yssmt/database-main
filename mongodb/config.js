require('dotenv').config();
const { MongoClient } = require('mongodb');

const uri = process.env.MONGO_URL;
const dbName = process.env.DB_NAME;

const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

async function getDatabase() {
  await client.connect();
  console.log('✓ Successfully connected to MongoDB');
  const db = client.db(dbName);
  console.log(`✓ Using database: ${dbName}`);
  return { client, db };
}

function closeConnection(client) {
  if (client) {
    client.close();
  }
}

module.exports = { getDatabase, closeConnection };
