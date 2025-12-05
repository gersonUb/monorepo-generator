from pathlib import Path
from ..services.command_runner import CommandRunner
from ..core.interfaces.file_manager_interface import IFileManager
from ..core.models.project_config import ProjectConfig, BackendFramework
from .scripts.create_fastapi import create_fastapi_project
from .scripts.create_node import create_node_project
from ..services.executable_finder import find_executable

def create_backend(
    config: ProjectConfig, 
    file_manager: IFileManager, 
    runner: CommandRunner
):
    print("Backend (Api) configuration")
    framework = config.backend
    
    api_path = Path(config.name) / "apps" / "api"
    if not api_path.exists():
        print(f"Creating backend directory at '{api_path}'...")
        file_manager.create_folder(str(api_path))
    
    file_manager.create_folder(str(api_path / "data"))
    file_manager.create_folder(str(api_path / "public"))

    match framework:
        case BackendFramework.FASTAPI:
            print("Framework selected: Python (FastAPI)")
            create_fastapi_project(
                api_path=api_path,
                file_manager=file_manager,
                runner=runner,
                find_executable_func=find_executable
            )
            
        case BackendFramework.NODE:
            print("Framework selected: Node.js (Express)")
            create_node_project(
                api_path=api_path,
                file_manager=file_manager,
                runner=runner,
                config=config,
                find_executable_func=find_executable
            )
        case _:
            print(f"⚠️ Unknown backend framework: {framework}. Skipping.")

        