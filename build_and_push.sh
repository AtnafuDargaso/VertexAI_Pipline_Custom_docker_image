#!/bin/bash

# Configuration variables - Replace these with your actual values
PROJECT_ID=""
REGION="us-central1"
REPO_NAME="ml-models"
IMAGE_NAME="churn-predictor"
IMAGE_TAG="latest"

IMAGE_URI="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}:${IMAGE_TAG}"

echo "Creating Artifact Registry repository if it doesn't exist..."
gcloud artifacts repositories create ${REPO_NAME} \
    --repository-format=docker \
    --location=${REGION} \
    --description="Docker repository for ML models" \
    --project=${PROJECT_ID} || true

echo "Configuring Docker authentication..."
gcloud auth configure-docker ${REGION}-docker.pkg.dev -q

echo "Building Docker image..."
docker build -t ${IMAGE_URI} .

echo "Pushing Docker image to Artifact Registry..."
docker push ${IMAGE_URI}

echo "Image pushed successfully: ${IMAGE_URI}"
echo "You can now run 'python pipeline.py' to deploy and run the pipeline."
