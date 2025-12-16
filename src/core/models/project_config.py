from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class FrontendFramework(Enum):
    REACT = "react"
    VUE = "vue"
    ANGULAR = "angular"


class BackendFramework(Enum):
    FASTAPI = "fastapi"
    NODE = "node"
    # GO = "go"
    # JAVA = "java"

class Admin_package(Enum):
    NPM = "npm"
    YARN = "yarn"


@dataclass
class ProjectConfig:
    name: str
    path: Path
    admin_package: Admin_package
    frontend: FrontendFramework
    backend: BackendFramework

    @property
    def full_path(self) -> Path:
        return self.path / self.name