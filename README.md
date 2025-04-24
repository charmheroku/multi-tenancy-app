# Multi-Tenant Application

A scalable multi-tenant application built with FastAPI and Tortoise ORM. The application supports multiple tenants with isolated databases, implemented using a clean architecture approach.

## Features

- Multi-tenant architecture with database isolation
- Clean architecture (Domain Models, Repositories, Use Cases)
- JWT-based authentication
- Strategy pattern for database connection handling
- Support for both SQLite and PostgreSQL
- Pydantic models for API request/response validation

## Prerequisites

- Docker and Docker Compose
- Git

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/charmheroku/multi-tenancy-app
   cd multi-tenancy-app
   ```

2. Start the application using Docker Compose:
```bash
docker-compose up --build
```

3. The API will be available at **http://localhost:8000**

## Interactive API Documentation  
Once the server is running, you can explore the API and test requests in‑browser:

- **Swagger UI:** <http://localhost:8000/docs>

## API Endpoints

### Core Endpoints

| Method | Path | Description |
| ------ | ---- | ----------- |
| `POST` | `/api/register` | Register a new core user |
| `POST` | `/api/login` | Login a core user |
| `POST` | `/api/organizations` | Create a new organization (tenant) |

### Tenant Endpoints

> All tenant endpoints require the `X-Tenant` header with a valid tenant ID.

| Method | Path | Description |
| ------ | ---- | ----------- |
| `POST` | `/api/tenant/auth/register` | Register a tenant user |
| `POST` | `/api/tenant/auth/login` | Login a tenant user |
| `GET`  | `/api/tenant/users/me`     | Get the current tenant user profile |
| `PUT`  | `/api/tenant/users/me`     | Update the current tenant user profile |

## Project Structure

```
multi_tenancy_app/
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
└── src/
    ├── adapters/
    │   ├── database/
    │   │   ├── core_models.py
    │   │   ├── db_config.py
    │   │   ├── db_manager.py
    │   │   ├── db_strategy.py
    │   │   ├── __init__.py
    │   │   └── tenant_models.py
    │   ├── __init__.py
    │   └── repositories/
    │       ├── core_postgres_repositories.py
    │       ├── __init__.py
    │       └── tenant_postgres_repositories.py
    ├── api/
    │   ├── dependencies/
    │   │   ├── auth.py
    │   │   ├── __init__.py
    │   │   └── tenant.py
    │   ├── __init__.py
    │   ├── routes/
    │   │   ├── core.py
    │   │   ├── __init__.py
    │   │   └── tenant.py
    │   └── schemas/
    │       ├── core.py
    │       ├── __init__.py
    │       └── tenant.py
    ├── core/
    │   ├── domain/
    │   │   ├── __init__.py
    │   │   └── models.py
    │   ├── __init__.py
    │   ├── repositories/
    │   │   ├── __init__.py
    │   │   ├── organization_repo.py
    │   │   └── user_repo.py
    │   └── use_cases/
    │       ├── create_organization.py
    │       ├── __init__.py
    │       ├── login_user.py
    │       └── register_user.py
    ├── __init__.py
    ├── main.py
    ├── settings.py
    └── tenant/
        ├── domain/
        │   ├── __init__.py
        │   └── models.py
        ├── __init__.py
        ├── repositories/
        │   ├── __init__.py
        │   └── user_repo.py
        └── use_cases/
            ├── __init__.py
            ├── login_user.py
            ├── register_user.py
            └── update_user.py
```

## Architecture

The application follows clean architecture principles:

- `core/domain/models.py` – Core domain models
- `core/repositories/` – Repository interfaces for core
- `tenant/repositories/` – Repository interfaces for tenants
- `core/use_cases/` – Core business logic
- `tenant/use_cases/` – Tenant business logic
- `adapters/` – Implementation of repositories
- `api/` – FastAPI routes and dependencies

## Database Strategy Pattern

The application uses the Strategy pattern to support different database types:

- **SQLiteStrategy** – for SQLite databases (development/testing)
- **PostgresStrategy** – for PostgreSQL databases (production)

## Testing

Coming soon…

