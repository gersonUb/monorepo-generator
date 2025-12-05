from pathlib import Path
from typing import Callable, Optional
from ...services.command_runner import CommandRunner
from ...core.interfaces.file_manager_interface import IFileManager
from ...core.models.project_config import ProjectConfig

FinderFunc = Callable[[str], Optional[str]]

def create_node_domain(
    domain_path: Path,
    file_manager: IFileManager,
    runner: CommandRunner,
    config: ProjectConfig,
    find_executable_func: FinderFunc
):
    pkg_name = config.admin_package.value.lower()
    domain_path_str = str(domain_path)

    print(f"Verifying executable: '{pkg_name}'...")
    pkg_exe_path = find_executable_func(pkg_name)
    
    if pkg_exe_path is None:
        raise FileNotFoundError(f"Executable '{pkg_name}' not found.")

    print(f"Found executable at: {pkg_exe_path}")

    print("\nStep 1: Initializing Node.js project...")
    runner.run([pkg_exe_path, "init", "-y"], cwd=domain_path_str)

    print("\nStep 2: Installing main dependencies (prisma, auth)...")
    # Prisma para 'entities', bcrypt y jsonwebtoken para 'auth'
    # pg es el driver de postgres
    main_deps = ["@prisma/client", "pg", "bcrypt", "jsonwebtoken"]
    if pkg_name == "yarn":
        runner.run([pkg_exe_path, "add"] + main_deps, cwd=domain_path_str)
    else:
        runner.run([pkg_exe_path, "install"] + main_deps, cwd=domain_path_str)

    print("\nStep 3: Installing dev dependencies (typescript, vitest, prisma)...")
    dev_deps = ["prisma", "typescript", "vitest", "@types/node", "@types/bcrypt", "@types/jsonwebtoken"]
    if pkg_name == "yarn":
        runner.run([pkg_exe_path, "add", "-D"] + dev_deps, cwd=domain_path_str)
    else:
        runner.run([pkg_exe_path, "install", "-D"] + dev_deps, cwd=domain_path_str)

    print("\nStep 4: Initializing Prisma with PostgreSQL...")
    npx_exe_path = find_executable_func("npx")
    if npx_exe_path is None:
        raise FileNotFoundError("Executable 'npx' not found, required for Prisma.")
        
    runner.run([npx_exe_path, "prisma", "init", "--datasource-provider", "postgresql"], cwd=domain_path_str)

    print("\nStep 5: Creating domain source structure...")
    src_path = domain_path / "src"
    file_manager.create_folder(str(src_path))
    file_manager.create_file(str(src_path / "index.ts"), "// Domain entry point\n")
    
    folders = ["entities", "services", "use_cases", "auth"]
    for folder in folders:
        folder_path = src_path / folder
        file_manager.create_folder(str(folder_path))
        file_manager.create_file(str(folder_path / ".gitkeep"), "")

    print(f"\nNode.js (Domain) package configured successfully at: {domain_path}")