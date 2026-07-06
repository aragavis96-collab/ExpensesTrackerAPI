# Expense Tracker REST API

A production-ready Expense Tracker REST API built using Django REST Framework. This project provides secure JWT authentication, expense management, analytics endpoints, pagination, filtering, and interactive API documentation with Swagger.

---

## Features

- User Registration
- JWT Authentication (Login & Refresh Token)
- Create Expense
- View All Expenses
- View Single Expense
- Update Expense
- Delete Expense
- Expense Summary
- Monthly Expense Summary
- Category-wise Expense Summary
- Dashboard Analytics
- Pagination
- Search Expenses
- Filter Expenses by Category
- Swagger API Documentation
- Postman Tested
- Render Deployment

---

## Tech Stack

- Python
- Django
- Django REST Framework
- SQLite
- JWT Authentication (SimpleJWT)
- Swagger (drf-yasg)
- Postman
- Git
- GitHub
- Render

---

## Live Demo

**API**

https://expensestrackerapi-2.onrender.com/

**Swagger Documentation**

https://expensestrackerapi-2.onrender.com/swagger/

---

## Project Structure

```
ExpensesTrackerAPI/
│── accounts/
│   ├── migrations/
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
│── expenses/
│   ├── migrations/
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
│── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
│── manage.py
│── requirements.txt
│── README.md
│── .gitignore
```

---

## API Endpoints

### Authentication

| Method | Endpoint |
|--------|----------|
| POST | `/accounts/register/` |
| POST | `/accounts/login/` |
| POST | `/accounts/refresh/` |

### Expense Management

| Method | Endpoint |
|--------|----------|
| GET | `/api/` |
| POST | `/api/` |
| GET | `/api/<id>/` |
| PUT | `/api/<id>/` |
| DELETE | `/api/<id>/` |

### Reports

| Method | Endpoint |
|--------|----------|
| GET | `/api/summary/` |
| GET | `/api/monthly-summary/` |
| GET | `/api/category-summary/` |
| GET | `/api/dashboard/` |

---

## Installation

```bash
git clone https://github.com/aragavis96-collab/ExpensesTrackerAPI.git

cd ExpensesTrackerAPI

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

---

## API Documentation

Swagger UI

https://expensestrackerapi-2.onrender.com/swagger/

---

