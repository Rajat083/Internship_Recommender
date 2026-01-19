# 🎓 Internship Recommender System

A FastAPI-based recommendation system that matches students with relevant internships using semantic search powered by TF-IDF vectorization and FAISS vector database.

## 🚀 Features

- **Semantic Search**: Uses TF-IDF vectorization and FAISS for efficient similarity search
- **Vector Database**: Fast retrieval from 1500+ internships using cosine similarity
- **RESTful API**: Built with FastAPI for high performance and auto-generated documentation
- **Supabase Integration**: Cloud PostgreSQL database for internship and student data
- **Automatic Training**: Vectorizer auto-trains from database when missing
- **Environment-based Config**: Secure credential management with `.env`

## 📋 Prerequisites

- Python 3.10+
- Conda (recommended) or virtualenv
- Internet connection for Supabase database access

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Temp
```

### 2. Create Conda Environment
```bash
conda create -n InternProj python=3.10
conda activate InternProj
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn psycopg2-binary python-dotenv
pip install scikit-learn numpy faiss-cpu pydantic
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
# Database Configuration
DB_HOST=your-supabase-host
DB_DATABASE=postgres
DB_USER=postgres
DB_PASSWORD=your-password
DB_PORT=5432

# Model Paths
MODEL_PATH=Constants/trained_model.pkl
VECTORIZER_PATH=Constants/vectorizer.pkl

# Vector DB Paths
FAISS_INDEX_PATH=DB/vectordb/faiss.index
INTERNSHIP_IDS_PATH=DB/vectordb/internship_ids.npy

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

### 5. Initialize the Project
```bash
python setup_project.py
```

This will:
- ✅ Verify database connection
- 📊 Train TF-IDF vectorizer on internship data
- 🔨 Build FAISS vector index
- ✅ Validate setup

## 🚦 Usage

### Start the API Server
```bash
python main.py
```

Or with auto-reload for development:
```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

### Interactive API Documentation
Visit `http://localhost:8000/docs` for Swagger UI documentation.

### Example API Request

**Endpoint**: `POST /recommendations/`

**Request Body**:
```json
{
  "student_id": "12345",
  "name": "Jane Doe",
  "skills": ["Python", "Machine Learning", "Data Science"],
  "domain": "Data Science"
}
```

**Response**:
```json
{
  "student_id": "12345",
  "student_name": "Jane Doe",
  "student_skills": ["Python", "Machine Learning", "Data Science"],
  "recommendatons": [
    {
      "rank": 1,
      "internship_id": "101",
      "internship_title": "Data Science Intern",
      "company": "Tech Corp",
      "similarity_score": 0.8636,
      "required_skills": ["Python", "Machine Learning", "TensorFlow"],
      "stipend": 25000.0,
      "domain": "Technology"
    }
  ],
  "total_recommendations": 5
}
```

### Using cURL
```bash
curl -X POST "http://localhost:8000/recommendations/" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "123",
    "name": "John Doe",
    "skills": ["Python", "Data Analysis"],
    "domain": "Data Science"
  }'
```

## 📁 Project Structure

```
.
├── Constants/
│   ├── config.py              # Configuration management
│   └── vectorizer.pkl         # Trained TF-IDF vectorizer
├── DB/
│   ├── Postgres.py            # Database connection utilities
│   └── VectorDB/
│       ├── BuildIndex.py      # FAISS index builder
│       ├── Search.py          # Vector search functions
│       └── vectordb/          # FAISS index storage
├── RecommenderModel/
│   ├── Recommender.py         # Recommendation logic
│   └── Vectorizer.py          # TF-IDF vectorizer management
├── Routes/
│   └── recommendations.py     # FastAPI route handlers
├── Schemas/
│   ├── StudentDetails.py      # Request schema
│   └── StudentRecommendation.py # Response schema
├── Services/
│   └── RecommendationService.py # Business logic
├── main.py                    # FastAPI application entry point
├── setup_project.py           # One-time setup script
├── .env                       # Environment variables (gitignored)
└── README.md
```

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint with API info |
| GET | `/health` | Health check |
| POST | `/recommendations/` | Get internship recommendations |
| GET | `/recommendations/health` | Recommendation service health |

## 🧪 Testing

Test the health endpoint:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

## 🔄 Rebuilding the Index

If internship data changes in the database:

```bash
python -c "from DB.VectorDB.BuildIndex import build_index; build_index()"
```

Or retrain the vectorizer:

```bash
python -c "from RecommenderModel.Vectorizer import train_and_save_vectorizer; train_and_save_vectorizer(force=True)"
```

## 📊 Database Schema

### Internships Table
```sql
CREATE TABLE internships (
    internship_id SERIAL PRIMARY KEY,
    internship_title VARCHAR(255),
    company VARCHAR(255),
    domain VARCHAR(100),
    required_skills TEXT,
    stipend NUMERIC,
    is_active BOOLEAN DEFAULT TRUE
);
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Troubleshooting

### Database Connection Issues
- Verify `.env` credentials are correct
- Check internet connectivity
- Ensure Supabase instance is active

### FAISS Index Not Found
Run the setup script:
```bash
python setup_project.py
```

### Import Errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## 📝 License

This project is licensed under the MIT License.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- FAISS for efficient similarity search
- Supabase for managed PostgreSQL hosting
- scikit-learn for TF-IDF implementation
