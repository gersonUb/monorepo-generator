from src.core.models.project_config import ProjectConfig
from .interfaces.ui_provider import IUserInterface
from src.services.wizard import WizardRunner

def ask_project_config(ui: IUserInterface) -> ProjectConfig:
    wizard = WizardRunner()
    wizard.add_step(
        key="name",
        action=lambda ctx: ui.ask_project_name(default=ctx.get("name", "my-app"))
    )
    wizard.add_step(
        key="path",
        action=lambda ctx: ui.ask_destination_path()
    )
    wizard.add_step(
        key="admin_package",
        action=lambda ctx: ui.ask_admin_package()
    )
    wizard.add_step(
        key="frontend",
        action=lambda ctx: ui.ask_frontend_framework()
    )
    wizard.add_step(
        key="backend",
        action=lambda ctx: ui.ask_backend_framework()
    )
    answers = wizard.run()

    ui.show_success("Configuration captured!")

    return ProjectConfig(
        name=answers["name"], 
        path=answers["path"],
        admin_package=answers["admin_package"], 
        frontend=answers["frontend"], 
        backend=answers["backend"]
    )