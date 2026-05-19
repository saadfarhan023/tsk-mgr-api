# Task Manager API

A REST API for managing tasks with JWT authentication, built with FastAPI and PostgreSQL.

## Stack

- FastAPI, SQLModel, PostgreSQL, JWT (python-jose), bcrypt

## Endpoints

### Auth

- `POST /users/register` — create account
- `POST /users/login` — get JWT token

### Tasks (require Bearer token)

- `GET /tasks/` — list your tasks
- `POST /tasks/` — create a task
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
podman-compose up -d
```

### Start the API

```bash
uvicorn main:app --reload
```

## Environment Variables

```
DATABASE_URL=postgresql://user:password@localhost/taskdb
SECRET_KEY=your-secret-key
```
