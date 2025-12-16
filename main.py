from src.cli.adapters.interactive_console import InteractiveConsoleUI
from src.project_creator import ProjectCreator
from src.core.infrastructure.file_manager import FileManager
from src.cli.questionnaire import ask_project_config
from src.services.command_runner import CommandRunner 
from src.builders.base_structure_creator import create_base_structure
from src.builders.fronted_creator import create_frontend
from src.builders.backend_creator import create_backend
from src.builders.domain_creator import create_domain
from src.builders.docker_creator import create_docker

def main():
    ui = InteractiveConsoleUI()
    config = ask_project_config(ui)

    file_manager = FileManager(".") 
    runner = CommandRunner()

    creator = ProjectCreator(file_manager, runner)

    creator.add_builder(create_base_structure) 
    creator.add_builder(create_frontend)
    creator.add_builder(create_backend)
    creator.add_builder(create_domain)
    creator.add_builder(create_docker)
    
    creator.create_project(config)

    print(f"\n Project '{config.name}' create correctly!")

if __name__ == "__main__":
    main()