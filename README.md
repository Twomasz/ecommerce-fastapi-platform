# E-commerce Platform
Simple **FastAPI** application for managing basic operations of an **e-commerce platform**.

The application provides a set of API endpoints for **displaying or creating** data about **users, products and orders**.

Information used by app comes from local **SQLite** database based on ORM model provided by **SQLAlchemy**.

The main advantage of implemented approach is the use of **asynchronous** operations, 
which introduce parallel computing that allows to handle multiple requests at the same time.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Management](#environment-management)
- [Testing](#testing)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [Users](#users)
  - [Products](#products)
  - [Orders](#orders)

## Requirements
- Python 3.12+
- Poetry

## Installation
Create a virtual environment and install the dependencies using Poetry:
```bash
poetry config virtualenvs.in-project true
poetry install
```

## Environment Management
To initialize SQLite database, it is required to create a `.env` file in the root directory of the project with the following content:
```
DATABASE_URL="sqlite+aiosqlite:///./ecommerce.db"
```
It is crucial to use `aiosqlite` driver to enable asynchronous operations.
Once app is running, the database will be created automatically with all required tables.

## Testing
To run tests firstly install the development dependencies:
```bash
poetry install --dev
```
Then run the tests using the following command:
```bash
poetry run pytest
```
The tests are run in a separate (in `:memory:`) database to avoid any conflicts with the main database.
It covers all endpoints and basic operations of the application.


## Running the Application
To run the application, use the following command:
```bash
poetry run uvicorn ecommerce_project.app:app --reload
```
To enjoy non-empty database, you can use the following command to fill it with sample data:
```bash
poetry run python scripts/fill_sample_db.py
```
Once it's done, you can use some [`sample_api_calls.http`](scripts/sample_api_calls.http) 😊


## API Endpoints
The application provides a set of API endpoints for managing users, products and orders.

You can find sample API calls in the [`sample_api_calls.http`](scripts/sample_api_calls.http) file!

Other than that, you can use the following complete list of available endpoints:
### Users
- **GET** `/users` - get all users
- **POST** `/users/register` - create a new user
- **GET** `/users/id/{user_id}` - get user by ID
- **PUT** `/users/id/{user_id}` - update user by ID
- **DELETE** `/users/id/{user_id}` - delete user by ID

### Products
- **GET** `/products` - get all products
- **POST** `/products/fill` - create a new product or increase its quantity
- **GET** `/products/search` - search for products by name, category or price
- **GET** `/products/id/{product_id}` - get product by ID
- **DELETE** `/products/id/{product_id}` - delete product by ID

### Orders
- **GET** `/orders` - get all orders
- **GET** `/orders/id/{order_id}` - get order by ID
- **POST** `/orders/place_order` - create a new order
- **GET** `/orders/history/users/{user_id}` - get order history for user by ID
