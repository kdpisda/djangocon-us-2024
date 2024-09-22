FROM python:3.12-slim-bullseye as builder

# Set environment variables for Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

# Set the working directory
WORKDIR /src/

# Copy the requirements file into the container
ADD requirements.txt /src/
RUN pip install -r requirements.txt

ADD . /src/

# Expose port 8000
EXPOSE 8000
