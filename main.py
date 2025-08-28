from fastapi import FastAPI, HTTPException
from models import AppIdea
from code_generator import generate_app

app = FastAPI(
    title="Zulu AI - App Generator API",
    description="Generate app starter code from ideas",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Zulu AI App Generator API is running"}

@app.post("/generate_app")
async def generate_app_endpoint(app_idea: AppIdea):
    """
    Generate app starter code based on user idea
    
    Args:
        app_idea: AppIdea model containing the app idea
        
    Returns:
        Dictionary with file paths and code content
    """
    # Validate input
    if not app_idea.idea or len(app_idea.idea.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="App idea cannot be empty"
        )
    
    try:
        # Generate the app files
        generated_files = generate_app(app_idea.idea.strip())
        return generated_files
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate app: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)