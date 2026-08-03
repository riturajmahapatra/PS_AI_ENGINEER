"""Git integration runner for commit, branch, and status tracking."""

from .shell import ShellRunner


class GitRunner:
    def __init__(self, repo_path: str = "."):
        self.shell = ShellRunner()
        self.repo_path = repo_path

    def get_status(self) -> str:
        code, out, _ = self.shell.run_command("git status", cwd=self.repo_path)
        return out
