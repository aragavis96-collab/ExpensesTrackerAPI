# Expense Tracker REST API

A RESTful Expense Tracker API built using Django REST Framework with JWT Authentication.

## Features

- User Registration
- User Login (JWT Authentication)
- Create Expense
- View All Expenses
- View Single Expense
- Update Expense
- Delete Expense
- Expense Summary
- Monthly Summary
- Category Summary
- Dashboard API
- Pagination
- Search & Category Filter
- Swagger API Documentation
- Postman Tested

## Tech Stack

- Python
- Django
- Django REST Framework
- SQLite
- JWT (SimpleJWT)
- Swagger (drf-yasg)
- Postman
- Git & GitHub

## API Endpoints

### Authentication

- POST `/accounts/register/`
- POST `/accounts/login/`
- POST `/accounts/refresh/`

### Expenses

- GET `/`
- POST `/`
- GET `/<id>/`
- PUT `/<id>/`
- DELETE `/<id>/`

### Reports

- GET `/summary/`
- GET `/monthly-summary/`
- GET `/category-summary/`
- GET `/dashboard/`

## Installation

```bash
git clone https://github.com/aragavis96-collab/ExpensesTrackerAPI.git

cd ExpensesTrackerAPI

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```
