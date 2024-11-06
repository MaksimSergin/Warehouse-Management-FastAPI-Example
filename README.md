
# Warehouse Management API

## Description
A backend service built with FastAPI to manage warehouse operations. This includes managing products, product quantities, and customer orders. It uses PostgreSQL to store data and Docker to make setup easier.
## Table of Contents
- [Description](#description)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [API Endpoints](#api-endpoints)
  - [Product Management](#product-management)
  - [Order Management](#order-management)

## Prerequisites
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup

1. **Clone the repository**
    ```bash
    git clone https://github.com/yourcompany/Warehouse-Management-FastAPI-example.git
    cd Warehouse-Management-FastAPI-example
    ```

2. **Configure Environment**
   Copy `.env.sample` to `.env`:
    ```bash
    cp .env.sample .env
    ```

## Running the Application
To start the application, initialize all services using Docker Compose:

1. **Start Services**
    ```bash
    docker-compose --profile web up --build
    ```
   - The service will be accessible at `http://localhost:8000/`.


## Running Tests

The tests are set up with `pytest` and can be run through Docker Compose.

1. **Run Tests with Docker Compose**
   ```bash
   docker-compose --profile test up --build --abort-on-container-exit
   ```


## API Endpoints

### Product Management
- **Create Product**
  - **URL:** `/api/v1/products/`
  - **Method:** `POST`
  - **Request Body:**
    ```json
    {
      "name": "Sample Product",
      "description": "A new product in the warehouse",
      "price": 29.99,
      "quantity": 100
    }
    ```
  - **Response:**
    ```json
    {
      "id": 1,
      "name": "Sample Product",
      "description": "A new product in the warehouse",
      "price": 29.99,
      "quantity": 100
    }
    ```

- **Get Products**
  - **URL:** `/api/v1/products/`
  - **Method:** `GET`
  - **Query Parameters (optional):** `skip`, `limit`
  - **Response:**
    ```json
    [
      {
        "id": 1,
        "name": "Sample Product",
        "description": "A new product in the warehouse",
        "price": 29.99,
        "quantity": 100
      }
    ]
    ```

- **Get Product by ID**
  - **URL:** `/api/v1/products/{product_id}`
  - **Method:** `GET`
  - **Response:**
    ```json
    {
      "id": 1,
      "name": "Sample Product",
      "description": "A new product in the warehouse",
      "price": 29.99,
      "quantity": 100
    }
    ```

- **Update Product**
  - **URL:** `/api/v1/products/{product_id}`
  - **Method:** `PUT`
  - **Request Body:**
    ```json
    {
      "name": "Updated Product Name",
      "description": "Updated description",
      "price": 35.99,
      "quantity": 150
    }
    ```
  - **Response:**
    ```json
    {
      "id": 1,
      "name": "Updated Product Name",
      "description": "Updated description",
      "price": 35.99,
      "quantity": 150
    }
    ```

- **Delete Product**
  - **URL:** `/api/v1/products/{product_id}`
  - **Method:** `DELETE`
  - **Response:** No content (204 status code)

### Order Management
- **Create Order**
  - **URL:** `/api/v1/orders/`
  - **Method:** `POST`
  - **Request Body:**
    ```json
    {
      "items": [
        {
          "product_id": 1,
          "quantity": 5
        }
      ]
    }
    ```
  - **Response:**
    ```json
    {
      "id": 1,
      "status": "in_progress",
      "items": [
        {
          "product_id": 1,
          "quantity": 5
        }
      ]
    }
    ```

- **Get Orders**
  - **URL:** `/api/v1/orders/`
  - **Method:** `GET`
  - **Query Parameters (optional):** `skip`, `limit`
  - **Response:**
    ```json
    [
      {
        "id": 1,
        "status": "in_progress",
        "items": [
          {
            "product_id": 1,
            "quantity": 5
          }
        ]
      }
    ]
    ```

- **Get Order by ID**
  - **URL:** `/api/v1/orders/{order_id}`
  - **Method:** `GET`
  - **Response:**
    ```json
    {
      "id": 1,
      "status": "in_progress",
      "items": [
        {
          "product_id": 1,
          "quantity": 5
        }
      ]
    }
    ```

- **Update Order Status**
  - **URL:** `/api/v1/orders/{order_id}/status`
  - **Method:** `PATCH`
  - **Request Body:**
    ```json
    {
      "status": "shipped"
    }
    ```
  - **Response:**
    ```json
    {
      "id": 1,
      "status": "shipped",
      "items": [
        {
          "product_id": 1,
          "quantity": 5
        }
      ]
    }
    ```

