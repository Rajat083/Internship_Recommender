import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from DB.VectorDB.BuildIndex import ensure_index_built

from Routes.recommendations import router as recommendations_router

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Internship Recommender API",
    description="API for recommending internships to students based on skills and domain using vector search",
    version="2.0.0",
)

# CORS middleware - Allow only specific origins for production
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000"  # Default for local development
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(recommendations_router)


@app.on_event("startup")
def _startup_build_index():
    """Ensure FAISS index is built at application startup."""
    try:
        ensure_index_built()
    except Exception as e:
        # Fail fast so the API doesn't run without a usable index
        print(f"[startup] Error ensuring FAISS index: {e}")
        raise


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Internship Recommender API",
        "version": "2.0.0",
        "description": "Vector-based semantic search for internship recommendations"
    }


@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
