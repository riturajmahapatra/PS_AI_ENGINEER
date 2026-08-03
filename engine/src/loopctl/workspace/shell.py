"""Shell execution runner for subprocess and command execution."""

import subprocess


class ShellRunner:
    def run_command(self, command: str, cwd: str = ".") -> tuple[int, str, str]:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.returncode, result.stdout, result.stderr
