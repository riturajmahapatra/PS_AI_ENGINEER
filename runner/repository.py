"""Repository runner for workspace file system operations."""

import os
from typing import List

class RepositoryRunner:
    def __init__(self, root_dir: str = "."):
        self.root_dir = root_dir

    def list_files(self) -> List[str]:
        return os.listdir(self.root_dir)
