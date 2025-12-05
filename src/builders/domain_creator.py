from pathlib import Path
from ..services.command_runner import CommandRunner
from ..core.interfaces.file_manager_interface import IFileManager
from ..core.models.project_config import ProjectConfig, BackendFramework
from .scripts.create_fastapi_domain import create_fastapi_domain
from .scripts.create_node_domain import create_node_domain
from ..services.executable_finder import find_executable

def create_domain(
    config: ProjectConfig, 
    file_manager: IFileManager, 
    runner: CommandRunner
):
    print("Configuring shared domain package...")
    
    framework = config.backend
    domain_path = Path(config.name) / "domain"
    
    if not domain_path.exists():
        print(f"Creating domain package at '{domain_path}'...")
        file_manager.create_folder(str(domain_path))

    match framework:
        case BackendFramework.FASTAPI:
            print("Framework selected: Python (SQLAlchemy, Poetry)")
            create_fastapi_domain(
                domain_path=domain_path,
                file_manager=file_manager,
                runner=runner,
                find_executable_func=find_executable
            )
            
        case BackendFramework.NODE:
            print("Framework selected: Node.js (Prisma, Vitest)")
            create_node_domain(
                domain_path=domain_path,
                file_manager=file_manager,
                runner=runner,
                config=config,
                find_executable_func=find_executable
            )
        case _:
            print(f"⚠️ Unknown backend framework: {framework}. Skipping domain.")