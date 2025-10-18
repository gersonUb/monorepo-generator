from typing import Protocol, List
from pathlib import Path

class IFileManager(Protocol):
    """Protocol for managing files and folders"""
    
    def create_folder(self, folder_path: str) -> Path:
        """Creates a folder and returns the created path"""
        ...
    
    def create_file(self, file_path: str, content: str = "") -> Path:
        """Creates a file with content and returns the path"""
        ...

    def exists(self, path: str) -> bool:
        """Checks if a route exists"""
        ...

    def list_files(self, folder_path: str) -> List[str]:
        """Lists files in a folder"""
        ...