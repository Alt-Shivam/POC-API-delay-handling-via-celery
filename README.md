
# POC API Delay Handling via Celery

This project demonstrates a proof of concept for handling delayed processing in an API using Celery. It leverages Docker and Docker Compose for environment setup and includes a 10-second delay when writing data to the database.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup Instructions

### 1. Clone the POC Repository

```bash
git clone https://github.com/Alt-Shivam/POC-API-delay-handling-via-celery.git
cd POC-API-delay-handling-via-celery
```

### 2. Build Container Image

```bash
docker-compose build
```

### 3. Run Setup

```bash
docker-compose up -d
```

Once the setup is complete, the API server will start and listen on port `5083` with a 10-second delay in writing data to the database.

## API Specification

### POST /api/employee

Add a new employee to the database.

```bash
curl -X POST http://127.0.0.1:5083/api/employee -H "Content-Type: application/json" -d '{"name": "Shivank"}'
```

### GET /api/employees

Retrieve a list of all employees.

```bash
curl -X GET http://localhost:5083/api/employees
```

### DELETE /api/employee/{id}

Delete an employee by ID.

```bash
curl -X DELETE http://localhost:5083/api/employee/1
```

## Example Docker Output

```plaintext
core@nodeb40:~/POC-API-delay-handling-via-celery$ docker-compose up 
Creating network "poc-api-delay-handling-via-celery_default" with the default driver
Creating poc-api-delay-handling-via-celery_db_1 ... done
Creating poc-api-delay-handling-via-celery_web_1 ... done
Attaching to poc-api-delay-handling-via-celery_db_1, poc-api-delay-handling-via-celery_web_1
db_1   | 
db_1   | PostgreSQL Database directory appears to contain a database; Skipping initialization
db_1   | 
db_1   | 2024-11-12 05:34:42.142 UTC [1] LOG:  starting PostgreSQL 13.16 (Debian 13.16-1.pgdg120+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit
db_1   | 2024-11-12 05:34:42.143 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
db_1   | 2024-11-12 05:34:42.143 UTC [1] LOG:  listening on IPv6 address "::", port 5432
db_1   | 2024-11-12 05:34:42.146 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
db_1   | 2024-11-12 05:34:42.151 UTC [27] LOG:  database system was shut down at 2024-11-12 05:34:36 UTC
db_1   | 2024-11-12 05:34:42.160 UTC [1] LOG:  database system is ready to accept connections
web_1  |  * Serving Flask app 'app'
web_1  |  * Debug mode: off
web_1  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
web_1  |  * Running on all addresses (0.0.0.0)
web_1  |  * Running on http://127.0.0.1:5083
web_1  |  * Running on http://172.21.0.3:5083
web_1  | Press CTRL+C to quit
```

## Additional Notes

This setup is intended for development and testing purposes. For production, consider using a WSGI server and ensure the proper configuration of Celery and the database.
