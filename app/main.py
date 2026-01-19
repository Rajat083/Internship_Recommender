from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Routes.recommendations import router as recommendations_router

app = FastAPI(
    title="Internship Recommender API",
    description="API for recommending internships to students based on skills and domain using vector search",
    version="2.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(recommendations_router)


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
    uvicorn.run(app, host="0.0.0.0", port=8000)
