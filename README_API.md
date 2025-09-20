# PM Intern Recommender - FastAPI Web Service

A high-performance RESTful web service for the PM Intern Recommender system that provides ML-based internship recommendations.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the Model (if not already done)
```bash
cd Recommender
python train.py
```

### 3. Start the API Server
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check
```http
GET /health
```
Returns service status and basic statistics.

### Get Students List
```http
GET /students?limit=100
```
Returns list of available students.

### Get Internships List
```http
GET /internships?limit=100
```
Returns list of available internships.

### Recommend for Existing Student
```http
POST /recommend/student/{student_id}?top_n=5
```
Get recommendations for a student by ID.

**Example:**
```bash
curl -X POST "http://localhost:8000/recommend/student/1?top_n=5"
```

### Recommend for New Student
```http
POST /recommend/new-student
Content-Type: application/json

{
    "name": "John Doe",
    "skills": "python, machine learning, data science"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/recommend/new-student" \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "skills": "python, machine learning, data science"}'
```

### Batch Recommendations
```http
POST /recommend/batch?top_n=5&limit=10
```
Get recommendations for multiple students (limited for performance).

## Testing the API

### Using curl:

1. **Health Check:**
```bash
curl http://localhost:8000/health
```

2. **Student Recommendation:**
```bash
curl -X POST http://localhost:8000/recommend/student/1
```

3. **New Student Recommendation:**
```bash
curl -X POST "http://localhost:8000/recommend/new-student" \
     -H "Content-Type: application/json" \
     -d '{"name": "Jane Smith", "skills": "react, javascript, node.js"}'
```

### Using Python requests:

```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Get recommendation for student ID 1
response = requests.post("http://localhost:8000/recommend/student/1")
print(response.json())

# Get recommendation for new student
new_student = {
    "name": "Alice Johnson",
    "skills": "flutter, dart, mobile development"
}
response = requests.post("http://localhost:8000/recommend/new-student", json=new_student)
print(response.json())
```

## Response Examples

### Student Recommendation Response:
```json
{
    "student_id": 1,
    "student_name": "Student_1",
    "student_skills": ["machine learning", "data science", "agentic ai"],
    "recommendations": [
        {
            "rank": 1,
            "internship_id": 1401,
            "internship_title": "Data Science Intern",
            "company": "Kumar & Patel",
            "similarity_score": 0.8636,
            "required_skills": "machine learning, python, tensorflow",
            "stipend": "25000",
            "domain": "Technology"
        }
    ],
    "total_recommendations": 5
}
```

### Health Check Response:
```json
{
    "status": "healthy",
    "timestamp": "2025-09-19T10:30:00",
    "model_loaded": true,
    "students_count": 1000,
    "internships_count": 2000
}
```

## Docker Deployment

For comprehensive Docker deployment instructions, see `DOCKER.md`.

### Quick Docker Setup:
```bash
# Using Docker Compose (Recommended)
docker-compose up --build

# Using Docker commands
docker build -t pm-intern-recommender .
docker run -d -p 8000:8000 \
  -v "$(pwd)/Recommender/dataset:/app/Recommender/dataset:ro" \
  -v "$(pwd)/Recommender/model:/app/Recommender/model:ro" \
  pm-intern-recommender
```

## Configuration

### Environment Variables:
- `API_HOST`: Host to bind (default: 0.0.0.0)
- `API_PORT`: Port to bind (default: 8000)
- `LOG_LEVEL`: Logging level (default: info)

### Performance Tuning:
- Batch endpoint limits number of students processed
- Caching can be added for frequently accessed data
- Database integration possible for larger datasets

## Development

### Project Structure:
```
PM Intern Recommender/
├── main.py              # FastAPI application
├── schemas.py           # Pydantic models
├── requirements.txt     # Dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose setup
├── Recommender/        # ML components
│   ├── train.py        # Model training
│   ├── utils.py        # Utility functions
│   ├── recommend.py    # CLI recommendation tool
│   ├── dataset/        # Training data
│   └── model/          # Trained models
└── scripts/            # Helper scripts
```

### Adding New Features:
1. Add new Pydantic models in `schemas.py`
2. Implement new endpoints in `main.py`
3. Add utility functions in `utils.py` if needed
4. Update this documentation

## Performance

- **Startup Time**: ~2-3 seconds (loading model)
- **Single Recommendation**: ~50-100ms
- **Batch Processing**: Limited to 100 students for performance
- **Concurrent Requests**: Supports multiple concurrent users

## Troubleshooting

### Common Issues:

1. **Model not found error:**
   - Run `cd Recommender && python train.py` first to train the model

2. **Port already in use:**
   - Change port: `uvicorn main:app --port 8001`

3. **CORS errors:**
   - Update CORS settings in `main.py` for production

4. **Memory issues with batch processing:**
   - Reduce the `limit` parameter in batch requests

## License

This project is part of the PM Intern Recommender system.