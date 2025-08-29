from fastapi import FastAPI, HTTPException
from models import AppIdea
from code_generator import generate_app
from agent_action import save_files_and_push

app = FastAPI(
    title="Zulu AI - App Generator API",
    description="Generate app starter code from ideas and automatically save to project",
    version="1.0.0"
)

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
        Dictionary with generated files, created file summary, and git commit info
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
        
        # Save files and push to GitHub
        commit_message = f"Generated app starter: {app_idea.idea[:50]}{'...' if len(app_idea.idea) > 50 else ''}"
        save_result = save_files_and_push(generated_files, commit_message)
        
        # Return both the generated files and the save/commit result
        return {
            "generated_files": generated_files,
            "file_operations": save_result,
            "summary": {
                "idea": app_idea.idea,
                "files_created": len(generated_files),
                "status": save_result.get("status", "unknown"),
                "commit_hash": save_result.get("commit_hash"),
                "created_files": save_result.get("created_files", [])
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate app: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)