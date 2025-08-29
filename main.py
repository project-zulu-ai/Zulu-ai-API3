    from fastapi import FastAPI, HTTPException
    from models import AppIdea
    from code_generator import generate_app
    from utils.git_helper import git_workflow  # ✅ use git helper

    app = FastAPI(
        title="Zulu AI - App Generator API",
        description="Generate app starter code from ideas and automatically save & push to GitHub",
        version="1.0.0"
    )

    @app.get("/")
    async def root():
        """Health check endpoint"""
        return {"message": "Zulu AI App Generator API is running"}

    @app.post("/generate_app")
    async def generate_app_endpoint(app_idea: AppIdea):
        """
        Generate app starter code based on user idea, save files, and push to GitHub.
        """
        if not app_idea.idea or len(app_idea.idea.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="App idea cannot be empty"
            )

        try:
            # 1. Generate the app files
            generated_files = generate_app(app_idea.idea.strip())

            # 2. Save generated files locally
            for path, content in generated_files.items():
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)

            # 3. Run Git workflow (push to repo)
            commit_message = f"Generated app starter: {app_idea.idea[:50]}{'...' if len(app_idea.idea) > 50 else ''}"
            git_status = git_workflow(
                repo_url="https://github.com/project-zulu-ai/Zulu-ai-API3.git",  # ✅ new repo URL
                commit_message=commit_message
            )

            # 4. Return structured response
            return {
                "idea": app_idea.idea,
                "files": generated_files,
                "git_status": git_status,
                "summary": f"Generated {len(generated_files)} files and pushed to GitHub"
            }

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate app: {str(e)}"
            )

    if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=5000)