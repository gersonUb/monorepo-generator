from .core.interfaces.file_manager_interface import IFileManager
from .core.models.project_config import ProjectConfig
from .services.command_runner import CommandRunner
from typing import List, Callable, Any

BuilderFunction = Callable[[ProjectConfig, IFileManager, CommandRunner], None]

class ProjectCreator:
    
    def __init__(self, file_manager: IFileManager, runner: CommandRunner):
        self.file_manager = file_manager
        self.runner = runner
        self._builders: List[BuilderFunction] = []

    def add_builder(self, builder_func: BuilderFunction):
        print(f"Builder '{builder_func.__name__}' registered.")
        self._builders.append(builder_func)

    def create_project(self, config: ProjectConfig):
        print(f"Starting project creation: {config.name}...")
        
        if not self._builders:
            print("No builders registered. Nothing to create.")
            return

        try:
            for builder in self._builders:
                print(f"\n--- Running Builder: {builder.__name__} ---")
                builder(
                    config=config,
                    file_manager=self.file_manager,
                    runner=self.runner
                )
            
            print(f"\n Project '{config.name}' created successfully!")

        except Exception as e:
            print(f"\n FATAL ERROR during creation: {e}")
            print("Build process stopped.")
            raise e