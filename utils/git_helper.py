import subprocess

def run_git_command(cmd):
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True
        )
        return {
            "command": cmd,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode,
            "success": result.returncode == 0
        }
    except Exception as e:
        return {"command": cmd, "error": str(e), "success": False}


def git_workflow(repo_url: str, commit_message: str = "AI generated update"):
    status = {}

    # Init repo
    status["init"] = run_git_command("git init")

    # Add remote (ignore error if already exists)
    status["remote_add"] = run_git_command(f"git remote add origin {repo_url}")

    # Stage changes
    status["add"] = run_git_command("git add .")

    # Commit changes
    status["commit"] = run_git_command(f'git commit -m "{commit_message}"')

    # Push to GitHub
    status["push"] = run_git_command("git push origin main --force")

    return status