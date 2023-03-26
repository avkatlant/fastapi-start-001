# Start FastAPI Template

### The idea comes from the repositories:

FastAPI Best Practices
https://github.com/zhanymkanov/fastapi-best-practices  
Project sample built with these best-practices in mind.
https://github.com/zhanymkanov/fastapi_production_template

## Local Development

### Install requirements

```sh
python3.10 -m venv venv
. ./venv/bin/activate
pip install --upgrade pip setuptools
pip install -r requirements.txt
```

### Run DB

```sh
make up_dev && make log_dev
```

### Run Migrations

```sh
alembic upgrade head
```

### Run FastAPI

```sh
uvicorn src.main:app --reload
# or:
uvicorn src.main:app --reload --port 8000
```

### Stop

```sh
make down_dev && make clean
```

## Tests

All tests are integrational and require DB connection.

I've made is to use default database (`postgres_test`), separated from app's `app` database.

### Run tests

```sh
make tests
```

---

## For `.env` file

Specifying `echo=True` when initializing the engine will allow us to see the generated SQL queries in the console.

---

### Create Migrations

```sh
alembic revision --autogenerate -m "name"
```

### Migrate

```sh
alembic upgrade head
# or:
alembic upgrade [revision]
```
