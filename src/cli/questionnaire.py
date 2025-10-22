from src.core.models.project_config import ProjectConfig, FrontendFramework, BackendFramework

def ask_project_config() -> ProjectConfig:
    print("🚀 Project Generator\n")
    
    name = _ask_project_name()
    frontend = _ask_frontend()
    backend = _ask_backend()
    
    return ProjectConfig(name=name, frontend=frontend, backend=backend)


def _ask_project_name() -> str:
    while True:
        name = input("Name project").strip()
        if name:
            return name
        return "new-project"


def _ask_frontend() -> FrontendFramework:
    print("\n Framework Frontend:")
    print("  1) React")
    
    while True:
        choice = input("...").strip() or "1"
        
        if choice in {"1", "react", "r"}:
            return FrontendFramework.REACT
        else:
            print("invalid option")


def _ask_backend() -> BackendFramework:
    print("\n Framework Backend:")
    print("  1) Python (Fast-Api)")
    print("  2) Node.js (Express)")
    
    while True:
        choice = input("...").strip()
        
        if choice in {"1", "fastapi", "fast", "python"}:
            return BackendFramework.FASTAPI
        elif choice in {"2", "node", "nodejs", "express"}:
            return BackendFramework.NODE
        else:
            print("invalid option")