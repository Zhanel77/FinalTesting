## Final Testing

# Selenium Test Runner

This project runs a Selenium-based test for login, order functionality.

## How to Run

1. **Install dependencies**  
   Make sure you have Python installed, then run:

   ```bash
   pip install -r requirements.txt

   ```

2. **Prepare the backend**
   Open the following link in your browser to wake up the backend on Render:
   https://nodedatabase.onrender.com/

3. **Run the test**
   You can run the test using either of these commands:
   ```bash
   python .\web_driver_test\tests\test_orders.py
   or
   pytest
   ```



## Node.js Shopping API – Postman

## A concise guide for running the API test collection against https://nodedatabase.onrender.com.

**Endpoints Covered**
- POST /users/register → register (201)
- POST /users/login → login (200)
- GET  /products/get → list products (200)
- POST /orders/create → create order (201)
- DELETE /orders/delete/{orderId} → delete order (200)

**Running the Tests**
```Execute requests in order:
Register → Login → Get Products → Create Order → Delete Order
```

## Example Request (Login)

POST https://nodedatabase.onrender.com/users/login

Content-Type: application/json

{
  "name": "<your_username>",
  "password": "<your_password>"
}

**Expected response**:
{
  "message": "Login successful",
  "token": "<JWT-token>",
  "id": "<userId>",
  "role": "general"
}

