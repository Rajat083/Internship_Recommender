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

4. **Prepare data**
   - Place `students.csv` and `internships.csv` in `Recommender/dataset/`
   - Ensure the CSV files contain the required columns

5. **Train the model**
   ```bash
   cd Recommender
   python train.py
   ```

6. **Start the API server**
   ```bash
   python main.py
   ```

### Docker Setup

1. **Using Docker Compose (Recommended)**
   ```bash
   docker-compose up --build
   ```

2. **Using Docker commands**
   ```bash
   docker build -t pm-intern-recommender .
   docker run -d -p 8000:8000 pm-intern-recommender
   ```

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

#### Get Students
```http
GET /students
```
Returns list of all students in the system.

#### Get Internships
```http
GET /internships?limit=100
```
Returns list of available internships.

#### Recommend for Existing Student
```http
POST /recommend/student/{student_id}?top_n=5
```
Get recommendations for a student by their ID.

#### Recommend for New Student
```http
POST /recommend/new-student?top_n=5
Content-Type: application/json

{
  "name": "John Doe",
  "skills": "python, machine learning, data science, sql"
}
```

#### Batch Recommendations
```http
POST /recommend/batch?top_n=5&limit=10
```
Get recommendations for multiple students.

### Response Format

All recommendation endpoints return structured data including:
- Student information
- Ranked list of internship recommendations
- Similarity scores
- Internship details (title, company, domain, stipend, required skills)

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

## Model Training

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

See `DOCKER.md` for comprehensive Docker deployment instructions.

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