# Multi-Tenant Application

A scalable multi-tenant application built with FastAPI and Tortoise ORM. The application supports multiple tenants with isolated databases, implemented using a clean architecture approach.

## Features

- Multi-tenant architecture with database isolation
- Clean architecture (Repositories, Use Cases, Domain Models)
- JWT-based authentication
- Strategy pattern for database connection handling
- Support for both SQLite and PostgreSQL

## Prerequisites

- Docker and Docker Compose
- Git

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/charmheroku/multi-tenancy-app
cd multi-tenancy-app
```

2. Start the application using Docker Compose:
```bash
docker-compose up
```

3. The API will be available at http://localhost:8000


## API Endpoints

### Core Endpoints

- `POST /api/register` - Register a new core user
- `POST /api/login` - Login a core user
- `POST /api/organizations` - Create a new organization (tenant)

### Tenant Endpoints

All tenant endpoints require the `X-Tenant` header with a valid tenant ID.

- `POST /api/tenant/auth/register` - Register a tenant user
- `POST /api/tenant/auth/login` - Login a tenant user
- `GET /api/tenant/users/me` - Get the current tenant user profile

## Project Structure

```
multi_tenancy_app/
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── README.md
├── requirements.txt
└── src/
    ├── adapters/
    │   ├── database/
    │   │   ├── core_models.py
    │   │   ├── db_config.py
    │   │   ├── db_manager.py
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
    │   │   └── user_repository.py
    │   └── use_cases/
    │       ├── create_organization.py
    │       ├── __init__.py
    │       ├── login_user.py
    │       └── register_user.py
    ├── __init__.py
    ├── main.py
    ├── settings.py
    ├── tenant/
    │   ├── domain/
    │   │   ├── __init__.py
    │   │   └── models.py
    │   ├── __init__.py
    │   ├── repositories/
    │   │   ├── __init__.py
    │   │   └── user_repository.py
    │   └── use_cases/
    │       ├── __init__.py
    │       ├── login_user.py
    │       ├── profile_user.py
    │       └── register_user.py
    └── tests/
        ├── conftest.py
        ├── __init__.py
        ├── test_core.py
        └── test_tenant.py
```

## Architecture

The application follows clean architecture principles:

- `core/domain/models.py` - Core domain models
- `core/repositories/` - Repository interfaces for core
- `tenant/repositories/` - Repository interfaces for tenants
- `core/use_cases/` - Core business logic
- `tenant/use_cases/` - Tenant business logic
- `adapters/` - Implementation of repositories
- `api/` - FastAPI routes and dependencies

## Database Strategy Pattern

The application uses the Strategy pattern to support different database types:

- `SQLiteStrategy` - For SQLite databases (development/testing)
- `PostgresStrategy` - For PostgreSQL databases (production)

## Testing
...
