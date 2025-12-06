from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from rich.console import Console
from rich.panel import Panel
from ...core.models.project_config import (
    FrontendFramework, 
    BackendFramework, 
    Admin_package
)
from ..interfaces.ui_provider import IUserInterface
console = Console()

class InteractiveConsoleUI(IUserInterface):
    
    def __init__(self):
        self._print_header()

    def _print_header(self):
        console.print(Panel.fit(
            "[bold cyan]🚀 Project Generator[/bold cyan] [dim]Clean Architecture - Monorepo[/dim]",
            border_style="cyan",
            padding=(1, 2)
        ))
        console.print("")

    def ask_project_name(self, default: str) -> str:
        return inquirer.text(
            message="Project Name:",
            default=default,
            qmark="📁",
            amark="✔",
            validate=lambda result: len(result) > 0,
            invalid_message="Name cannot be empty",
        ).execute()

    def ask_admin_package(self) -> Admin_package:
        return inquirer.select(
            message="Select Package Manager:",
            choices=[
                Choice(value=Admin_package.NPM, name="npm"),
                Choice(value=Admin_package.YARN, name="yarn"),
            ],
            default=Admin_package.NPM,
            pointer="❯",
            qmark="📦",
        ).execute()

    def ask_frontend_framework(self) -> FrontendFramework:
        return inquirer.select(
            message="Select Frontend Framework:",
            choices=[
                Choice(value=FrontendFramework.REACT, name="React"),
                Choice(value=FrontendFramework.VUE, name="Vue"),
                Choice(value=FrontendFramework.ANGULAR, name="Angular"),
            ],
            default=FrontendFramework.REACT,
            pointer="❯",
            qmark="💻",
        ).execute()

    def ask_backend_framework(self) -> BackendFramework:
        return inquirer.select(
            message="Select Backend Framework:",
            choices=[
                Choice(value=BackendFramework.FASTAPI, name="Python (FastAPI)"),
                Choice(value=BackendFramework.NODE, name="Node.js (Express)"),
                Separator(),
                Choice(value=None, name="Django (Coming soon)", enabled=False),
            ],
            default=BackendFramework.FASTAPI,
            pointer="❯",
            qmark="🐍",
        ).execute()
        
    def show_success(self, message: str):
        console.print("")
        console.rule("[bold green]Success![/bold green]")
        console.print(f"[bold green]✔ {message}[/bold green]")
        console.print("[dim]Your project is ready to build.[/dim]\n")

    def show_error(self, message: str):
        console.print(f"[bold red]✘ Error: {message}[/bold red]")