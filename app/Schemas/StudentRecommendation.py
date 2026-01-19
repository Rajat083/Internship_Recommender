from pydantic import BaseModel, Field
from typing import Annotated


class RecommendationResponse(BaseModel):
    rank: Annotated[int, Field(..., description="Rank of the recommended course")]
    internship_id: Annotated[str, Field(..., description="Unique identifier for the internship")]
    internship_title: Annotated[str, Field(..., description="Title of the internship")]
    company: Annotated[str, Field(..., description="Company offering the internship")]
    similarity_score: Annotated[float, Field(..., description="Similarity score between student skills and internship requirements")]
    required_skills: Annotated[list[str], Field(..., description="List of skills required for the internship")]
    stipend: Annotated[float, Field(..., description="Stipend offered for the internship")]
    domain: Annotated[str, Field(..., description="Domain of the internship")]
    

class StudentRecommendation(BaseModel):
    student_id: Annotated[str, Field(..., description="Unique identifier for the student")]
    
    student_name: Annotated[str, Field(..., description="Full name of the student")]
    student_skills: Annotated[list[str], Field(..., description="List of skills possessed by the student")]
    
    recommendatons: Annotated[list[RecommendationResponse], Field(..., description="List of recommended courses for the student")]
    
    total_recommendations: Annotated[int, Field(..., description="Total number of recommended courses")]
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "student_id": "1",
                "student_name": "John Doe",
                "student_skills": ["python", "machine learning", "data science"],
                "recommendatons": [
                    {
                        "rank": 1,
                        "internship_id": "101",
                        "internship_title": "Data Science Intern",
                        "company": "Tech Corp",
                        "similarity_score": 0.8636,
                        "required_skills": ["python", "machine learning", "tensorflow"],
                        "stipend": 25000.0,
                        "domain": "Technology"
                    },
                    {
                        "rank": 2,
                        "internship_id": "102",
                        "internship_title": "ML Engineer Intern",
                        "company": "AI Solutions",
                        "similarity_score": 0.7829,
                        "required_skills": ["python", "scikit-learn", "data analysis"],
                        "stipend": 30000.0,
                        "domain": "Technology"
                    }
                ],
                "total_recommendations": 5
            }
        }
    }
