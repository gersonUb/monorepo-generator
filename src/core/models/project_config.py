from dataclasses import dataclass
from enum import Enum


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
    admin_package: Admin_package
    frontend: FrontendFramework
    backend: BackendFramework