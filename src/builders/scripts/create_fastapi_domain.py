from pathlib import Path
from typing import Callable, Optional
from ...services.command_runner import CommandRunner
from ...core.interfaces.file_manager_interface import IFileManager

FinderFunc = Callable[[str], Optional[str]]

def create_fastapi_domain(
    domain_path: Path,
    file_manager: IFileManager,
    runner: CommandRunner,
    find_executable_func: FinderFunc
):
    print("Verifying executable: 'poetry'...")
    poetry_exe = find_executable_func("poetry")
    
    if poetry_exe is None:
        raise FileNotFoundError("Executable 'poetry' not found.")
    
    print(f"Found executable at: {poetry_exe}")
    domain_path_str = str(domain_path)

    print("\nStep 1: Initializing Poetry project...")
    runner.run([poetry_exe, "init", "-n"], cwd=domain_path_str)

    print("\nStep 2: Configuring Poetry for in-project venv...")
    runner.run([poetry_exe, "config", "virtualenvs.in-project", "true", "--local"], cwd=domain_path_str)

    print("\nStep 3: Installing main dependencies (sqlalchemy, passlib, jose)...")
    main_deps = ["sqlalchemy", "passlib[bcrypt]", "python-jose[cryptography]", "pydantic"]
    runner.run([poetry_exe, "add"] + main_deps, cwd=domain_path_str)

    print("\nStep 4: Installing dev dependencies (pytest, ruff)...")
    runner.run([poetry_exe, "add", "--group", "dev", "pytest", "ruff"], cwd=domain_path_str)

    print("\nStep 5: Creating domain source structure...")
    src_path = domain_path / "src"
    file_manager.create_folder(str(src_path))
    file_manager.create_file(str(src_path / "__init__.py"), "")
    
    folders = ["entities", "services", "use_cases", "auth"]
    for folder in folders:
        folder_path = src_path / folder
        file_manager.create_folder(str(folder_path))
        file_manager.create_file(str(folder_path / "__init__.py"), "")
        file_manager.create_file(str(folder_path / ".gitkeep"), "") # Para que git las vea

    print(f"\nPython (Domain) package configured successfully at: {domain_path}")