# Vehicle FastAPI Service 🚗

A simple **FastAPI microservice** for managing vehicle details using
**PostgreSQL**, **SQLAlchemy**, and **Alembic**.\
The project is containerized with **Docker** and supports CI/CD using
**GitHub Actions**.

------------------------------------------------------------------------

## ✨ Features

-   FastAPI-based REST API
-   PostgreSQL database
-   SQLAlchemy ORM
-   Alembic migrations
-   Health check endpoint
-   Prometheus metrics endpoint
-   Docker & Docker Compose support
-   GitHub Actions CI/CD pipeline
-   Pytest-based testing setup

------------------------------------------------------------------------

## 📁 Project Structure

    .
    ├── alembic.ini
    ├── app
    │   ├── config.py
    │   ├── database.py
    │   ├── main.py
    │   ├── models.py
    │   └── schemas.py
    ├── migrations
    │   └── versions
    ├── tests
    ├── Dockerfile
    ├── docker-compose.yml
    ├── .env
    ├── .env.example
    ├── requirements.txt
    └── README.md

------------------------------------------------------------------------

## ⚙️ Environment Variables

Create a `.env` file:

``` env
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_NAME=vehicle_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
```

------------------------------------------------------------------------

## 🚀 Run Locally (Without Docker)

``` bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API will be available at:

    http://localhost:8000

------------------------------------------------------------------------

## 🐳 Run with Docker Compose

``` bash
docker-compose up --build
```

API:

    http://localhost:8000

------------------------------------------------------------------------

## 🧪 Run Tests

``` bash
pytest
```

------------------------------------------------------------------------

## 🛠 Database Migrations

Create migration:

``` bash
alembic revision --autogenerate -m "create vehicles table"
```

Apply migration:

``` bash
alembic upgrade head
```

------------------------------------------------------------------------

## 📌 API Endpoints

### Health Check

    GET /api/health

### Prometheus Metrics

    GET /metrics

### Create Vehicle

    POST /api/vehicles

### List Vehicles

    GET /api/vehicles

------------------------------------------------------------------------

## 🧾 Example Vehicle Payload

``` json
{
  "number": "KL-07-AB-1234",
  "type": "Car",
  "owner_name": "John Doe"
}
```

------------------------------------------------------------------------

## 🔄 CI/CD

-   Runs tests on every push
-   Builds Docker image
-   Pushes image to Docker registry with version tag

------------------------------------------------------------------------

## 📄 License

MIT License
