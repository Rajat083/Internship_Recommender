"""
PM Intern Recommender - FastAPI Web Service
==========================================

A RESTful web service for the PM Intern Recommender system.
Provides endpoints for getting internship recommendations for students.

Endpoints:
- GET /health - Health check
- POST /recommend/student/{student_id} - Get recommendations for existing student
- POST /recommend/new-student - Get recommendations for new student with custom skills
- POST /recommend/batch - Get recommendations for all students
- GET /students - List all students
- GET /internships - List all internships
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from typing import List, Optional, Dict, Any
import pickle
import os
from datetime import datetime

# Import our utility functions
from Recommender.utils import (
    load_trained_model_and_data, process_skills_for_prediction,
    create_student_vectors, clean_skills, create_recommendations,
    display_sample_recommendations, display_single_recommendation
)

# Import Pydantic models for request/response validation
from schemas import (
    StudentRecommendationResponse, NewStudentRequest, NewStudentResponse,
    BatchRecommendationResponse, HealthResponse, StudentInfo, InternshipInfo,
    ErrorResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="PM Intern Recommender API",
    description="RESTful API for internship recommendations using ML-based skill matching",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables to store loaded model and data
model = None
vectorizer = None
students_df = None
internships_df = None
stu_skills = None
int_reqs = None

@app.on_event("startup")
async def startup_event():
    """Load model and data when the application starts"""
    global model, vectorizer, students_df, internships_df, stu_skills, int_reqs
    
    logger.info("Loading model and data...")
    try:
        model, vectorizer, students_df, internships_df = load_trained_model_and_data()
        if model is None:
            raise Exception("Failed to load model and data")
        
        # Process skills for prediction
        stu_skills, int_reqs = process_skills_for_prediction(students_df, internships_df)
        
        logger.info("Model and data loaded successfully!")
        logger.info(f"Loaded {len(students_df)} students and {len(internships_df)} internships")
        
    except Exception as e:
        logger.error(f"Error loading model and data: {e}")
        raise e

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        model_loaded=model is not None,
        students_count=len(students_df) if students_df is not None else 0,
        internships_count=len(internships_df) if internships_df is not None else 0
    )

@app.get("/students", response_model=List[StudentInfo])
async def get_students(limit: Optional[int] = 100):
    """Get list of students"""
    if students_df is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    students_limited = students_df.head(limit)
    return [
        StudentInfo(
            student_id=row['student_id'],
            student_name=row['student_name'],
            skills=stu_skills.get(row['student_id'], []),
            primary_domain=row.get('primary_domain', '')
        )
        for _, row in students_limited.iterrows()
    ]

@app.get("/internships", response_model=List[InternshipInfo])
async def get_internships(limit: Optional[int] = 100):
    """Get list of internships"""
    if internships_df is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    internships_limited = internships_df.head(limit)
    return [
        InternshipInfo(
            internship_id=row['internship_id'],
            internship_title=row['internship_title'],
            company=row['company'],
            required_skills=row['required_skills'],
            stipend=str(row.get('stipend', '')),
            domain=str(row.get('domain', ''))
        )
        for _, row in internships_limited.iterrows()
    ]

@app.post("/recommend/student/{student_id}", response_model=StudentRecommendationResponse)
async def recommend_for_student(student_id: int, top_n: Optional[int] = 5):
    """Get recommendations for an existing student by ID"""
    if model is None or vectorizer is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    if student_id not in stu_skills:
        raise HTTPException(status_code=404, detail=f"Student ID {student_id} not found")
    
    try:
        # Get student info
        student_info = students_df[students_df['student_id'] == student_id].iloc[0]
        student_skills_list = stu_skills[student_id]
        
        # Create vector for this student
        student_skills_text = ' '.join(student_skills_list)
        student_vector = vectorizer.transform([student_skills_text])
        
        # Get recommendations
        distances, indices = model.kneighbors(student_vector)
        
        # Process results
        internship_ids = list(internships_df['internship_id'])
        recommended_internships = []
        
        for j, (dist, idx) in enumerate(zip(distances[0][:top_n], indices[0][:top_n])):
            internship_id = internship_ids[idx]
            internship_info = internships_df[internships_df['internship_id'] == internship_id].iloc[0]
            similarity_score = 1 - dist
            
            recommended_internships.append({
                'rank': j + 1,
                'internship_id': internship_id,
                'internship_title': internship_info['internship_title'],
                'company': internship_info['company'],
                'similarity_score': round(float(similarity_score), 4),
                'required_skills': internship_info['required_skills'],
                'stipend': str(internship_info.get('stipend', '')),
                'domain': str(internship_info.get('domain', ''))
            })
        
        return StudentRecommendationResponse(
            student_id=student_id,
            student_name=student_info['student_name'],
            student_skills=student_skills_list,
            recommendations=recommended_internships,
            total_recommendations=len(recommended_internships)
        )
        
    except Exception as e:
        logger.error(f"Error getting recommendations for student {student_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommend/new-student", response_model=NewStudentResponse)
async def recommend_for_new_student(request: NewStudentRequest, top_n: Optional[int] = 5):
    """Get recommendations for a new student with custom skills"""
    if model is None or vectorizer is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Clean and process the skills
        cleaned_skills = clean_skills(request.skills.lower())
        skills_list = [skill.strip() for skill in cleaned_skills.split(',') if skill.strip()]
        
        if not skills_list:
            raise HTTPException(status_code=400, detail="No valid skills provided")
        
        # Create vector for the new student
        student_vector = vectorizer.transform([cleaned_skills])
        
        # Get recommendations
        distances, indices = model.kneighbors(student_vector)
        
        # Process results
        internship_ids = list(internships_df['internship_id'])
        recommended_internships = []
        
        for j, (dist, idx) in enumerate(zip(distances[0][:top_n], indices[0][:top_n])):
            internship_id = internship_ids[idx]
            internship_info = internships_df[internships_df['internship_id'] == internship_id].iloc[0]
            similarity_score = 1 - dist
            
            recommended_internships.append({
                'rank': j + 1,
                'internship_id': internship_id,
                'internship_title': internship_info['internship_title'],
                'company': internship_info['company'],
                'similarity_score': round(float(similarity_score), 4),
                'required_skills': internship_info['required_skills'],
                'stipend': str(internship_info.get('stipend', '')),
                'domain': str(internship_info.get('domain', ''))
            })
        
        return NewStudentResponse(
            student_name=request.name,
            student_skills=skills_list,
            recommendations=recommended_internships,
            total_recommendations=len(recommended_internships)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting recommendations for new student: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommend/batch", response_model=BatchRecommendationResponse)
async def recommend_batch(background_tasks: BackgroundTasks, top_n: Optional[int] = 5, limit: Optional[int] = 10):
    """Get recommendations for multiple students (limited for performance)"""
    if model is None or vectorizer is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Limit the number of students for performance
        limited_students = students_df.head(limit)
        limited_stu_skills = {
            sid: skills for sid, skills in stu_skills.items() 
            if sid in limited_students['student_id'].values
        }
        
        # Create vectors for limited students
        X = create_student_vectors(limited_stu_skills, vectorizer)
        
        # Get recommendations
        all_recommendations = create_recommendations(
            model, X, limited_students, internships_df, limited_stu_skills, top_n
        )
        
        # Convert to API response format
        batch_results = []
        for student_id, data in all_recommendations.items():
            student_result = {
                'student_id': student_id,
                'student_name': data['student_name'],
                'student_skills': data['student_skills'],
                'recommendations': [
                    {
                        'rank': rec['rank'],
                        'internship_id': rec['internship_id'],
                        'internship_title': internships_df[internships_df['internship_id'] == rec['internship_id']]['internship_title'].iloc[0],
                        'company': rec['company'],
                        'similarity_score': round(rec['similarity_score'], 4),
                        'required_skills': rec['required_skills'],
                        'stipend': str(internships_df[internships_df['internship_id'] == rec['internship_id']]['stipend'].iloc[0]),
                        'domain': str(internships_df[internships_df['internship_id'] == rec['internship_id']]['domain'].iloc[0])
                    }
                    for rec in data['internships']
                ]
            }
            batch_results.append(student_result)
        
        return BatchRecommendationResponse(
            total_students=len(batch_results),
            recommendations=batch_results
        )
        
    except Exception as e:
        logger.error(f"Error getting batch recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content=ErrorResponse(error="Not Found", message="The requested resource was not found").dict()
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(error="Internal Server Error", message="An internal error occurred").dict()
    )

if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )