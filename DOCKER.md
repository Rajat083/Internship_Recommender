# PM Intern Recommender - Docker Deployment

This directory contains Docker configuration for deploying the PM Intern Recommender API with automatic data generation and model training.

## Quick Start

### Option 1: Using Pre-built Image (Fastest)
```bash
docker run -p 8000:8000 razzat/internship_recommender
```

### Option 2: Using Docker Compose
```bash
# Build and start the service
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop the service
docker-compose down
```

### Option 3: Build Locally
```bash
# Build the image
docker build -t razzat/internship_recommender .

# Run the container
docker run -p 8000:8000 razzat/internship_recommender
```

### Windows Batch Script
```cmd
# Run the provided batch script
scripts\docker-run.bat
```

## Container Startup Process

The Docker container executes a complete end-to-end pipeline:

### Step 1: Data Generation
- Runs `Recommender/dataset/script.py`
- Generates 1000 student profiles and 2000 internship listings
- Creates `students.csv` and `internships.csv` files

### Step 2: Model Training
- Runs `Recommender/train.py`
- Trains TF-IDF vectorizer and k-NN model
- Saves trained models to `model/` directory

### Step 3: API Server Startup
- Starts FastAPI server using uvicorn
- Loads trained models into memory
- Makes API available on port 8000

### Expected Output
```
Step 1: Running data preprocessing script...
✅ Files generated: internships.csv, students.csv
Step 2: Training the model...
Loading datasets...
Loaded 1000 students and 2000 internships
Training completed successfully!
Step 3: Starting FastAPI server...
INFO: Uvicorn running on http://0.0.0.0:8000
```

## Access the API

- **API Base URL:** http://localhost:8000
- **Interactive Documentation:** http://localhost:8000/docs
- **OpenAPI Schema:** http://localhost:8000/openapi.json
- **Health Check:** http://localhost:8000/health

## Configuration

### Environment Variables
- `PYTHONPATH`: Set to `/app` (configured in Dockerfile)
- `PYTHONUNBUFFERED`: Set to `1` for real-time logs
- `PYTHONDONTWRITEBYTECODE`: Set to `1` to prevent .pyc files

### Volumes (Not Required)
The new Docker setup is fully self-contained and doesn't require external volumes:
- Data generation happens inside the container
- Model training occurs during container startup
- All files are created and managed internally

### Ports
- **Container Port:** 8000
- **Host Port:** 8000 (configurable)

## Data Requirements

**No external data requirements!** The container automatically:

1. **Generates sample datasets** using `script.py`:
   - Creates 1000 diverse student profiles
   - Generates 2000 internship opportunities across 7 domains
   - Produces realistic skill combinations and requirements

2. **Trains ML models** using `train.py`:
   - TF-IDF vectorizer for skill text processing
   - k-nearest neighbors model for similarity matching
   - Automatically saves trained models

## Docker Commands

### Container Management
```bash
# View running containers
docker ps

# View logs
docker logs <container_id>

# Follow logs in real-time  
docker logs -f <container_id>

# Execute commands in container
docker exec -it <container_id> bash

# Stop container
docker stop <container_id>

# Remove container
docker rm <container_id>

# Remove image
docker rmi razzat/internship_recommender
```

### Health Check
```bash
# Manual health check
curl http://localhost:8000/health

# Expected response:
# {
#   "status": "healthy",
#   "timestamp": "2025-09-20T10:30:00",
#   "ml_model_loaded": true,
#   "students_count": 1000,
#   "internships_count": 2000
# }
```

## Production Deployment

### Docker Hub Deployment
The image is available on Docker Hub:
```bash
docker pull razzat/internship_recommender
docker run -p 8000:8000 razzat/internship_recommender
```

### Security Considerations
1. **Use production-grade WSGI server** (already configured with uvicorn)
2. **Configure reverse proxy** (nginx/traefik) for HTTPS
3. **Set up monitoring and logging**
4. **Resource limits** for container memory/CPU

### Example Production docker-compose.yml
```yaml
version: '3.8'
services:
  api:
    image: pm-intern-recommender:latest
    restart: always
    environment:
      - WORKERS=4
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
```

## Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Change host port
   docker run -p 8001:8000 pm-intern-recommender
   ```

2. **Data files not found:**
   - Verify data files exist in mounted directories
   - Check volume mount paths
   - Ensure read permissions

3. **Container fails to start:**
   ```bash
   # Check logs
   docker logs pm-intern-recommender
   
   # Run interactively for debugging
   docker run -it --rm pm-intern-recommender bash
   ```

4. **Health check failures:**
   - Verify API is responding on port 8000
   - Check application logs for errors
   - Ensure all dependencies are installed

### Performance Tuning

- **Memory:** Increase container memory for large datasets
- **CPU:** Use multi-worker deployment for high load
- **Storage:** Use faster storage for model files

## Development

### Live Development with Docker
```bash
# Mount source code for development
docker run -it --rm \
  -p 8000:8000 \
  -v "$(pwd):/app" \
  pm-intern-recommender \
  uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Building with Different Environments
```bash
# Development build
docker build --target development -t pm-intern-recommender:dev .

# Production build
docker build --target production -t pm-intern-recommender:prod .
```