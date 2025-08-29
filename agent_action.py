import os
import subprocess
from typing import Dict

def save_files_and_push(files: Dict[str, str], commit_message: str = "Generated app starter") -> Dict[str, str]:
    """
    Save generated files to correct directories, commit, and push to GitHub.
    
    Args:
        files (dict): { "path/to/file": "file_content" }
        commit_message (str): Git commit message
        
    Returns:
        dict: Summary of operations performed
    """
    created_files = []
    git_hash = None
    
    try:
        # Save files to their respective directories
        for path, content in files.items():
            # Ensure directory exists
            if '/' in path:
                os.makedirs(os.path.dirname(path), exist_ok=True)
            
            # Write file
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            created_files.append(path)
            print(f"✅ Saved: {path}")

        # Git operations
        try:
            # Add all changes
            subprocess.run(["git", "add", "."], check=True, capture_output=True, text=True)
            
            # Commit changes
            commit_result = subprocess.run(
                ["git", "commit", "-m", commit_message], 
                check=True, capture_output=True, text=True
            )
            
            # Get commit hash
            hash_result = subprocess.run(
                ["git", "rev-parse", "HEAD"], 
                check=True, capture_output=True, text=True
            )
            git_hash = hash_result.stdout.strip()[:7]  # Short hash
            
            # Push to GitHub
            subprocess.run(["git", "push"], check=True, capture_output=True, text=True)
            
            print(f"🚀 Changes committed ({git_hash}) and pushed to GitHub successfully!")
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Git error: {e}")
            # Still return success for file creation even if git fails
            return {
                "status": "files_created_git_failed",
                "created_files": created_files,
                "git_error": str(e),
                "commit_hash": None
            }
        
        return {
            "status": "success",
            "created_files": created_files,
            "commit_hash": git_hash,
            "commit_message": commit_message
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "created_files": created_files
        }

# Example usage for testing
if __name__ == "__main__":
    test_files = {
        "frontend/App.js": "console.log('Hello World React');",
        "backend/main.py": "print('Hello from backend');",
        "README.md": "# Example generated app"
    }
    
    result = save_files_and_push(test_files, "Test: Initial generated app starter")
    print("Result:", result)