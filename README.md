# RESTAURANT

___

## Loyiha Haqida
Bu loyiha restoranlardan joy buyurtma qilish uchun mo'ljallangan. Bu loyiha orqali joylarni va taomlarni ham oldindan buyurtma berib qo'yishingiz mumkin. Bu mijozlarni kutib qolmasligi uchun qulaylik yaratadi.

___

## Restaurant Management System

This is a Django-based RESTful API for managing a restaurant system, including restaurants, dining spaces, products, orders, order items, and user authentication. Below is an overview of the API endpoints and their functionalities.

## Table of Contents
- [Project Overview](#project-overview)
- [API Endpoints](#api-endpoints)
  - [Restaurant Management](#restaurant-management)
  - [Dining Space Management](#dining-space-management)
  - [Product Management](#product-management)
  - [Order Management](#order-management)
  - [Order Item Management](#order-item-management)
  - [Authentication and User Management](#authentication-and-user-management)
- [Setup Instructions](#setup-instructions)
- [Dependencies](#dependencies)

## Project Overview
This project provides a backend API for managing restaurant-related operations. It includes CRUD (Create, Read, Update, Delete) operations for restaurants, dining spaces, products, orders, and order items, along with user authentication features such as registration, OTP verification, login, and password management.

## API Endpoints

### Restaurant Management
| Endpoint | Method | Description | Name |
|----------|--------|-------------|------|
| `/crud/restaurant/create/` | POST | Create a new restaurant | `create_restaurant` |
| `/crud/restaurant/update/<int:pk>/` | PUT/PATCH | Update an existing restaurant | `update_restaurant` |
| `/crud/restaurant/delete/<int:pk>/` | DELETE | Delete a restaurant | `delete_restaurant` |
| `/list_restaurant/` | GET | List all restaurants | `list_restaurant` |
| `/detail_restaurant/<int:pk>/` | GET | Retrieve details of a specific restaurant | `detail_restaurant` |

### Dining Space Management
| Endpoint | Method | Description | Name |
|----------|--------|-------------|------|
| `/crud/diningspace/create/` | POST | Create a new dining space | `create_diningspace` |
| `/crud/diningspace/update/<int:pk>/` | PUT/PATCH | Update an existing dining space | `update_diningspace` |
| `/crud/diningspace/delete/<int:pk>/` | DELETE | Delete a dining space | `delete_diningspace` |
| `/list_diningspace/<int:pk>/` | GET | List dining spaces for a specific restaurant | `list_diningspace` |
| `/detail_diningspace/<int:pk>/` | GET | Retrieve details of a specific dining space | `detail_diningspace` |

### Product Management
| Endpoint | Method | Description | Name |
|----------|--------|-------------|------|
| `/crud/product/create/` | POST | Create a new product | `create_product` |
| `/crud/product/update/<int:pk>/` | PUT/PATCH | Update an existing product | `update_product` |
| `/crud/product/delete/<int:pk>/` | DELETE | Delete a product | `delete_product` |
| `/list_product/<int:pk>/` | GET | List products for a specific restaurant | `list_product` |
| `/detail_product/<int:pk>/` | GET | Retrieve details of a specific product | `detail_product` |

### Order Management
| Endpoint | Method | Description | Name |
|----------|--------|-------------|------|
| `/order/create/` | POST | Create a new order | `create_order` |
| `/order/update/<int:pk>/` | PUT/PATCH | Update an existing order | `update_order` |
| `/order/delete/<int:pk>/` | DELETE | Delete an order | `delete_order` |
| `/order/list/` | GET | List all orders | `list_order` |

### Order Item Management
| Endpoint | Method | Description | Name |
|----------|--------|-------------|------|
| `/orderitem/create/` | POST | Create a new order item | `create_order_item` |
| `/orderitem/update/<int:pk>/` | PUT/PATCH | Update an existing order item | `update_order_item` |
| `/orderitem/delete/<int:pk>/` | DELETE | Delete an order item | `delete_order_item` |
| `/orderitem/list/` | GET | List all order items | `list_order_items` |

### Authentication and User Management
| Endpoint | Method | Description | Name |
|----------|--------|-------------|------|
| `/registr/` | POST | Register a new user | `registr` |
| `/verify/` | POST | Verify user with OTP | `verify` |
| `/login_admin/` | POST | Admin login | `login_admin` |
| `/login_user/` | POST | User login | `login_user` |
| `/resend_otp/` | POST | Resend OTP for verification | `resend_otp` |
| `/change_password/` | POST | Change user password | `change_password` |
| `/forgot_password/` | POST | Initiate password reset | `forgot_password` |
| `/update_password/` | POST | Update password after reset | `update_password` |

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the API**:
   - The API will be available at `http://127.0.0.1:8000/`.
   - Use tools like Postman or curl to test the endpoints.

## Dependencies
- Django
- Django REST Framework (if used for API implementation)
- Python 3.8+
- Other dependencies listed in `requirements.txt`