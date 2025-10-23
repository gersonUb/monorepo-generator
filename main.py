from src.project_creator import ProjectCreator
from src.core.infrastructure.file_manager import FileManager
from src.cli.questionnaire import ask_project_config

def main():
    config = ask_project_config()
    file_manager = FileManager(".")
    creator = ProjectCreator(file_manager)
    
    creator.create_project(config)
    
    print(f"\n Project '{config.name}' create correctly!")


if __name__ == "__main__":
    main()
