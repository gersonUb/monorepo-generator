from pathlib import Path
from typing import Callable, Optional
from ...services.command_runner import CommandRunner
from ...core.interfaces.file_manager_interface import IFileManager
from ...core.models.project_config import ProjectConfig

FinderFunc = Callable[[str], Optional[str]]

def create_node_project(
    api_path: Path,
    file_manager: IFileManager,
    runner: CommandRunner,
    config: ProjectConfig,
    find_executable_func: FinderFunc
):
    pkg_name = config.admin_package.value.lower()
    api_path_str = str(api_path)

    print(f"Verifying executable: '{pkg_name}'...")
    pkg_exe_path = find_executable_func(pkg_name)
    
    if pkg_exe_path is None:
        print(f"❌ FATAL: Could not find '{pkg_name}' executable.")
        raise FileNotFoundError(f"Executable '{pkg_name}' not found.")

    print(f"Found executable at: {pkg_exe_path}")

    print("\nStep 1: Initializing Node.js project...")
    runner.run([pkg_exe_path, "init", "-y"], cwd=api_path_str)

    print("\nStep 2: Installing main dependencies (express)...")
    if pkg_name == "yarn":
        runner.run([pkg_exe_path, "add", "express"], cwd=api_path_str)
    else:
        runner.run([pkg_exe_path, "install", "express"], cwd=api_path_str)

    print("\nStep 3: Installing dev dependencies (typescript, ts-node, nodemon, @types)...")
    dev_deps = ["typescript", "ts-node", "nodemon", "@types/node", "@types/express"]
    if pkg_name == "yarn":
        runner.run([pkg_exe_path, "add", "-D"] + dev_deps, cwd=api_path_str)
    else:
        runner.run([pkg_exe_path, "install", "-D"] + dev_deps, cwd=api_path_str)

    print("\nStep 4: Creating source files (src/index.ts)...")
    src_path = api_path / "src"
    file_manager.create_folder(str(src_path))
    
    index_ts_content = (
        "import express from 'express';\n\n"
        "const app = express();\n"
        "const port = process.env.PORT || 8000;\n\n"
        "app.get('/', (req, res) => {\n"
        "  res.send('Hello from Express!');\n"
        "});\n\n"
        "app.listen(port, () => {\n"
        "  console.log(`Server running at http://localhost:${port}`);\n"
        "});\n"
    )
    file_manager.create_file(str(src_path / "index.ts"), index_ts_content)

    print("\nStep 5: Creating tsconfig.json...")
    tsconfig_content = (
        "{\n"
        "  \"compilerOptions\": {\n"
        "    \"target\": \"es6\",\n"
        "    \"module\": \"commonjs\",\n"
        "    \"outDir\": \"./dist\",\n"
        "    \"rootDir\": \"./src\",\n"
        "    \"strict\": true,\n"
        "    \"esModuleInterop\": true,\n"
        "    \"skipLibCheck\": true\n"
        "  },\n"
        "  \"include\": [\"src/**/*\"],\n"
        "  \"exclude\": [\"node_modules\"]\n"
        "}\n"
    )
    file_manager.create_file(str(api_path / "tsconfig.json"), tsconfig_content)
    
    print(f"\nNode.js (Express) backend configured successfully at: {api_path}")