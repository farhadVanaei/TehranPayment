
# TehranPayment OTP

This project is a Django application that uses Celery for background tasks 
and JWT for authentication. It also includes a sample configuration for sending OTPs via SMS.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Docker.
- You have installed Docker Compose.

## Getting Started

To get a local copy up and running, follow these simple steps.

### 1. Clone the repository

```sh
git clone https://github.com/farhadVanaei/TehranPayment.git
cd TehranPayment
```

### 2. Set up environment variables

Create a `.env` file in the root directory of TehranPayment and add the following content:
FYI : you can use env_example file too 

```env
DEBUG=True
SECRET_KEY='*bxf&f_r*p_0+z+sl5j%$@)#q0d2=v&mgxr*brsm&d+3a8342q'
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
SIMPLE_JWT_ACCESS_TOKEN_LIFETIME=5  # In minutes
SIMPLE_JWT_REFRESH_TOKEN_LIFETIME=1  # In days
```

### 3. Build and run the Docker containers

Build and start the containers using Docker Compose:

```sh
docker-compose up --build
```

This will start the Django application and the Celery worker.

### 4. Apply migrations

Run the following command to apply the database migrations:

```sh
docker-compose run web python manage.py migrate
```

### 5. Create a superuser

Create a superuser to access the Django admin interface:

```sh
docker-compose run web python manage.py createsuperuser
```

### 6. Access the application Swagger

Open your web browser and navigate to `http://localhost:8000/swagger` to access the application.

## Project Structure

- `Dockerfile`: Instructions to build the Docker image for the Django application.
- `docker-compose.yml`: Configuration for Docker Compose to run the Django and Celery services.
- `requirements.txt`: List of Python dependencies.
- `manage.py`: Django's command-line utility for administrative tasks.

