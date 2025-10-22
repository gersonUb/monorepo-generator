from dataclasses import dataclass
from enum import Enum


class FrontendFramework(Enum):
    REACT = "react"
    # VUE = "vue"
    # ANGULAR = "angular"


class BackendFramework(Enum):
    FASTAPI = "fastapi"
    NODE = "node"
    # GO = "go"
    # JAVA = "java"


@dataclass
class ProjectConfig:
    name: str
    frontend: FrontendFramework
    backend: BackendFramework