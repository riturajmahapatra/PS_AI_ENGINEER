"""Repository runner for workspace file system operations."""

import os


class RepositoryRunner:
    def __init__(self, root_dir: str = "."):
        self.root_dir = root_dir

    def list_files(self) -> list[str]:
        return os.listdir(self.root_dir)
