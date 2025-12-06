import shutil
from pathlib import Path
from typing import List, Callable

from .core.interfaces.file_manager_interface import IFileManager
from .core.models.project_config import ProjectConfig
from .services.command_runner import CommandRunner

BuilderFunction = Callable[[ProjectConfig, IFileManager, CommandRunner], None]

class ProjectCreator:
    
    def __init__(self, file_manager: IFileManager, runner: CommandRunner):
        self.file_manager = file_manager
        self.runner = runner
        self._builders: List[BuilderFunction] = []

    def add_builder(self, builder_func: BuilderFunction):
        print(f"Builder '{builder_func.__name__}' registered.")
        self._builders.append(builder_func)

    def _rollback(self, path_to_clean: str):
        print(f"\n  ROLLBACK INITIATED: Cleaning up '{path_to_clean}'...")
        path = Path(path_to_clean)
        
        if path.exists() and path.is_dir():
            try:
                shutil.rmtree(path)
                print(" Cleanup complete. System state restored.")
            except OSError as e:
                print(f" Error during rollback: {e}")
        else:
            print(" Nothing to clean (directory didn't exist yet).")

    def create_project(self, config: ProjectConfig):
        print(f"Starting project creation: {config.name}...")
        
        if not self._builders:
            print("No builders registered. Nothing to create.")
            return

        project_root = config.name

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
            print("The process was interrupted.")

            self._rollback(project_root)
            
            raise e