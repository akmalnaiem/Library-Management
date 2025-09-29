# Library Management API

A backend system for managing a small library, built with **Django** and **Django REST Framework (DRF)**.  
This API allows **librarians** to manage books and generate reports, and **customers** to browse, checkout, and manage their reading lists.

---

## Features

###  User
- Register and login via password.  
- Token-based authentication.  
- Support for different user roles (**Librarian** / **Customer**).

###  Librarian Actions
- **Add Book**: Add new books with title, author, ISBN, price, and cover image URL.  
- **Delete Book**: Remove a book from the library.  
- **Book Report**: View how many times each book has been issued, with filters:  
  - Most issued  
  - Least issued  
  - By author  

###  Customer Actions
- **Browse Books**: List available books with filters (most issued, least issued, author).  
- **Add to Cart**: Add a book to a personal cart.  
- **Checkout**: Issue books from cart, set return date (e.g., +14 days), and generate a bill summary.  
- **Save for Later**: Save a book to view later.  

---

##  Tech Stack
- **Backend**: Django, Django REST Framework  
- **Database**: SQLite (default) 
- **Authentication**: Token-based (DRF authtoken)  
- **Documentation**: Postman Collection  

---

##  Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/akmalnaiem/Library-Management.git
cd Library-Management
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser (for admin access)
```bash
python manage.py createsuperuser
```

### 6. Run Server
```bash
python manage.py runserver
```

## Base URL 
 `https://library-management-famh.onrender.com`


## Endpoints

### Authentication
- **POST** `/api/registration/` → User Registration  
- **POST** `/api/login/` → User Login  

### Librarian
- **GET** `/api/librarian/` → Librarian Panel   
- **POST** `/api/librarian/add-books/` → Add a new book  
- **DELETE** `/api/librarian/delete-books/<id>/` → Delete a book by ID  
- **GET** `/api/librarian/report/` → Get book issue report  

### Customer 
- **GET** `/api/customer/` → Customer Panel
- **GET** `/api/customer/browse-book/` → Browse available books  
- **POST** `/api/customer/save-book/` → Save a book for later  
- **POST** `/api/customer/add-to-cart/` → Add a book to cart  
- **DELETE** `/api/customer/remove-from-cart/` → Remove a book from cart  
- **POST** `/api/customer/checkout/` → Checkout books from cart  



## Admin Panel Access

You can access the Django admin panel here:  
 [https://library-management-famh.onrender.com/admin/](https://library-management-famh.onrender.com/admin/)


### Superuser Credentials
- **Username:** akki  
- **Password:** akki@2501


---

##  Authentication
- Register and login to obtain a token.  
- Use the token in Postman or frontend requests:  
---

##  API Documentation

You can test and explore the APIs using Postman.  

- Import the Postman collection:  
  [`docs/postman/Library Management.postman_collection.json`](docs/postman/Library Management.postman_collection.json)

---

##  Author
Developed by **Akmal Naiem Ansari**  
Feel free to ⭐ this repo if you like the project!  
