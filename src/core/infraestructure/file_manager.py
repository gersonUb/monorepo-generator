from pathlib import Path;
from core.interfaces import IFileManager;

class FileManager(IFileManager):
    def __init__(self, project_name: str):
        self.base_path = Path(project_name)

    def create_folder(self, folder_path: str) -> Path:
        path = self.base_path / folder_path
        path.mkdir(parents=True, exist_ok=True)
        return path

    def create_file(self, file_path:str , content:str = ""):
        path = self.base_path / file_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path
    
    def exists(self, path):
        return (self.base_path / path).exists()
    
    def list_files_folders(self, folder_path):
        folder = self.base_path / folder_path

        if not folder.exists():
            return []

        archives = []
        for f in folder.iterdir():
            if f.is_file():
                archives.append(f.name)
            elif f.is_dir():
                archives.append(f"{f.name}/")
        return archives