# Expense Tracker REST API

A production-ready Expense Tracker REST API built with Django REST Framework. The application supports secure JWT authentication, expense management, analytics endpoints, pagination, filtering, and interactive API documentation using Swagger.

## Features

- User Registration
- JWT Authentication (Login & Refresh Token)
- Create, Read, Update and Delete Expenses (CRUD)
- Expense Summary
- Monthly Expense Summary
- Category-wise Expense Summary
- Dashboard Analytics
- Pagination
- Search Expenses
- Filter by Category
- Swagger API Documentation
- Postman Tested
- Render Deployment

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

## Live Demo

**API:**  
https://expensestrackerapi-1.onrender.com/

**Swagger UI:**  
https://expensestrackerapi-1.onrender.com/swagger/

## API Endpoints

### Authentication

| Method | Endpoint |
|---------|----------|
| POST | `/accounts/register/` |
| POST | `/accounts/login/` |
| POST | `/accounts/refresh/` |

### Expenses

| Method | Endpoint |
|---------|----------|
| GET | `/api/` |
| POST | `/api/` |
| GET | `/api/<id>/` |
| PUT | `/api/<id>/` |
| DELETE | `/api/<id>/` |

### Reports

| Method | Endpoint |
|---------|----------|
| GET | `/api/summary/` |
| GET | `/api/monthly-summary/` |
| GET | `/api/category-summary/` |
| GET | `/api/dashboard/` |

## Installation

```bash
git clone https://github.com/aragavis96-collab/ExpensesTrackerAPI.git

cd ExpensesTrackerAPI

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```
