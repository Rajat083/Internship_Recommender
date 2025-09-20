# PM Intern Recommender - Docker Deployment

This directory contains Docker configuration for deploying the PM Intern Recommender API.

## Quick Start

### Using Docker Compose (Recommended)
```bash
# Build and start the service
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop the service
docker-compose down
```

### Using Docker Commands
```bash
# Build the image
docker build -t pm-intern-recommender .

# Run the container with mounted data
docker run -d \
  --name pm-intern-recommender \
  -p 8000:8000 \
  -v "$(pwd)/Recommender/dataset:/app/Recommender/dataset:ro" \
  -v "$(pwd)/Recommender/model:/app/Recommender/model:ro" \
  pm-intern-recommender
```

### Windows Batch Script
```cmd
# Run the provided batch script
scripts\docker-run.bat
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

### Volumes
The Docker setup mounts the following directories:
- `./Recommender/dataset` → `/app/Recommender/dataset` (read-only)
- `./Recommender/model` → `/app/Recommender/model` (read-only)

### Ports
- **Container Port:** 8000
- **Host Port:** 8000 (configurable)

## Data Requirements

Before running the container, ensure you have:

1. **Dataset files** in `Recommender/dataset/`:
   - `students.csv`
   - `internships.csv`

2. **Model files** in `Recommender/model/`:
   - `trained_model.pkl`
   - `vectorizer.pkl`

## Docker Commands

### Container Management
```bash
# View running containers
docker ps

# View logs
docker logs pm-intern-recommender

# Follow logs in real-time
docker logs -f pm-intern-recommender

# Execute commands in container
docker exec -it pm-intern-recommender bash

# Stop container
docker stop pm-intern-recommender

# Remove container
docker rm pm-intern-recommender

# Remove image
docker rmi pm-intern-recommender
```

### Health Check
```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' pm-intern-recommender

# Manual health check
curl http://localhost:8000/health
```

## Production Deployment

### Security Considerations
1. **Remove development volumes** in production
2. **Use secrets management** for sensitive data
3. **Configure reverse proxy** (nginx/traefik)
4. **Enable HTTPS/TLS**
5. **Set up monitoring and logging**

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