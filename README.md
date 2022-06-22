# Text Stat API (MVP)

### About

Generate a backend using Python, including interactive API documentation.

## Features

* Full **Docker** integration (Docker based).
* **Docker Compose** integration.
* **Production ready** Python web server using Uvicorn and Gunicorn.
* Python **[FastAPI](https://github.com/tiangolo/fastapi)** backend:
    * **Fast**: Very high performance, on par with **NodeJS** and **Go** (thanks to Starlette and Pydantic).
    * **Intuitive**: Great editor support. <abbr title="also known as auto-complete, autocompletion, IntelliSense">Completion</abbr> everywhere. Less time debugging.
    * **Easy**: Designed to be easy to use and learn. Less time reading docs.
    * **Short**: Minimize code duplication. Multiple features from each parameter declaration.
    * **Robust**: Get production-ready code. With automatic interactive documentation.
    * **Standards-based**: Based on (and fully compatible with) the open standards for APIs: <a href="https://github.com/OAI/OpenAPI-Specification" target="_blank">OpenAPI</a> and <a href="http://json-schema.org/" target="_blank">JSON Schema</a>.
    * [**Many other features**](https://github.com/tiangolo/fastapi) including automatic validation, serialization, interactive documentation, authentication with OAuth2 JWT tokens, etc.
* **SQLAlchemy** models.
* **Alembic** migrations.
* **Secure password** hashing by default.
* **JWT token** authentication.
* **CORS** (Cross Origin Resource Sharing).
* **Celery** worker that can import and use code from the rest of the backend selectively (you don't have to install the complete app in each worker).
* **Postgres** database.
* **Email notifications** for account creation and password recovery, compatible with:
    * Mailgun
    * SparkPost
    * SendGrid
    * ...any other provider that can generate standard SMTP credentials.
* **Nginx** integration, including Let's Encrypt **HTTPS** certificates automatic generation.
* GitHub CI (continuous integration).

## How to use it

Go to the directory where you want to create your project and run:

```bash
cp .env.example .env
```

## How to deploy

```bash
docker-compose -f docker-compose.yml up -d --build
```
