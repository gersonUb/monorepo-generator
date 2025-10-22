from typing import Protocol
from ..models.project_config import ProjectConfig

class IProjectCreator(Protocol):
    """
    Protocol that coordinates the creation of the base structure of a monorepo
    """

    def create_project(self, config: ProjectConfig):
        """Create the initial structure of the project according to the config"""
        ...