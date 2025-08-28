from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import AppIdeaRequest, GeneratedAppResponse
from code_generator import CodeGenerator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Zulu AI - App Builder Service",
    description="Generate structured app starter code based on user ideas",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize code generator
code_generator = CodeGenerator()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Zulu AI App Builder Service is running"}

@app.post("/generate_app", response_model=GeneratedAppResponse)
async def generate_app(request: AppIdeaRequest):
    """
    Generate structured app starter code based on user's app idea.
    
    Args:
        request: AppIdeaRequest containing the app idea description
        
    Returns:
        GeneratedAppResponse with generated code files
    """
    try:
        logger.info(f"Generating app for idea: {request.idea[:100]}...")
        
        # Validate input
        if not request.idea or len(request.idea.strip()) < 5:
            raise HTTPException(
                status_code=400, 
                detail="App idea must be at least 5 characters long"
            )
        
        # Generate code based on the idea
        generated_files = code_generator.generate_app_code(request.idea)
        
        logger.info(f"Successfully generated {len(generated_files)} files")
        
        return GeneratedAppResponse(
            success=True,
            message="App code generated successfully",
            files=generated_files
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating app: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate app code: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "zulu-ai-app-builder"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
