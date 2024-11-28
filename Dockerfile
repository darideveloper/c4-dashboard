#
# NOTE: THIS DOCKERFILE IS GENERATED VIA "apply-templates.sh"
#
# PLEASE DO NOT EDIT IT DIRECTLY.
#

# Use Python 3.12 slim image
FROM python:3.12-slim

# Load env vars from caprover settings
ARG ENV

ARG SECRET_KEY
ARG DEBUG

ARG DB_ENGINE
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT

ARG TEST_HEADLESS

ARG LANDING_HOST

# Load env vars from caprover settings
ENV ENV=${ENV}

ENV SECRET_KEY=${SECRET_KEY}
ENV DEBUG=${DEBUG}

ENV DB_ENGINE=${DB_ENGINE}
ENV DB_NAME=${DB_NAME}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}

ENV TEST_HEADLESS=${TEST_HEADLESS}

ENV LANDING_HOST=${LANDING_HOST}

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app/

# Install system dependencies (e.g., for PostgreSQL support)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static files and migrate database
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Expose the port that Django/Gunicorn will run on
EXPOSE 80

# Command to run Gunicorn with the WSGI application for production
CMD ["gunicorn", "--bind", "0.0.0.0:80", "project.wsgi:application"]