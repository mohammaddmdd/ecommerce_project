# Django Project Instructions

## Project Stack

| Name           | Version  | Name II    | Version |
|:--------------:|:--------:|:----------:|:-------:|
| Python         |   3.10   | Nginx      |         |
| Django         |  4.1.0   | Gunicorn   |         |
| Ubuntu         | 20.10.14 | Gevent     |         |
| Docker         |  20.04   | Redis      |         |
| Git            |   2.33   | RabbitMQ   |         |
| Postgres       |   14.3   | Celery     |         |
| docker-compose |   14.3   | Prometheus |         |

## Development Environment Configuration

### Clone Project

The first thing to do is to clone the repository

### Python Env Setup

Create a virtual environment to install dependencies inside it and activate it.

#### Virtualenv package

Install Virtualenv package

```sh
pip install virtualenv --upgrade
```

Create a virtual environment

```sh
virtualenv .env
```

Activate virtual environment in linux

```sh
source .env/bin/activate
```

Activate virtual environment in windows

```sh
.\.env\Scripts\activate.bat
```

To install dependencies you can use bellow command.

```sh
pip install django
```

To save all dependencies version always after installation use bellow command.

```sh
pip freeze > requirements.txt
```

To install all current dependencies on your environment:

```sh
pip install -r requirements.txt
```

---

#### pipenv package

Install pipenv package

```sh
pip install pipenv --upgrade
```

activate virtual environment

```sh
pipenv shell
```

To install a package you can use bellow command. One of feature of this virtual environment is to lock the dependencies automatically.

**NOTICE:** It maybe slow on your local machine.

```sh
pipenv install django
```

To install all current dependencies on your environment:

```sh
pipenv install
```

### Prepare Settings

#### Secret Key Configuration

Add a secret key to `settings.ini` file.

```py
import secrets

print(secrets.token_urlsafe(50))
```

**TIP:** Copy generated secret key to `settings.ini` with `SECRET_KEY`.

```ini
SECRET_KEY=<your-strong-password>
```

#### Database Configuration

Now you need to config your database configuration. Database of current project is `postgresql`.

```ini
# your database name that is created on postgreSQL
DB_NAME=

# Enter your database user and it must have access to the created db.

DB_USER=

# Enter your specified user's database password.
DB_PASSWORD=

# Accessible port of the installed database (default is `5432`)
DB_PORT=

# Local Database is `localhost` if you are using docker must enter `docker-service-name`
DB_HOST=

# Select a test database name for the created user.
DB_TEST=
```

In this section you should know how to create a database with the user in PostgreSQL

Create Database on your postgres DBMS

```sql
CREATE DATABASE <db_name>;
```

Create User

```sql
CREATE USER db_user WITH PASSWORD 'your-strong-password';
ALTER ROLE db_user SET client_encoding TO 'utf8';
ALTER ROLE db_user SET default_transaction_isolation TO 'read committed';
ALTER db_user SET timezone TO 'UTC';
```

Access user to create database (for django tests database).

```sql
ALTER USER db_user CREATEDB;
```

Connect user to the database

```sql
GRANT AL PRIVILEGES ON DATABASE db_name TO db_user;
```

### Prepare Development Environment

Before project running, you must run tests to check project is work correctly. To run the tests, `cd` into the directory where `manage.py` is already exist:

```sh
python manage.py test
```

#### Run Unit Tests

Once `pipenv` or `pip` has finished downloading the dependencies, Then simply apply the migrations:

```sh
python manage.py makemigrations
python manage.py migrate
```

#### Run Project

You can now run the development server:

```sh
python manage.py runserver 8000
```

Finally navigate to http://localhost:8000

## Production Environment Configuration
