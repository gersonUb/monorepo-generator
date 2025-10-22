from .core.interfaces.file_manager_interface import IFileManager
from .core.templates.base_template import base_template
from .core.models.project_config import ProjectConfig
from .core.interfaces.project_creator_interface import IProjectCreator
from typing import Dict, Any

class ProjectCreator(IProjectCreator):    
    def __init__(self, file_manager: IFileManager):
        self.file_manager = file_manager

    def create_project(self, config: ProjectConfig):
        structure = base_template(config.name)
        self._create_recursive(structure)

    def _create_recursive(self, structure: Dict[str, Any], base_path: str = ""):
        for name, content in structure.items():
            current_path = f"{base_path}/{name}" if base_path else name

            if isinstance(content, dict):
                self.file_manager.create_folder(current_path)
                self._create_recursive(content, current_path)
            elif isinstance(content, str):
                self.file_manager.create_file(current_path, content)
            else:
                self.file_manager.create_folder(current_path)
