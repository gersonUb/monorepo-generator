from src.core.models.project_config import ProjectConfig
from .interfaces.ui_provider import IUserInterface

def ask_project_config(ui: IUserInterface) -> ProjectConfig:
    name = ui.ask_project_name(default="my-app")
    path = ui.ask_destination_path()
    admin_package = ui.ask_admin_package()
    frontend = ui.ask_frontend_framework()
    backend = ui.ask_backend_framework()
    
    ui.show_success("Configuration captured!")

    return ProjectConfig(
        name=name, 
        path=path,
        admin_package=admin_package, 
        frontend=frontend, 
        backend=backend
    )