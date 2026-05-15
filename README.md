# Vertex AI Custom Container Pipeline
This project demonstrates an end-to-end automated deployment for a machine learning model on Google Cloud Platform. It containerizes a Python model training script using Docker, pushes the image to Artifact Registry, and uses the Kubeflow Pipelines (KFP) SDK to orchestrate and execute a Vertex AI model training job.

## Overall Process
The model codebase is containerized into a Docker image and pushed to Google Cloud Artifact Registry. A Vertex AI pipeline is then compiled and executed using the Kubeflow SDK, which provisions cloud compute resources, pulls the image, trains the predictive model, and saves the resulting model artifacts to Google Cloud Storage.

---

## Prerequisites & GCP Setup

> **⚠️ IMPORTANT INITIAL CONFIGURATION ⚠️**  
> Before running this repository in a new environment, you must perform a find-and-replace to map your Google Cloud project details.  
> 
> *   **`build_and_push.sh`**: Replace `YOUR_PROJECT_ID` with your GCP Project ID.  
> *   **`pipeline.py`**: Replace `YOUR_PROJECT_ID` with your GCP Project ID.  
> *   **`dependencies.sh`**: Replace `YOUR_PROJECT_ID` with your GCP Project ID, and replace the generic project number `Project Number` with your project's unique number.  
> *   **`README.md`** (this file): Replace the placeholder `PROJECTID` with your Project ID.


Before running this project, ensure you have the following installed:
* [Google Cloud SDK (`gcloud`)](https://cloud.google.com/sdk/docs/install)
* [Docker](https://docs.docker.com/get-docker/)
* `python3` (Ensure Python 3.10+ is supported/used)

### 1. Enable Required GCP APIs
Run the following commands to enable the necessary Google Cloud services in your project:

```bash
gcloud services enable \
    compute.googleapis.com \
    aiplatform.googleapis.com \
    artifactregistry.googleapis.com \
    storage.googleapis.com
```

### 2. IAM Permissions (For your user/account)
The account running the scripts must have the following roles:
* **Artifact Registry Administrator/Writer** (`roles/artifactregistry.admin` or `roles/artifactregistry.writer`): To create repos and push Docker images.
* **Vertex AI User** (`roles/aiplatform.user`): To submit Pipeline jobs.
* **Storage Object Admin** (`roles/storage.objectAdmin`): To read/write pipeline artifacts in GCS.

### 3. Service Account Permissions (For Vertex AI)
The Vertex AI service account running the pipeline inside GCP needs read access to your Artifact Registry repository to pull your custom Docker image.
Run this command (replace `project#` with your project number, and `PROJECTID` with your project ID):

```bash
gcloud artifacts repositories add-iam-policy-binding ml-models \
    --location=us-central1 \
    --project=PROJECTID \
    --member="serviceAccount:service-854107379584@gcp-sa-aiplatform-cc.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.reader"
```
*(Note: Vertex AI should automatically configure Storage Admin rights for its agent to the staging bucket, but verify if you face GCS access errors).*

### 4. Create the Cloud Storage Bucket
The pipeline will need a Google Cloud Storage bucket to save the pipeline root directories, model output bindings, and metrics.
```bash
gsutil mb -p PROJECTID -l us-central1 -b on gs://PROJECTID-vertex-pipelines
```

---

## How to Run

1. **Authenticate your environment:**
   ```bash
   gcloud auth login
   gcloud config set project PROJECTID
   ```

2. **Execute the automation script:**
   This wrapper script will set up a Python virtual environment, build & push the Docker image, and submit the pipeline job automatically.
   ```bash
   chmod +x run_in_venv.sh build_and_push.sh
   ./run_in_venv.sh
   ```

3. **Monitor Execution:**
   The output in the terminal will provide a URL to the Vertex AI console. Click this URL to view the DAG pipeline running live in the Google Cloud Console.

### Testing With "Real" telecom Data (Optional)
By default, the pipeline runs using synthetic memory data generated inside `train.py`. You can use a more realistic dataset by following these steps:

1. Generate the CSV file locally:
   ```bash
   python generate_telecom_data.py
   ```
2. Upload the file to your GCS Bucket:
   ```bash
   gsutil cp telecom_churn_data.csv gs://PROJECTID-vertex-pipelines/telecom_churn_data.csv
   ```
3. Update `pipeline.py` to point to the GCS URI as the `data_path` parameter, then execute `./run_in_venv.sh` again.

---

## Project Structure
* `src/train.py` - Core PyScikit Learn modeling. Parses CLI arguments to read data and dump resulting artifacts (Metrics and Joblib models).
* `Dockerfile` - Packages the training script with necessary Python dependencies (like `pandas`, `scikit-learn`, `google-cloud-storage`).
* `build_and_push.sh` - Configuration to push the image to Google Cloud Artifact Registry.
* `pipeline.py` - The Kubeflow (`kfp`) configuration directing Vertex AI to run step sequences using our custom Docker container.
* `run_in_venv.sh` - Bash wrapper ensuring dependency isolation while deploying securely.
* `generate_telecom_data.py` - Provides a mock dataset mimicking real-world features for churn prediction testing.
* `app.py` - A Streamlit interactive UI application for exploring the dataset and making real-time predictions locally.
* `requirements.txt` - Lists all Python dependencies required for the project.

**Resources:**
* [Vertex AI Pipelines Documentation](https://cloud.google.com/vertex-ai/docs/pipelines/build-pipeline)