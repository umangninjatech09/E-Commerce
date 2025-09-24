# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./order_service/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the order_service project directory into the container
COPY ./order_service /app/order_service

# Expose the port the app runs on
EXPOSE 8001

# Define the command to run your application
CMD ["uvicorn", "order_service.main:app", "--host", "0.0.0.0", "--port", "8001"]