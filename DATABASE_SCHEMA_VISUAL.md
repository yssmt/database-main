# Real Estate Database Schema - Visual Guide

## Database Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         REAL ESTATE DATABASE                            │
│                         Database: real_estate_db                        │
└─────────────────────────────────────────────────────────────────────────┘


┌──────────────────────┐
│       USERS          │ (Main authentication & profile)
├──────────────────────┤
│ firebase_uid (PK)    │◄─────────────┐
│ email                │              │
│ name                 │              │
│ role                 │              │  References
│ verification_status  │              │
│ is_suspended         │              │
│ is_banned            │              │
└──────────────────────┘              │
         │                            │
         │ creates                    │
         ▼                            │
┌──────────────────────┐              │
│     PROPERTIES       │              │
├──────────────────────┤              │
│ property_id (PK)     │◄──┐          │
│ title                │   │          │
│ description          │   │          │
│ property_type        │   │          │
│ current_price        │   │          │
│ price_history[]      │   │ links to │
│ location{}           │   │          │
│ bedrooms             │   │          │
│ bathrooms            │   │          │
│ amenities[]          │   │          │
│ images[]             │   │          │
└──────────────────────┘   │          │
                           │          │
         │                 │          │
         │ has             │          │
         ▼                 │          │
┌──────────────────────┐   │          │
│      LISTINGS        │   │          │
├──────────────────────┤   │          │
│ listing_id (PK)      │   │          │
│ property_id (FK)─────┼───┘          │
│ lister_firebase_uid  │──────────────┘
│ status               │
│ views_count          │
│ verified_at          │
│ expires_at           │
└──────────────────────┘
         │
         │ referenced by
         │
    ┌────┴────┬─────────────┐
    ▼         ▼             ▼
┌─────────┐ ┌────────┐  ┌─────────┐
│  SAVED  │ │REVIEWS │  │ AUDIT   │
│LISTINGS │ │        │  │  LOGS   │
└─────────┘ └────────┘  └─────────┘
    │
    │ user saves
    │
┌──────────────────────┐
│ SAVED_LISTINGS       │
├──────────────────────┤
│ saved_id (PK)        │
│ user_firebase_uid    │─────┐
│ listing_id (FK)      │     │
│ notes                │     │
└──────────────────────┘     │
                             │
                             │ belongs to user
┌──────────────────────┐     │
│PROPERTY_COMPARISONS  │     │
├──────────────────────┤     │
│ comparison_id (PK)   │     │
│ user_firebase_uid    │◄────┤
│ property_ids[]       │     │
└──────────────────────┘     │
                             │
┌──────────────────────┐     │
│      REVIEWS         │     │
├──────────────────────┤     │
│ review_id (PK)       │     │
│ reviewer_uid         │◄────┤
│ target_type          │     
│ target_id            │     
│ rating (1-5)         │     
│ comment              │     
└──────────────────────┘     

┌──────────────────────┐
│   NOTIFICATIONS      │
├──────────────────────┤
│ notification_id (PK) │
│ user_firebase_uid    │ (null = broadcast)
│ title                │
│ message              │
│ is_read              │
└──────────────────────┘

┌──────────────────────┐
│VERIFICATION_DOCS     │
├──────────────────────┤
│ document_id (PK)     │
│ user_firebase_uid    │
│ document_type        │
│ document_url         │
│ status               │
│ verified_by_admin    │
└──────────────────────┘

┌──────────────────────┐
│    AUDIT_LOGS        │
├──────────────────────┤
│ log_id (PK)          │
│ user_firebase_uid    │
│ action               │
│ resource_type        │
│ resource_id          │
│ metadata{}           │
│ timestamp            │
└──────────────────────┘
```

---
