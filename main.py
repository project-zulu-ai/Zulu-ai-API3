from fastapi import FastAPI, HTTPException
from models import AppIdea
from code_generator import generate_app
from agent_action import save_files_and_push
from utils.git_helper import git_workflow
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Zulu AI - App Generator API",
    description="Generate app starter code from ideas, save files, and push to GitHub",
    version="1.0.0"
)

# Repository URL
repo_url = "https://github.com/project-zulu-ai/Zulu-ai-api.git"

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Zulu AI App Generator API is running"}

@app.post("/generate_app")
async def generate_app_endpoint(app_idea: AppIdea):
    """
    Generate app starter code based on user idea, save files, and push to GitHub
    
    Args:
        app_idea: AppIdea model containing the app idea
        
    Returns:
        Dictionary with generated files, file operations, and git status
    """
    # Validate input
    if not app_idea.idea or len(app_idea.idea.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="App idea cannot be empty"
        )
    
    try:
        logger.info(f"Generating app for idea: {app_idea.idea}")
        
        # Generate the app files
        generated_files = generate_app(app_idea.idea.strip())
        
        # Save files to local directories
        commit_message = f"Generated app starter: {app_idea.idea[:50]}{'...' if len(app_idea.idea) > 50 else ''}"
        save_result = save_files_and_push(generated_files, commit_message)
        
        # Run Git workflow to push to GitHub
        git_status = git_workflow(repo_url, commit_message=f"Generated app for idea: {app_idea.idea}")
        
        # Return comprehensive response
        return {
            "idea": app_idea.idea,
            "files": generated_files,
            "file_operations": save_result,
            "git_status": git_status,
            "summary": f"Generated {len(generated_files)} files and pushed to GitHub"
        }
        
    except Exception as e:
        logger.error(f"App generation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate app: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)