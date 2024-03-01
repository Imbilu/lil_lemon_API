## Little Lemon Restaurant API

This is the API for the Little Lemon Restaurant, allowing users to browse menus, manage orders, and more.

### Features

* **Menu management:**
    * View all menu items.
    * (Manager only) Create, update, and delete menu items.
* **Cart management:**
    * Add, view, and delete items from your cart.
* **Order management:**
    * View your orders.
    * Create new orders from your cart.
    * (Manager) View all orders.
    * (Manager) Update order status and assign delivery crew.
    * (Delivery crew) View assigned orders and update their status.
* **User roles:**
    * Customer
    * Manager
    * Delivery crew

### User registration and authentication

* Users can register and obtain JWT tokens for API access.
* Djoser library is used for user registration and authentication endpoints.

### Prerequisites

* Python 3.x
* Django
* djoser
* django-rest-framework
* JWT library (e.g., `rest_framework_simplejwt`)

### Installation

1. Clone this repository.
2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

5. (Optional) Create a superuser for initial setup:

   ```bash
   python manage.py createsuperuser
   ```

### Usage

1. Start the development server:

   ```bash
   python manage.py runserver
   ```

### License

This project is licensed under the MIT License. See the `LICENSE` file for details.
