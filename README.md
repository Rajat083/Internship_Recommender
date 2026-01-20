# Internship Recommender System

Live app: https://internship-recommender-3k5v.vercel.app/

This project recommends internships based on student skills and domain using TF-IDF vectorization and FAISS vector search. Backend is FastAPI; frontend is React + Vite.

## Tech Stack
- FastAPI, Uvicorn
- PostgreSQL (psycopg2-binary)
- FAISS, scikit-learn, numpy, pandas
- Pydantic, python-dotenv
- React, Vite, Axios, Tailwind CSS

## Quick Start

### Backend
```
cd app
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # macOS/Linux
pip install -r requirements.txt
```

Create `app/.env`:
```
DB_HOST=your-host
DB_PORT=5432
DB_DATABASE=your-db
DB_USER=your-user
DB_PASSWORD=your-password
MODEL_PATH=Constants/trained_model.pkl
VECTORIZER_PATH=Constants/vectorizer.pkl
ALLOWED_ORIGINS=https://internship-recommender-3k5v.vercel.app,http://localhost:3000
PORT=8000
```

Run backend:
```
cd app
python main.py
```
API: http://localhost:8000, Docs: http://localhost:8000/docs

### Frontend
```
cd frontend
npm install
```

Create `frontend/.env.local`:
```
VITE_API_BASE_URL=http://localhost:8000
```

Run frontend:
```
cd frontend
npm run dev
```
App: http://localhost:3000

## API
- POST /recommendations/?top_k=5 — body: {"name": "John", "skills": ["python"], "domain": "data"}
- GET /health

## Deployment
- Backend: Render (uses render.yaml), set env vars above.
- Frontend: Vercel, set VITE_API_BASE_URL to your backend URL.

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
