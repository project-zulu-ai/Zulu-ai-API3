from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(
    title="Zulu AI - App Generator API",
    description="Generate app starter code from ideas",
    version="1.0.0"
)

class AppIdeaRequest(BaseModel):
    idea: str

class AppGeneratorResponse(BaseModel):
    frontend: Dict[str, str]
    backend: Dict[str, str]
    readme: str

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Zulu AI App Generator API is running"}

@app.post("/generate_app", response_model=AppGeneratorResponse)
async def generate_app(request: AppIdeaRequest):
    """
    Generate app starter code based on user idea
    
    Args:
        request: AppIdeaRequest containing the app idea
        
    Returns:
        AppGeneratorResponse with generated code files
    """
    # Validate input
    if not request.idea or len(request.idea.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="App idea cannot be empty"
        )
    
    idea = request.idea.strip()
    
    # Generate placeholder code
    frontend_files = {
        "App.js": "// React code placeholder"
    }
    
    backend_files = {
        "main.py": "# FastAPI backend placeholder"
    }
    
    readme_content = f"# {idea}\n\nGenerated app starter by Zulu AI"
    
    return AppGeneratorResponse(
        frontend=frontend_files,
        backend=backend_files,
        readme=readme_content
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)