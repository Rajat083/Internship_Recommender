#!/bin/bash

echo "Starting PM Intern Recommender API Server..."
echo

# Check if model files exist
if [ ! -f "trained_model.pkl" ]; then
    echo "Model files not found. Training model first..."
    python train.py
    if [ $? -ne 0 ]; then
        echo "Error: Model training failed!"
        exit 1
    fi
fi

echo "Starting FastAPI server..."
echo "API will be available at: http://localhost:8000"
echo "Interactive docs at: http://localhost:8000/docs"
echo

python main.py