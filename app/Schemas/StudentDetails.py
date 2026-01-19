from pydantic import BaseModel, Field
from typing import Annotated, Optional

class StudentDetails(BaseModel):
    student_id: Annotated[Optional[str], Field(None, description="Unique identifier for the student")] = None
    name: Annotated[str, Field(..., description="Full name of the student")]
    skills: Annotated[list[str], Field(..., description="List of skills possessed by the student")] 
    domain: Annotated[str, Field(..., description="Domain of interest for the student")]
    

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Jane Doe",
                "skills": ["Python", "Data Analysis", "Machine Learning"],
                "domain": "Data Science"
            }
        }
    }