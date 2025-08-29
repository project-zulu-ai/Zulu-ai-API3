        import subprocess

        # Default GitHub repo for Zulu AI API
        DEFAULT_REPO_URL = "https://github.com/project-zulu-ai/Zulu-ai-API3.git"


        def run_git_command(cmd):
            """Run a shell git command and return its result."""
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


        def git_workflow(repo_url: str = DEFAULT_REPO_URL, commit_message: str = "AI generated update"):
            """
            Runs the full Git workflow: init, branch, add remote, commit, push.
            If no repo_url is provided, defaults to Zulu-ai-API3 repo.
            """
            status = {}

            # Init repo (safe even if already initialized)
            status["init"] = run_git_command("git init")

            # Ensure branch is main
            status["branch"] = run_git_command("git branch -M main")

            # Add remote (ignore error if already exists)
            status["remote_add"] = run_git_command(f"git remote add origin {repo_url}")

            # Stage all changes
            status["add"] = run_git_command("git add .")

            # Commit changes (skip if nothing new to commit)
            status["commit"] = run_git_command(f'git commit -m "{commit_message}"')

            # Push to GitHub (force overwrite main branch)
            status["push"] = run_git_command("git push -u origin main --force")

            return status