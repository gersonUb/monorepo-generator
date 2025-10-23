from src.core.models.project_config import ProjectConfig, FrontendFramework, BackendFramework, Admin_package

def ask_project_config() -> ProjectConfig:
    print(" Project Generator\n")
    
    name = _ask_project_name()
    admin_package = _ask_admin_package()
    frontend = _ask_frontend()
    backend = _ask_backend()
    
    return ProjectConfig(name=name, admin_package= admin_package, frontend=frontend, backend=backend)


def _ask_project_name() -> str:
    while True:
        name = input("Name project: ").strip()
        if name:
            return name
        return "new-project"


def _ask_frontend() -> FrontendFramework:
    print("\n Framework Frontend:")
    print("  1) React")
    print("  2) Vue")
    print("  3) Angular")
    
    while True:
        choice = input("... ").strip() or "1"
        
        if choice in {"1", "react", "r"}:
            return FrontendFramework.REACT
        elif choice in {"2", "vue", "v"}:
            return FrontendFramework.VUE
        elif choice in {"3", "angular", "a"}:
            return FrontendFramework.ANGULAR
        else:
            print("invalid option")


def _ask_backend() -> BackendFramework:
    print("\n Framework Backend:")
    print("  1) Python (Fast-Api)")
    print("  2) Node.js (Express)")
    
    while True:
        choice = input("... ").strip()
        
        if choice in {"1", "fastapi", "fast", "python"}:
            return BackendFramework.FASTAPI
        elif choice in {"2", "node", "nodejs", "express"}:
            return BackendFramework.NODE
        else:
            print("invalid option")

def _ask_admin_package() -> Admin_package:
    print("\n Admin package: ")
    print("  1) Yarn")
    print("  2) Npm")

    while True:
        choice = input("... ").strip()
        if choice in {"1", "yarn", "y"}:
            return Admin_package.YARN
        elif choice in {"2", "npm", "n"}:
            return Admin_package.NPM
        else:
            print("invalid option")