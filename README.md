# PM Intern Recommender

A machine learning-powered recommendation system that matches students with relevant internship opportunities based on skill similarity using TF-IDF vectorization and k-nearest neighbors algorithm.

## Overview

The PM Intern Recommender is a FastAPI-based web service that provides intelligent internship recommendations by analyzing the similarity between student skills and internship requirements. The system uses natural language processing and machine learning techniques to deliver personalized recommendations.

## Features

- **Skill-based Matching**: Uses TF-IDF vectorization to analyze and match skills
- **Machine Learning**: Implements k-nearest neighbors algorithm for similarity computation
- **REST API**: FastAPI-based web service with automatic OpenAPI documentation
- **Multiple Endpoints**: Support for individual, new student, and batch recommendations
- **Data Validation**: Pydantic models ensure data integrity and type safety
- **Health Monitoring**: Built-in health check endpoints
- **Containerized**: Docker support for easy deployment

## Architecture

### Components

- **FastAPI Application** (`main.py`): Web service with REST endpoints
- **ML Pipeline** (`Recommender/`): Core machine learning functionality
  - `train.py`: Model training pipeline
  - `utils.py`: Shared utility functions
  - `recommend.py`: CLI recommendation tool
- **Data Schemas** (`schemas.py`): Pydantic models for API validation
- **Datasets**: Student profiles and internship listings

### Technology Stack

- **Backend**: FastAPI, Python 3.10+
- **Machine Learning**: scikit-learn, pandas, numpy
- **Data Processing**: TF-IDF Vectorization, text preprocessing
- **API Documentation**: OpenAPI/Swagger
- **Containerization**: Docker, Docker Compose

## Installation

### Prerequisites

- Python 3.10 or higher
- Conda (recommended) or pip
- Docker (optional, for containerized deployment)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pm-intern-recommender
   ```

2. **Create and activate conda environment**
   ```bash
   conda create -n InternProj python=3.10
   conda activate InternProj
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate sample data (optional - Docker does this automatically)**
   ```bash
   cd Recommender/dataset
   python script.py
   ```

5. **Train the model (optional - Docker does this automatically)**
   ```bash
   cd Recommender
   python train.py
   ```

6. **Start the API server**
   ```bash
   python main.py
   ```

**Note**: When using Docker, steps 4-5 are handled automatically. For manual setup, you can either run these steps or provide your own CSV files in the correct format.

### Docker Setup (Recommended)

The Docker container automatically handles all setup steps including data generation, model training, and API startup.

1. **Build and run with Docker**
   ```bash
   docker build -t razzat/internship_recommender .
   docker run -p 8000:8000 razzat/internship_recommender
   ```

2. **Using Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Using pre-built image from Docker Hub**
   ```bash
   docker run -p 8000:8000 razzat/internship_recommender
   ```

The Docker container will automatically:
- **Step 1**: Generate sample datasets (`script.py`)
- **Step 2**: Train the ML model (`train.py`) 
- **Step 3**: Start the FastAPI server on port 8000

### Manual Local Setup

If you prefer to run without Docker:

## API Documentation

### Base URL
```
http://localhost:8000
```

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

#### Health Check
```http
GET /health
```
Returns service status and model information.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-20T10:30:00",
  "model_loaded": true,
  "students_count": 1000,
  "internships_count": 2000
}
```

#### Get Students
```http
GET /students?limit=100
```
Returns list of all students in the system.

**Parameters:**
- `limit` (optional): Maximum number of students to return (default: 100)

#### Get Internships
```http
GET /internships?limit=100
```
Returns list of available internships.

**Parameters:**
- `limit` (optional): Maximum number of internships to return (default: 100)

#### Recommend for Existing Student
```http
POST /recommend/student/{student_id}?top_n=5
```
Get recommendations for a student by their ID.

**Parameters:**
- `student_id` (path): Student identifier
- `top_n` (optional): Number of recommendations to return (default: 5)

**Example:**
```bash
curl -X POST "http://localhost:8000/recommend/student/1?top_n=5"
```

#### Recommend for New Student
```http
POST /recommend/new-student?top_n=5
Content-Type: application/json

{
  "name": "John Doe",
  "skills": "python, machine learning, data science, sql"
}
```

**Parameters:**
- `top_n` (optional): Number of recommendations to return (default: 5)

**Example:**
```bash
curl -X POST "http://localhost:8000/recommend/new-student" \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "skills": "python, machine learning, data science"}'
```

#### Batch Recommendations
```http
POST /recommend/batch?top_n=5&limit=10
```
Get recommendations for multiple students.

**Parameters:**
- `top_n` (optional): Number of recommendations per student (default: 5)
- `limit` (optional): Maximum number of students to process (default: 10)

### Response Format

All recommendation endpoints return structured data including:
- Student information
- Ranked list of internship recommendations
- Similarity scores
- Internship details (title, company, domain, stipend, required skills)

**Example Recommendation Response:**
```json
{
  "student_id": 1,
  "student_name": "John Doe",
  "student_skills": ["python", "machine learning", "data science"],
  "recommendations": [
    {
      "rank": 1,
      "internship_id": 101,
      "internship_title": "Data Science Intern",
      "company": "Tech Corp",
      "similarity_score": 0.8636,
      "required_skills": "python, machine learning, tensorflow",
      "stipend": "25000",
      "domain": "Technology"
    },
    {
      "rank": 2,
      "internship_id": 102,
      "internship_title": "ML Engineer Intern",
      "company": "AI Solutions",
      "similarity_score": 0.7829,
      "required_skills": "python, scikit-learn, data analysis",
      "stipend": "30000",
      "domain": "Technology"
    }
  ],
  "total_recommendations": 5
}
```

### Testing the API

For detailed API testing examples and more comprehensive documentation, see `README_API.md`.

## Data Format

### Students Dataset (`students.csv`)
```csv
student_id,student_name,skills
1,John Doe,"python,machine learning,data analysis"
```

### Internships Dataset (`internships.csv`)
```csv
internship_id,internship_title,company,stipend,required_skills,domain
1,Data Analyst,Tech Corp,25000,"python,sql,statistics",Technology
```

## Development

### Project Structure
```
pm-intern-recommender/
├── main.py                 # FastAPI application
├── schemas.py             # Pydantic models
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── Recommender/          # ML components
│   ├── train.py         # Model training
│   ├── utils.py         # Utility functions
│   ├── recommend.py     # CLI tool
│   ├── dataset/         # Data files
│   └── model/           # Trained models
├── scripts/             # Helper scripts
└── analysis/           # Analysis notebooks
```

### Running Tests

The project includes a test script for API validation:
```bash
python test_api.py
```

### CLI Usage

The system includes a command-line interface for direct recommendations:
```bash
cd Recommender
python recommend.py
```

### Data Generation

The system includes an automated data generation script that creates realistic sample datasets:

```bash
cd Recommender/dataset
python script.py
```

This generates:
- `students.csv`: 1000 student profiles with diverse skill combinations
- `internships.csv`: 2000 internship opportunities across various domains

**Note**: Docker automatically runs this script, so manual execution is only needed for local development.

### Model Training

### Training Process

1. **Data Loading**: Reads student and internship datasets
2. **Text Preprocessing**: Cleans and normalizes skill descriptions
3. **Vectorization**: Creates TF-IDF vectors from skill text
4. **Model Training**: Trains k-nearest neighbors model
5. **Model Persistence**: Saves trained model and vectorizer

### Training Command
```bash
cd Recommender
python train.py
```

### Model Files
- `trained_model.pkl`: Serialized k-NN model
- `vectorizer.pkl`: TF-IDF vectorizer
- `processed_students.csv`: Preprocessed student data
- `processed_internships.csv`: Preprocessed internship data

## Configuration

### Environment Variables

- `PYTHONPATH`: Application path configuration
- `PYTHONUNBUFFERED`: Enable real-time logging
- `PORT`: API server port (default: 8000)

### API Configuration

The FastAPI application includes:
- CORS middleware for cross-origin requests
- Automatic OpenAPI documentation generation
- Request/response validation
- Error handling and logging

## Deployment

### Production Considerations

1. **Environment Setup**
   - Use production WSGI server (uvicorn with workers)
   - Configure environment variables
   - Set up monitoring and logging

2. **Security**
   - Enable HTTPS/TLS
   - Configure authentication if needed
   - Validate input data thoroughly

3. **Scaling**
   - Use load balancer for multiple instances
   - Consider model caching strategies
   - Monitor resource usage

### Docker Deployment

The Docker container provides a complete, self-contained deployment:

```bash
# Option 1: Build locally
docker build -t razzat/internship_recommender .
docker run -p 8000:8000 razzat/internship_recommender

# Option 2: Use pre-built image
docker run -p 8000:8000 razzat/internship_recommender

# Option 3: Docker Compose
docker-compose up --build
```

The container automatically executes the complete pipeline:
1. **Data Generation**: Creates sample datasets with 1000 students and 2000 internships
2. **Model Training**: Trains TF-IDF vectorizer and k-NN model
3. **API Startup**: Launches FastAPI server on port 8000

**Container Output Example**:
```
Step 1: Running data preprocessing script...
✅ Files generated: internships.csv, students.csv
Step 2: Training the model...
Training completed successfully!
Step 3: Starting FastAPI server...
INFO: Uvicorn running on http://0.0.0.0:8000
```

## Performance

### Optimization Strategies

- **Model Loading**: Models are loaded once at startup
- **Vectorization**: Reuses trained TF-IDF vectorizer
- **Caching**: In-memory storage of processed data
- **Batch Processing**: Efficient handling of multiple requests

### Resource Requirements

- **Memory**: 512MB minimum, 1GB recommended
- **CPU**: Single core sufficient for small datasets
- **Storage**: Minimal (models are typically < 50MB)

## Troubleshooting

### Common Issues

1. **Module Import Errors**
   - Ensure all dependencies are installed
   - Verify Python path configuration
   - Check virtual environment activation

2. **Model Loading Failures**
   - Verify model files exist in `Recommender/model/`
   - Check file permissions
   - Ensure training completed successfully

3. **Data File Errors**
   - Verify CSV files are in correct format
   - Check column names match expected schema
   - Ensure data files are accessible

4. **API Connection Issues**
   - Verify server is running on correct port
   - Check firewall settings
   - Ensure no port conflicts

### Debugging

Enable detailed logging by setting log level:
```python
logging.basicConfig(level=logging.DEBUG)
```

Check application logs for detailed error information.

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make changes and test thoroughly
4. Submit a pull request

### Code Standards

- Follow PEP 8 style guidelines
- Add type hints where appropriate
- Include docstrings for functions and classes
- Write unit tests for new features

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For issues, questions, or contributions:
- Create an issue in the repository
- Review existing documentation
- Check the troubleshooting section

## Acknowledgments

Built with FastAPI, scikit-learn, and other open-source technologies that make machine learning accessible and scalable.