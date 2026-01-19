from fastapi import APIRouter, HTTPException, status
from typing import Optional
import uuid

from Schemas.StudentDetails import StudentDetails
from Schemas.StudentRecommendation import StudentRecommendation
from Services.RecommendationService import recommend_for_student

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.post("/", response_model=StudentRecommendation, status_code=status.HTTP_200_OK)
async def get_recommendations(student: StudentDetails, top_k: Optional[int] = 5):
    """
    Get internship recommendations for a student based on their skills and domain.
    
    Args:
        student: Student details including name, skills and domain
        top_k: Number of top recommendations to return (default: 5)
        
    Returns:
        StudentRecommendation object with ranked internship recommendations
    """
    try:
        if top_k < 1 or top_k > 20:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="top_k must be between 1 and 20"
            )
        
        # Auto-generate a student ID for this request (no persistence)
        student.student_id = str(uuid.uuid4())[:8].upper()
        
        recommendations = recommend_for_student(student, top_k=top_k)
        return recommendations
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating recommendations: {str(e)}"
        )


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint for the recommendation service."""
    return {"status": "healthy", "service": "recommendation"}
