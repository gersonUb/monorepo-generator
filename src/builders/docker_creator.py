from pathlib import Path
from ..services.command_runner import CommandRunner
from ..core.interfaces.file_manager_interface import IFileManager
from ..core.models.project_config import ProjectConfig
from ..templates.docker_templates import (
    get_docker_compose_content,
    get_docker_compose_test_content,
    get_monolithic_dockerfile,
    get_dockerignore_content,
    get_env_example_content,
    get_env_content
)

def create_docker(
    config: ProjectConfig, 
    file_manager: IFileManager, 
):
    print("Configuring Docker...")
    root_path = Path(config.name)
    docker_dir = root_path / ".docker"
    
    file_manager.create_folder(str(docker_dir))

    compose_content = get_docker_compose_content(config)
    file_manager.create_file(str(docker_dir / "docker-compose.yml"), compose_content)

    test_compose_content = get_docker_compose_test_content(config)
    file_manager.create_file(str(docker_dir / "docker-compose.test.yml"), test_compose_content)

    env_example_content = get_env_example_content()
    file_manager.create_file(str(docker_dir / ".env.example"), env_example_content)
    
    env_content = get_env_content()
    file_manager.create_file(str(docker_dir / ".env"), env_content)

    ignore_content = get_dockerignore_content()
    file_manager.create_file(str(root_path / ".dockerignore"), ignore_content)

    dockerfile_content = get_monolithic_dockerfile(config)
    file_manager.create_file(str(docker_dir / "dockerfile"), dockerfile_content)

    print("Docker configuration files created successfully in .docker/ folder.")