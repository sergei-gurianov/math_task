#!/bin/bash

# Check if LLM_MODEL_API_KEY is defined
if [ -z "$LLM_MODEL_API_KEY" ]; then
  echo "Error: LLM_MODEL_API_KEY is not set."
  echo "You can set it using bash command export LLM_MODEL_API_KEY=..."
  exit 1
fi

# Variables
IMAGE_NAME="math_questions_task"
CONTAINER_NAME="math_questions_task"
HOST_PORT=8008
CONTAINER_PORT=8008

# Build the Docker image
echo "Building Docker image ..."
docker build -t $IMAGE_NAME .

# Check if a container with the same name already exists
echo "Checking container with same name..."
docker rm -f $(docker ps -a -q --filter name=$IMAGE_NAME)

# Step 3: Run the Docker container
echo "Running Docker container..."
docker run -d \
  --name $CONTAINER_NAME \
  -e LLM_MODEL_API_KEY="$LLM_MODEL_API_KEY" \
  -p $HOST_PORT:$CONTAINER_PORT \
  $IMAGE_NAME

echo "Successfully started Docker container"
echo "Service is running on http://0.0.0.0:$HOST_PORT"
