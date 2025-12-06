from pathlib import Path
from ..core.models.project_config import ProjectConfig
from ..core.interfaces.file_manager_interface import IFileManager
from ..services.command_runner import CommandRunner
from ..services.docker_content_generator import DockerContentGenerator

def create_docker(
    config: ProjectConfig, 
    file_manager: IFileManager, 
    runner: CommandRunner
):
    print(" Configuring Docker environment...")

    src_root = Path(__file__).parent.parent
    templates_path = src_root / "templates" / "docker_templates"

    try:
        docker_gen = DockerContentGenerator(templates_path)
    except Exception as e:
        print(f" Error initializing Docker Generator: {e}")
        raise e

    try:
        compose_content = docker_gen.get_docker_compose_content(config)
        dockerfile_content = docker_gen.get_monolithic_dockerfile(config)
        dockerignore_content = docker_gen.get_dockerignore_content()
        env_example_content = docker_gen.get_env_example_content()
        
    except FileNotFoundError as e:
        print(f" Error reading templates from {templates_path}: {e}")
        raise e

    root_path = Path(config.name) 
    
    file_manager.create_file(str(root_path / "docker-compose.yml"), compose_content)
    file_manager.create_file(str(root_path / "Dockerfile"), dockerfile_content)
    file_manager.create_file(str(root_path / ".dockerignore"), dockerignore_content)
    file_manager.create_file(str(root_path / ".env.example"), env_example_content)

    print(f" Docker configuration created successfully in {root_path}")