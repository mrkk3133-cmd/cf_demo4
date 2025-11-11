#!/bin/bash
# ==========================================================
# Local Cloud Function Runner
# ----------------------------------------------------------
# Starts Functions Framework for hello_http from project root
# ==========================================================

set -e  # Exit if any command fails

# Navigate to project root
cd "$(dirname "$0")/../cloud_function_trainer"

# Define environment
export FUNCTION_TARGET="hello_http"
export FUNCTION_PORT=8080
export PYTHONPATH=$(pwd)

# Check if requirements exist in root
if [ ! -f "requirements.txt" ]; then
  echo "❌ requirements.txt not found in project root!"
  exit 1
fi

# Install dependencies
echo "🔧 Installing dependencies..."
pip install -r requirements.txt --quiet

echo "🚀 Starting Functions Framework (target=${FUNCTION_TARGET}, port=${FUNCTION_PORT})..."
functions-framework \
  --target=${FUNCTION_TARGET} \
  --port=${FUNCTION_PORT} \
  --debug
