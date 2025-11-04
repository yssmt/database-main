const mongoose = require('mongoose');

const messageSchema = new mongoose.Schema({
  message_id: { type: String, unique: true, required: true },
  sender_firebase_uid: { type: String, required: true, ref: 'User' },
  receiver_firebase_uid: { type: String, required: true, ref: 'User' },
  listing_id: { type: String, ref: 'Listing' },
  subject: { type: String },
  content: { type: String, required: true },
  status: { type: String, enum: ['unread', 'read'], default: 'unread' },
  sent_at: { type: Date, default: Date.now },
  read_at: { type: Date },
});

const Message = mongoose.model('Message', messageSchema);

module.exports = Message;
