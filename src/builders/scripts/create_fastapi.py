from pathlib import Path
from typing import Callable, Optional
from ...services.command_runner import CommandRunner
from ...core.interfaces.file_manager_interface import IFileManager

FinderFunc = Callable[[str], Optional[str]]

def create_fastapi_project(
    api_path: Path,
    file_manager: IFileManager,
    runner: CommandRunner,
    find_executable_func: FinderFunc
):
    print("Verifying executable: 'poetry'...")
    poetry_exe = find_executable_func("poetry")
    
    if poetry_exe is None:
        print("❌ FATAL: Could not find 'poetry' executable.")
        print("Please ensure Poetry is installed and in your system PATH.")
        raise FileNotFoundError("Executable 'poetry' not found.")
    
    print(f"Found executable at: {poetry_exe}")
    api_path_str = str(api_path)

    print("\nStep 1: Initializing Poetry project...")
    runner.run([poetry_exe, "init", "-n"], cwd=api_path_str)

    print("\nStep 2: Configuring Poetry for in-project venv...")
    runner.run([poetry_exe, "config", "virtualenvs.in-project", "true", "--local"], cwd=api_path_str)

    print("\nStep 3: Installing main dependencies (fastapi, uvicorn)...")
    runner.run([poetry_exe, "add", "fastapi", "uvicorn[standard]", "python-dotenv"], cwd=api_path_str)

    print("\nStep 4: Installing dev dependencies (pytest, httpx, ruff)...")
    runner.run([poetry_exe, "add", "--group", "dev", "pytest", "httpx", "ruff"], cwd=api_path_str)

    print("\nStep 5: Creating source files (src/main.py)...")
    src_path = api_path / "src"
    file_manager.create_folder(str(src_path))
    file_manager.create_file(str(src_path / "__init__.py"), "")
    
    main_py_content = (
        "from fastapi import FastAPI\n\n"
        "app = FastAPI()\n\n"
        "@app.get(\"/\")\n"
        "def read_root():\n"
        "    return {\"Hello\": \"From FastAPI\"}\n"
    )
    file_manager.create_file(str(src_path / "main.py"), main_py_content)
    
    env_example_content = "APP_HOST=0.0.0.0\nAPP_PORT=8000\n"
    file_manager.create_file(str(api_path / ".env.example"), env_example_content)

    ruff_toml_content = (
        "[lint]\n"
        "select = [\"E\", \"F\", \"W\", \"I\", \"UP\"]\n\n"
        "[format]\n"
        "quote-style = \"double\"\n"
    )
    file_manager.create_file(str(api_path / "ruff.toml"), ruff_toml_content)
    
    print(f"\nPython (FastAPI) backend configured successfully at: {api_path}")