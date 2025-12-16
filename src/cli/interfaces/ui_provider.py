from typing import Protocol
from pathlib import Path
from ...core.models.project_config import FrontendFramework, BackendFramework, Admin_package

class IUserInterface(Protocol):

    def ask_project_name(self, default: str) -> str:
        ...

    def ask_admin_package(self) -> Admin_package:
        ...

    def ask_destination_path(self) -> Path:
        ...

    def ask_frontend_framework(self) -> FrontendFramework:
        ...

    def ask_backend_framework(self) -> BackendFramework:
        ...
    
    def show_success(self, message: str):
        ...
        
    def show_error(self, message: str):
        ...