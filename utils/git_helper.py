import subprocess
import logging

# Set up logging
logger = logging.getLogger(__name__)

def run_command(cmd):
    """
    Run a shell command safely and capture output
    
    Args:
        cmd: List of command arguments
        
    Returns:
        str: Command output or error message
    """
    try:
        result = subprocess.run(cmd, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        error_msg = f"Error: {e.stderr}" if e.stderr else f"Command failed: {' '.join(cmd)}"
        logger.error(error_msg)
        return error_msg

def git_push(repo_url: str, commit_message: str = "Auto commit from Zulu API"):
    """
    Initialize git repo, commit files, and push to GitHub
    
    Args:
        repo_url: GitHub repository URL
        commit_message: Commit message
        
    Returns:
        dict: Status and message of git operations
    """
    try:
        logger.info(f"Starting git operations for repo: {repo_url}")
        
        # Initialize git if not already initialized
        init_result = run_command(["git", "init"])
        logger.info(f"Git init: {init_result}")
        
        # Add all files
        add_result = run_command(["git", "add", "."])
        logger.info(f"Git add: {add_result}")
        
        # Commit changes
        commit_result = run_command(["git", "commit", "-m", commit_message])
        logger.info(f"Git commit: {commit_result}")
        
        # Set main branch
        branch_result = run_command(["git", "branch", "-M", "main"])
        logger.info(f"Git branch: {branch_result}")
        
        # Remove existing origin if it exists (ignore errors)
        try:
            run_command(["git", "remote", "remove", "origin"])
        except:
            pass  # It's okay if origin doesn't exist
        
        # Add remote origin
        remote_result = run_command(["git", "remote", "add", "origin", repo_url])
        logger.info(f"Git remote add: {remote_result}")
        
        # Push to GitHub
        push_result = run_command(["git", "push", "-u", "origin", "main", "--force"])
        logger.info(f"Git push: {push_result}")
        
        return {
            "status": "success", 
            "message": "Code pushed to GitHub successfully",
            "details": {
                "commit_message": commit_message,
                "repo_url": repo_url,
                "push_result": push_result
            }
        }
        
    except Exception as e:
        error_msg = f"Git operations failed: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error", 
            "message": error_msg
        }