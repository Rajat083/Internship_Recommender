# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .
COPY schemas.py .
COPY Recommender/ ./Recommender/

# Create necessary directories and files
RUN mkdir -p Recommender/model Recommender/dataset

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Create a startup script that runs all three steps
RUN echo '#!/bin/bash\n\
echo "Step 1: Running data preprocessing script..."\n\
cd /app && python -m Recommender.dataset.script\n\
echo "Step 2: Training the model..."\n\
cd /app && python -m Recommender.train\n\
echo "Step 3: Starting FastAPI server..."\n\
cd /app && uvicorn main:app --host 0.0.0.0 --port 8000' > /app/startup.sh && \
    chmod +x /app/startup.sh

# Command to run the application
CMD ["/app/startup.sh"]