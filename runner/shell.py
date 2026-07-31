"""Shell execution runner for subprocess and command execution."""

import subprocess
from typing import Tuple

class ShellRunner:
    def run_command(self, command: str, cwd: str = ".") -> Tuple[int, str, str]:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.returncode, result.stdout, result.stderr
