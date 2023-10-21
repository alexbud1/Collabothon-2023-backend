# Set the target platform as a build argument
ARG PLATFORM

# Use a multi-architecture base image
FROM --platform=$PLATFORM python:3.10.6-alpine

WORKDIR /app
COPY requirements.txt /app/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY backend-point.sh /
EXPOSE 8000

# Install dependencies
# RUN pip install --upgrade pip
# COPY ./requirements.txt .
# RUN pip install -r requirements.txt

# Copy the project
# COPY . .