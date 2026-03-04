# Database Schema Documentation

This document describes the data storage architecture of the Azure SQL Django application, which uses a hybrid approach combining Relational (SQL), Document (NoSQL), and Flat File (CSV) data sources.

## 1. Azure SQL Database (Relational)
Used for structured, transactional data. Managed via Django Models (`api/models.py`).

### ER Diagram Overview
`Store` --(1:N)--> `Product` (Implicit logic, currently loosely coupled)
`User` --(1:N)--> `Order`
`Order` --(1:N)--> `OrderItem`
`Product` --(1:N)--> `OrderItem`

### Tables

#### `api_store`
Stores physical store locations.
*   `id` (PK, Auto-increment)
*   `store_id` (Integer, Unique) - Business Key
*   `store_location` (String)

#### `api_product`
Stores catalog information.
*   `id` (PK, Auto-increment)
*   `name` (String, max 100)
*   `description` (Text, optional)
*   `price` (Decimal, 10 digits, 2 decimals)

#### `auth_user` (Django Default)
Stores user authentication data.
*   `id` (PK, Auto-increment)
*   `username` (String)
*   `email` (String)
*   ... (standard Django auth fields)

#### `api_order`
Stores order headers.
*   `id` (PK, Auto-increment)
*   `user_id` (FK to `auth_user`)
*   `status` (String: 'PENDING', 'COMPLETED', 'CANCELLED')
*   `created_at` (DateTime)

#### `api_orderitem`
Stores line items for each order.
*   `id` (PK, Auto-increment)
*   `order_id` (FK to `api_order`)
*   `product_id` (FK to `api_product`)
*   `quantity` (Integer)

---

## 2. MongoDB (NoSQL)
Used for unstructured, high-volume user feedback. Managed via `pymongo` in `api/views/reviews.py`.

### Collection: `reviews`
Stores product reviews and ratings.

#### Schema (Implicit)
```json
{
  "_id": "ObjectId",        // Auto-generated via Mongo
  "product_id": "Integer",  // Reference to SQL api_product.id
  "user_id": "Integer",     // Reference to SQL auth_user.id
  "rating": "Integer",      // 1-5
  "comment": "String",      // Text content
  "created_at": "ISO Date String"
}
```

---

## 3. External Data (CSV)
Used for offline business targets, ingested via Azure Data Factory.

### File: `target_sales.csv`
Stores monthly sales goals per product.

#### Schema
*   `product_id` (Integer) - References `api_product.id`
*   `target_sales` (Integer) - The unit sales goal for the month
*   `target_month` (String/Date) - e.g., "2023-10"

---

## 4. Hybrid Data Integration
The application and ADF pipeline link these distinct data sources:
1.  **Sales Performance**: `api_order` (SQL) joined with `target_sales.csv` (Blob) to compare Actual vs. Target.
2.  **Product Sentiment**: `api_product` (SQL) joined with `reviews` (Mongo) to correlate Sales vs. Ratings.
