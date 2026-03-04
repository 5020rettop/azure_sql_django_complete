# API Documentation

Base URL: `/api/`

## 1. Stores
Manage physical store locations (SQL).

### Endpoints
*   `GET /stores/` - List all stores.
*   `POST /stores/` - Create a new store.
*   `GET /stores/<store_id>/` - Retrieve a store.
*   `PUT /stores/<store_id>/` - Update a store.
*   `DELETE /stores/<store_id>/` - Delete a store.
*   `DELETE /stores/deleteAll/` - **BE CAREFUL**: Deletes ALL stores.

### Payloads
**Create/Update Store**:
```json
{
    "store_id": 101,
    "store_location": "New York - 5th Ave"
}
```

---

## 2. Products
Manage product catalog (SQL).

### Endpoints
*   `GET /products/` - List all products.
*   `POST /products/` - Create a new product.
*   `GET /products/<id>/` - Retrieve a product.
*   `PUT /products/<id>/` - Update a product.
*   `DELETE /products/<id>/` - Delete a product.
*   `DELETE /products/deleteAll/` - **BE CAREFUL**: Deletes ALL products.

### Payloads
**Create/Update Product**:
```json
{
    "name": "Super Widget",
    "description": "A high-quality widget.",
    "price": "19.99"
}
```

---

## 3. Orders
Manage customer orders (SQL).

### Endpoints
*   `GET /orders/` - List all orders.
*   `POST /orders/` - Create a new order (with nested items).
*   `GET /orders/<id>/` - Retrieve an order (includes items).
*   `PUT /orders/<id>/` - Update an order status.
*   `DELETE /orders/<id>/` - Delete an order.

### Payloads
**Create Order**:
*   **Note**: The backend assigns the order to the authenticated user (or the first user in the DB if using the demo setup).
```json
{
    "status": "PENDING",
    "items": [
        {
            "product": 1, 
            "quantity": 2
        },
        {
            "product": 5, 
            "quantity": 1
        }
    ]
}
```

---

## 4. Reviews
Manage product user reviews (MongoDB).

### Endpoints
*   `GET /reviews/` - List all reviews.
    *   **Filter**: `?product_id=1` checks reviews for a specific product.
*   `POST /reviews/` - Create a new review.
*   `GET /reviews/<id>/` - Retrieve a review (ID is a MongoDB ObjectId string).
*   `PUT /reviews/<id>/` - Update a review.
*   `DELETE /reviews/<id>/` - Delete a review.

### Payloads
**Create Review**:
```json
{
    "product_id": 1,
    "user_id": 1,
    "rating": 5,
    "comment": "Excellent product, highly recommended!"
}
```

---

## 5. Users
Manage application users (SQL - Django Auth).

### Endpoints
*   `GET /users/` - List all users.
*   `POST /users/` - Create a new user.
*   `GET /users/<id>/` - Retrieve a user.
*   `PUT /users/<id>/` - Update a user.
*   `DELETE /users/<id>/` - Delete a user.

### Payloads
**Create/Update User**:
```json
{
    "username": "jdoe",
    "email": "jdoe@example.com"
}
```

---

## 6. Utilities
*   `GET /connect-db/` - Checks connection to both SQL and MongoDB. Returns status `200` if both are healthy.
