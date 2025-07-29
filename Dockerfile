# Base Python image
FROM python:3.12-slim

# Copy project depenpencies into container
COPY requirements.txt .

# Install required modules 
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set the container working directory
WORKDIR /app

# Copy project code
COPY src src

# Run the FastAPI application
ENTRYPOINT uvicorn --host 0.0.0.0 --port 8008 src.main:app
