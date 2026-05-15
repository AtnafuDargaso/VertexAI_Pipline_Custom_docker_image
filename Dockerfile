FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir pandas scikit-learn joblib google-cloud-storage gcsfs

COPY src/ /app/src/

ENTRYPOINT ["python", "/app/src/train.py"]
