# IDRAK Onboarding Project

This is a small order management app for a warehouse packing system. It uses a FastAPI backend, PostgreSQL database, SQLAlchemy models, Alembic migrations, and a Vue frontend dashboard.

## Features

- View products and bottle styles
- Create orders with multiple items
- View and filter orders
- View the next order in the queue
- Fulfill an order with a worker ID
- View worker fulfillment stats
- Use a Vue dashboard to view and fulfill queued orders

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Vue
- Vite
- Docker Compose

## Setup

Open the project inside the Dev Container first.

Start PostgreSQL:

```bash
docker compose up -d
```

Go into the backend folder:

```bash
cd backend
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

Run the database migration:

```bash
alembic upgrade head
```

Seed the database:

```bash
python seed.py
```

Start the backend:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API docs:

```text
http://localhost:8000/docs
```

## Frontend

Open another terminal and go into the frontend folder:

```bash
cd frontend
```

Install frontend dependencies:

```bash
npm install
```

Start the frontend:

```bash
npm run dev -- --host 0.0.0.0 --port 5173
```

Frontend:

```text
http://localhost:5173
```

## Basic Test Flow

1. Start PostgreSQL.
2. Run the migration.
3. Run the seed script.
4. Start the backend.
5. Start the frontend.
6. Create an order from `/docs`.
7. Refresh the dashboard.
8. Enter a worker ID.
9. Click **Fulfill Order**.
