# Event Management API

## Overview

This project is a simplified Event Management API designed for an admin panel. It supports role-based access (Admin and User), event creation, and basic ticket purchases.

## Tech Stack

- **Backend**: Django, Django REST Framework (DRF)
- **Database**: PostgreSQL/MySQL
- **Authentication**: Custom User Model (Optional: JWT-based Authentication)

## Features

### User Management

- Register a user as Admin or User.
- Role-based access control.

### Event Management (Admin Only)

- Create new events.
- Fetch all events.

### Ticket Purchase (User Only)

- Purchase tickets for an event.
- Validation to ensure tickets are available before purchase.

---

## Project Setup

### 1. Clone the Repository

```bash
git clone
cd EventAPI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 7. Run the Server

```bash
python manage.py runserver
```

---

## API Endpoints

### User Registration

- **POST** `/api/register/` - Register a user (Admin/User)

### Event Management (Admin Only)

- **POST** `/api/events/create` - Create a new event (Admin only)
- **GET** `/api/events/` - Fetch all events (Admin and User)

### Ticket Purchase (User Only)

- **POST** `/api/events/{id}/purchase/` - Purchase tickets
  - **Request Body:** `{ "quantity": <number_of_tickets> }`
  - **Validation:**
    - Ensures the requested quantity does not exceed available tickets.
    - Updates `tickets_sold` in the `Event` model.

---

## SQL Query for Top 3 Events by Tickets Sold

```sql
SELECT e.id, e.name, e.date, e.total_tickets, e.tickets_sold
FROM event e
ORDER BY e.tickets_sold DESC
LIMIT 3;
```


