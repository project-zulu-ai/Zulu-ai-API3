from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class AppIdeaRequest(BaseModel):
    """Request model for app idea input"""
    idea: str = Field(
        ..., 
        min_length=5, 
        max_length=1000,
        description="Description of the app idea (5-1000 characters)"
    )
    complexity: Optional[str] = Field(
        default="simple",
        description="App complexity level: simple, medium, or complex"
    )

class GeneratedFile(BaseModel):
    """Model representing a generated code file"""
    path: str = Field(..., description="File path relative to project root")
    content: str = Field(..., description="File content")
    file_type: str = Field(..., description="Type of file (python, javascript, html, markdown)")

class GeneratedAppResponse(BaseModel):
    """Response model for generated app code"""
    success: bool = Field(..., description="Whether the generation was successful")
    message: str = Field(..., description="Status message")
    files: List[GeneratedFile] = Field(..., description="List of generated files")
    structure: Optional[Dict] = Field(
        default=None,
        description="Directory structure overview"
    )

class AppMetadata(BaseModel):
    """Metadata extracted from app idea"""
    app_name: str
    app_type: str  # todo, blog, ecommerce, etc.
    frontend_type: str  # react, html
    features: List[str]
    database_needed: bool
    api_endpoints: List[str]
