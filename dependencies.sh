#!/bin/bash
# gsutil mb -p YOUR_PROJECT_ID -l us-central1 -b on gs://YOUR_PROJECT_ID-vertex-pipelines

echo "Installing Docker using Homebrew..."
brew install --cask docker

echo "Starting Docker locally..."
open -a Docker

echo "Please wait a moment for the Docker GUI and engine to fully start."

echo "=========================================="
echo "Google Cloud Platform Setup"
echo "=========================================="
PROJECT_ID=""
PROJECT_NUMBER=""
REGION="us-central1"

echo "1. Enabling required GCP APIs..."
# Requires your user to have 'roles/serviceusage.serviceUsageAdmin' to execute
gcloud services enable \
    compute.googleapis.com \
    aiplatform.googleapis.com \
    artifactregistry.googleapis.com \
    storage.googleapis.com \
    --project=$PROJECT_ID

echo "2. Granting Artifact Registry Reader role to Vertex AI Service Agent..."
# Gives Vertex AI the permission to pull the 'churn-predictor' Docker image
gcloud artifacts repositories add-iam-policy-binding ml-models \
    --location=$REGION \
    --project=$PROJECT_ID \
    --member="serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-aiplatform-cc.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.reader" || true

echo "3. Granting roles to the executing user account..."
# Automatically detect the active gcloud authenticated email
USER_EMAIL=$(gcloud config get-value account)

if [ -z "$USER_EMAIL" ]; then
    echo "Could not detect an active gcloud user. Please run 'gcloud auth login' first."
else
    echo "Found active user: $USER_EMAIL"
    
    gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member="user:$USER_EMAIL" \
        --role="roles/artifactregistry.writer"

    gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member="user:$USER_EMAIL" \
        --role="roles/aiplatform.user"

    gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member="user:$USER_EMAIL" \
        --role="roles/storage.objectAdmin"

    gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member="user:$USER_EMAIL" \
        --role="roles/serviceusage.serviceUsageAdmin"
fi

echo "Setup script finished successfully."