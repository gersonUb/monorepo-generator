from pathlib import Path
from typing import Dict, Any
from ..core.models.project_config import ProjectConfig
from ..core.interfaces.file_manager_interface import IFileManager
from ..services.command_runner import CommandRunner

def _base_template(project_name: str) -> dict:
    return {
        project_name: {
            'apps': {},
            'packages': {},
            'docs': {},
            'README.md': f'# Welcome to {project_name}',
            '.gitignore': 'node_modules\n.venv\n__pycache__\n'
        }
    }

def _create_recursive(file_manager: IFileManager, structure: Dict[str, Any], base_path: str = ""):
    for name, content in structure.items():
        current_path = f"{base_path}/{name}" if base_path else name

        if isinstance(content, dict):
            file_manager.create_folder(current_path)
            _create_recursive(file_manager, content, current_path)
        elif isinstance(content, str):
            file_manager.create_file(current_path, content)
        else:
            file_manager.create_folder(current_path)

def create_base_structure(config: ProjectConfig, file_manager: IFileManager, runner: CommandRunner):
    full_project_path = config.path / config.name
    print(f"Creating project skeleton in '{full_project_path}'...")
    
    structure = _base_template(config.name)
    _create_recursive(file_manager, structure, base_path=str(config.path))
    
    print("Base skeleton created.")