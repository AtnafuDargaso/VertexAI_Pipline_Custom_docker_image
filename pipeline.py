import os
from kfp import dsl
from kfp import compiler
from google.cloud import aiplatform

# Configuration variables
PROJECT_ID = "" # Replace with your GCP project ID
REGION = "us-central1"
BUCKET_NAME = f"gs://{PROJECT_ID}-vertex-pipelines"
PIPELINE_ROOT = f"{BUCKET_NAME}/pipeline_root/"
# The image built and pushed to Artifact Registry
CUSTOM_IMAGE_URI = f"{REGION}-docker.pkg.dev/{PROJECT_ID}/ml-models/churn-predictor:latest"

@dsl.component(base_image=CUSTOM_IMAGE_URI)
def train_model(
    data_path: str,
    model_output: dsl.OutputPath(str),
    metrics_output: dsl.OutputPath(str)
):
    import subprocess
    import sys
    
    # Run the training script baked into the container
    subprocess.run([
        sys.executable, "/app/src/train.py",
        "--data_path", data_path,
        "--model_dir", model_output,
        "--metrics_path", metrics_output
    ], check=True)

@dsl.pipeline(
    name="customer-churn-prediction-pipeline",
    description="Pipeline for training a custom churn prediction model.",
    pipeline_root=PIPELINE_ROOT,
)
def churn_pipeline(
    data_path: str = "dummy_data", # In real use case, provide GCS path like "gs://bucket/data.csv"
    # data_path: str = "gs://YOUR_PROJECT_ID-vertex-pipelines/telecom_churn_data.csv",

):
    # Step 1: Train the model using the custom container
    train_task = train_model(
        data_path=data_path
    )
    
def compile_and_run(project_id: str, region: str):
    compiler.Compiler().compile(
        pipeline_func=churn_pipeline,
        package_path="churn_pipeline.json"
    )

    aiplatform.init(project=project_id, location=region)

    pipeline_job = aiplatform.PipelineJob(
        display_name="churn-prediction-job",
        template_path="churn_pipeline.json",
        enable_caching=True,
    )

    pipeline_job.submit()
    print("Pipeline submitted successfully!")

if __name__ == "__main__":
    compile_and_run(PROJECT_ID, REGION)
