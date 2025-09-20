"""
PM Intern Recommender - Pydantic Schemas
=======================================

Pydantic models for request/response validation and API documentation.
These schemas define the structure of data exchanged through the API.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(..., description="Current timestamp")
    model_loaded: bool = Field(..., description="Whether the ML model is loaded")
    students_count: int = Field(..., description="Number of students in database")
    internships_count: int = Field(..., description="Number of internships in database")


class StudentInfo(BaseModel):
    """Student information"""
    student_id: int = Field(..., description="Unique student identifier")
    student_name: str = Field(..., description="Student name")
    skills: List[str] = Field(..., description="List of student skills")
    primary_domain: str = Field("", description="Primary domain/field of study")


class InternshipInfo(BaseModel):
    """Internship information"""
    internship_id: int = Field(..., description="Unique internship identifier")
    internship_title: str = Field(..., description="Internship title/position")
    company: str = Field(..., description="Company name")
    required_skills: str = Field(..., description="Required skills for the internship")
    domain: str = Field("", description="Internship domain/field")
    stipend: str = Field("", description="Internship stipend/salary")


class RecommendationItem(BaseModel):
    """Individual recommendation item"""
    rank: int = Field(..., description="Recommendation rank (1 is best match)")
    internship_id: int = Field(..., description="Internship identifier")
    internship_title: str = Field(..., description="Internship title/position")
    company: str = Field(..., description="Company name")
    similarity_score: float = Field(..., description="Similarity score (0-1, higher is better)")
    required_skills: str = Field(..., description="Required skills for the internship")
    domain: Optional[str] = Field("", description="Internship domain/field")
    stipend: Optional[str] = Field("", description="Internship stipend/salary")


class StudentRecommendationResponse(BaseModel):
    """Response for student-specific recommendations"""
    student_id: int = Field(..., description="Student identifier")
    student_name: str = Field(..., description="Student name")
    student_skills: List[str] = Field(..., description="Student's skills")
    recommendations: List[RecommendationItem] = Field(..., description="List of recommended internships")
    total_recommendations: int = Field(..., description="Total number of recommendations")


class NewStudentRequest(BaseModel):
    """Request for new student recommendations"""
    name: str = Field(..., description="Student name", min_length=1, max_length=100)
    skills: str = Field(..., description="Comma-separated list of skills", min_length=1)
    
    @validator('skills')
    def validate_skills(cls, v):
        if not v.strip():
            raise ValueError('Skills cannot be empty')
        return v.strip()
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "skills": "python, machine learning, data science, sql"
            }
        }


class NewStudentResponse(BaseModel):
    """Response for new student recommendations"""
    student_name: str = Field(..., description="Student name")
    student_skills: List[str] = Field(..., description="Processed student skills")
    recommendations: List[RecommendationItem] = Field(..., description="List of recommended internships")
    total_recommendations: int = Field(..., description="Total number of recommendations")


class BatchStudentRecommendation(BaseModel):
    """Individual student recommendation in batch response"""
    student_id: int = Field(..., description="Student identifier")
    student_name: str = Field(..., description="Student name")
    student_skills: List[str] = Field(..., description="Student's skills")
    recommendations: List[RecommendationItem] = Field(..., description="List of recommended internships")


class BatchRecommendationResponse(BaseModel):
    """Response for batch recommendations"""
    total_students: int = Field(..., description="Total number of students processed")
    recommendations: List[BatchStudentRecommendation] = Field(..., description="Recommendations for each student")


class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="Error timestamp")

    class Config:
        schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Invalid input data",
                "timestamp": "2025-09-19T10:30:00"
            }
        }


class RecommendationStats(BaseModel):
    """Statistics about recommendations"""
    avg_similarity_score: float = Field(..., description="Average similarity score")
    min_similarity_score: float = Field(..., description="Minimum similarity score")
    max_similarity_score: float = Field(..., description="Maximum similarity score")
    top_companies: List[str] = Field(..., description="Most recommended companies")


class BatchRequestParams(BaseModel):
    """Parameters for batch recommendation requests"""
    top_n: int = Field(5, description="Number of recommendations per student", ge=1, le=20)
    limit: int = Field(10, description="Maximum number of students to process", ge=1, le=100)
    include_stats: bool = Field(False, description="Whether to include recommendation statistics")