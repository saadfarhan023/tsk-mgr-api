# Task Manager API

A REST API for managing tasks with JWT authentication, built with FastAPI and PostgreSQL.

## Stack

- FastAPI, SQLModel, PostgreSQL, JWT (python-jose), bcrypt, Celery, Redis, Alembic

## Endpoints

### Auth

- `POST /users/register` — create account
- `POST /users/login` — get JWT token

### Tasks (require Bearer token)

- `GET /tasks/` — list your tasks (supports `?skip=0&limit=10`)
- `POST /tasks/` — create a task
- `PATCH /tasks/{id}` — update title or description
- `PATCH /tasks/{id}/complete` — mark complete
- `DELETE /tasks/{id}` — delete a task

## Run locally

```bash
git clone https://github.com/saadfarhan023/tsk-mgr-api
cd tsk-mgr-api
pip install -r requirements.txt
cp .env.example .env  # fill in your values
```

### Start the database

```bash
podman-compose up db
```

### Start the API

```bash
uvicorn main:app --reload
```

### Start the Celery worker

```bash
celery -A celery_app worker --loglevel=info
```

### Run database migrations

```bash
alembic upgrade head
```

## Run with Podman (full stack)

Start database only:

```bash
podman-compose up db
```

Start database + api:

```bash
podman-compose up --build
```

## Environment Variables

```bash
DATABASE_URL=postgresql://user:password@localhost/taskdb
SECRET_KEY=your-secret-key
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
SMTP_FROM=your-email@gmail.com
```
