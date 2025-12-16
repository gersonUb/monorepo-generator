from InquirerPy import inquirer
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
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

    def _execute_safe(self, prompt):
        """
        Ejecuta el prompt. Si el resultado es None (Salir), 
        lanza KeyboardInterrupt para que main.py cierre todo.
        """
        result = prompt.execute()
        
        if result is None:
            raise KeyboardInterrupt 
            
        return result

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
        prompt = inquirer.select(
            message="Select Package Manager:",
            choices=[
                Choice(value=Admin_package.NPM, name="npm"),
                Choice(value=Admin_package.YARN, name="yarn"),
                Separator(""),
                Choice(value=None, name="❌ exit"), 
            ],
            default=Admin_package.NPM,
            pointer="❯",
            qmark="📦",
        )
        return self._execute_safe(prompt)

    def ask_frontend_framework(self) -> FrontendFramework:
        prompt = inquirer.select(
            message="Select Frontend Framework:",
            choices=[
                Choice(value=FrontendFramework.REACT, name="React"),
                Choice(value=FrontendFramework.VUE, name="Vue"),
                Choice(value=FrontendFramework.ANGULAR, name="Angular"),
                Separator(""),
                Choice(value=None, name="❌ exit"), 
                
            ],
            default=FrontendFramework.REACT,
            pointer="❯",
            qmark="💻",
        )
        return self._execute_safe(prompt)

    def ask_backend_framework(self) -> BackendFramework:
        prompt = inquirer.select(
            message="Select Backend Framework:",
            choices=[
                Choice(value=BackendFramework.FASTAPI, name="Python (FastAPI)"),
                Choice(value=BackendFramework.NODE, name="Node.js (Express)"),
                Separator(""),
                Choice(value=None, name="❌ exit"), 
            ],
            default=BackendFramework.FASTAPI,
            pointer="❯",
            qmark="🐍",
        )
        return self._execute_safe(prompt)
    
    def ask_destination_path(self) -> Path:
        prompt = inquirer.select(
            message="Where should we create the project?",
            choices=[
                Choice(value="current", name="Current Directory (.)"),
                Choice(value="custom", name="Choose Folder... 📂"),
                Separator(""),
                Choice(value=None, name="❌ exit"), # Agregamos salir aquí también por consistencia
            ],
            default="current",
            pointer="❯",
            qmark="📍"
        )
        
        choice = self._execute_safe(prompt)

        if choice == "current":
            return Path.cwd()
            
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        print("  Waiting for folder selection...")
        folder_selected = filedialog.askdirectory(
            title="Select Destination Folder",
            mustexist=True
        )
        
        root.destroy()

        if not folder_selected:
            console.print("[yellow]⚠ No folder selected. Using current directory.[/yellow]")
            return Path.cwd()

        return Path(folder_selected)
        
    def show_success(self, message: str):
        console.print("")
        console.rule("[bold green]Success![/bold green]")
        console.print(f"[bold green]✔ {message}[/bold green]")
        console.print("[dim]Your project is ready to build.[/dim]\n")

    def show_error(self, message: str):
        console.print(f"[bold red]✘ Error: {message}[/bold red]")