#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "=========================================="
echo "1. Creating Python virtual environment..."
echo "=========================================="
# Create a virtual environment named '.venv'
python3 -m venv .venv

echo "=========================================="
echo "2. Activating virtual environment..."
echo "=========================================="
source .venv/bin/activate

echo "=========================================="
echo "3. Running build and push script..."
echo "=========================================="
./build_and_push.sh

echo "=========================================="
echo "4. Installing Python requirements..."
echo "=========================================="
# Upgrade pip to avoid warnings
pip install --upgrade pip
# Install requirements into the isolated virtual environment
pip install -r requirements.txt

echo "=========================================="
echo "5. Running pipeline deployment..."
echo "=========================================="
python3 pipeline.py

echo "=========================================="
echo "6. Deactivating virtual environment..."
echo "=========================================="
deactivate

echo "Done! Everything was run in an isolated virtual environment (.venv)."
