# 🎓 Internship Recommender System

A full-stack web application that intelligently matches students with relevant internships using semantic search powered by TF-IDF vectorization and FAISS vector database. Built with FastAPI backend and React frontend.

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![React](https://img.shields.io/badge/react-18+-61DAFB.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)

## 🌟 Features

### Backend
- **Semantic Search**: TF-IDF vectorization with FAISS for efficient similarity matching
- **Vector Database**: Fast retrieval from 1500+ internships using cosine similarity
- **RESTful API**: High-performance FastAPI with auto-generated documentation
- **Cloud Database**: Supabase (PostgreSQL) integration for internship data
- **Auto-Training**: Vectorizer automatically trains from database when missing

### Frontend
- **Modern UI**: React 18 with Tailwind CSS for responsive design
- **Real-time Recommendations**: Instant feedback with loading states
- **Student Input Form**: Skills-based input with validation
- **Detailed Results**: Ranked recommendations with similarity scores
- **Error Handling**: Comprehensive error messages and fallbacks

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │  (Port 3000)
│   Tailwind CSS  │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│  FastAPI Backend│  (Port 8000)
│   + CORS        │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────────┐
│ FAISS  │ │  Supabase    │
│ Vector │ │  PostgreSQL  │
│   DB   │ │  (Cloud DB)  │
└────────┘ └──────────────┘
```

## 📋 Prerequisites

- **Python**: 3.10 or higher
- **Node.js**: 18 or higher
- **npm**: 9 or higher
- **Git**: For version control
- **Internet**: For Supabase database access

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Rajat083/Internship_Recommender.git
cd Internship_Recommender
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
cd app
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Configure Environment Variables
Create `.env` file in the `app` directory:
```env
# Database Configuration
DB_HOST=your-supabase-host.supabase.co
DB_DATABASE=postgres
DB_USER=postgres
DB_PASSWORD=your-password
DB_PORT=5432

# Model Paths
MODEL_PATH=Constants/trained_model.pkl
VECTORIZER_PATH=Constants/vectorizer.pkl

# Vector DB Paths
FAISS_INDEX_PATH=DB/VectorDB/faiss.index
INTERNSHIP_IDS_PATH=DB/VectorDB/internship_ids.npy

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

#### Start Backend Server
```bash
python main.py
```

Backend will run at: `http://localhost:8000`

### 3. Frontend Setup

#### Install Dependencies
```bash
cd frontend
npm install
```

#### Configure Environment (Optional)
Create `.env` file in the `frontend` directory:
```env
VITE_API_BASE_URL=http://localhost:8000
```

#### Start Development Server
```bash
npm run dev
```

Frontend will run at: `http://localhost:3000`

## 📁 Project Structure

```
Internship_Recommender/
├── app/                          # Backend (FastAPI)
│   ├── .env                      # Environment variables
│   ├── main.py                   # FastAPI application entry point
│   ├── requirements.txt          # Python dependencies
│   ├── Constants/                
│   │   ├── config.py             # Configuration management
│   │   ├── trained_model.pkl     # Trained ML model (generated)
│   │   └── vectorizer.pkl        # TF-IDF vectorizer (generated)
│   ├── DB/
│   │   ├── Postgres.py           # PostgreSQL connection
│   │   └── VectorDB/
│   │       ├── BuildIndex.py     # FAISS index builder
│   │       ├── Search.py         # Vector search implementation
│   │       ├── faiss.index       # FAISS index file (generated)
│   │       └── internship_ids.npy # Internship ID mappings
│   ├── RecommenderModel/
│   │   ├── Recommender.py        # Core recommendation logic
│   │   └── Vectorizer.py         # TF-IDF vectorization
│   ├── Routes/
│   │   └── recommendations.py    # API endpoints
│   ├── Schemas/
│   │   ├── StudentDetails.py     # Student input schema
│   │   └── StudentRecommendation.py # Response schemas
│   └── Services/
│       └── RecommendationService.py # Business logic
│
└── frontend/                     # Frontend (React + Vite)
    ├── public/                   # Static assets
    ├── src/
    │   ├── components/           # React components
    │   │   ├── RecommendationForm.jsx
    │   │   └── RecommendationResults.jsx
    │   ├── pages/
    │   │   └── Home.jsx          # Main page
    │   ├── services/
    │   │   └── api.js            # API client (Axios)
    │   ├── App.jsx               # Root component
    │   ├── main.jsx              # Entry point
    │   └── index.css             # Tailwind styles
    ├── package.json              # Node dependencies
    ├── vite.config.js            # Vite configuration
    └── tailwind.config.js        # Tailwind configuration
```

## 🔌 API Documentation

### Endpoints

#### `POST /recommendations/`
Get personalized internship recommendations.

**Request Body:**
```json
{
  "name": "John Doe",
  "skills": ["Python", "Machine Learning", "Django"],
  "domain": "Data Science"
}
```

**Query Parameters:**
- `top_k` (optional): Number of recommendations (default: 5)

**Response:**
```json
{
  "student_id": "A1B2C3D4",
  "student_name": "John Doe",
  "student_skills": ["Python", "Machine Learning", "Django"],
  "recommendatons": [
    {
      "rank": 1,
      "internship_id": "123",
      "internship_title": "ML Intern",
      "company": "Tech Corp",
      "domain": "Data Science",
      "required_skills": ["Python", "Machine Learning", "TensorFlow"],
      "stipend": 15000,
      "similarity_score": 0.89
    }
  ],
  "total_recommendations": 5
}
```

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

### Interactive Documentation
Visit `http://localhost:8000/docs` for Swagger UI.

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server
- **PostgreSQL**: Database (Supabase)
- **FAISS**: Vector similarity search
- **scikit-learn**: TF-IDF vectorization
- **Pydantic**: Data validation
- **python-dotenv**: Environment management

### Frontend
- **React 18**: UI library
- **Vite**: Build tool
- **Tailwind CSS**: Utility-first CSS
- **Axios**: HTTP client
- **JavaScript (JSX)**: Programming language

## 🧪 Development

### Backend Development
```bash
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Build Frontend for Production
```bash
cd frontend
npm run build
```

### Lint Frontend Code
```bash
cd frontend
npm run lint
```

## 🚢 Deployment

### Docker Deployment (Recommended)

#### Backend Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend Dockerfile
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  backend:
    build: ./app
    ports:
      - "8000:8000"
    env_file:
      - ./app/.env
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    restart: unless-stopped
```

### Cloud Deployment Options

- **Backend**: Render, Railway, Heroku, AWS EC2, Google Cloud Run
- **Frontend**: Vercel, Netlify, AWS S3 + CloudFront, GitHub Pages
- **Database**: Supabase (already configured)

## 🐛 Troubleshooting

### Backend Issues

**FAISS index not found:**
```bash
cd app
python DB/VectorDB/BuildIndex.py
```

**Database connection failed:**
- Verify `.env` credentials
- Check Supabase project status
- Ensure IP is whitelisted in Supabase

**Module import errors:**
```bash
pip install -r requirements.txt
```

### Frontend Issues

**API connection failed:**
- Verify backend is running on port 8000
- Check CORS configuration in backend
- Verify `VITE_API_BASE_URL` in frontend `.env`

**Tailwind styles not working:**
```bash
npm install
npm run dev
```

**Build errors:**
```bash
rm -rf node_modules package-lock.json
npm install
```

## 📊 Performance

- **Search Speed**: < 50ms for 1500+ internships
- **API Response Time**: < 200ms average
- **Frontend Load Time**: < 2s initial load
- **Accuracy**: Cosine similarity-based ranking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Rajat083**
- GitHub: [@Rajat083](https://github.com/Rajat083)

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Supabase for cloud PostgreSQL hosting
- FAISS for efficient vector search
- Tailwind CSS for the styling system
- React team for the frontend library

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review API docs at `/docs` endpoint

---

**⭐ Star this repository if you find it helpful!**
