import os
import shutil
from pathlib import Path
from typing import Optional
from ..services.command_runner import CommandRunner
from ..core.interfaces.file_manager_interface import IFileManager
from ..core.models.project_config import ProjectConfig
from src.services.executable_finder import find_executable

def create_frontend(
    config: ProjectConfig, 
    file_manager: IFileManager, 
    runner: CommandRunner
):
    
    apps_dir = Path(config.name) / "apps"
    name = "frontend"
    template = f"{config.frontend.value}-ts"
    pkg_name = config.admin_package.value.lower()
    
    print(f"Verifying executable: '{pkg_name}'...")

    pkg_exe_path =find_executable(pkg_name)
    
    if pkg_exe_path is None:
        print(f"❌ FATAL: Could not find '{pkg_name}' executable.")
        print("Please ensure Node.js and/or Yarn are installed correctly.")
        raise FileNotFoundError(
            f"Executable '{pkg_name}' not found. Please install Node.js."
        )
    
    print(f"Found executable at: {pkg_exe_path}")

    target = apps_dir.resolve()
    
    if not target.exists():
        print(f"⚠️ Apps directory not found. Creating '{target}'...")
        file_manager.create_folder(str(target))

    frontend_path = target / name

    print("\nStep 1: Initializing Vite (React + TS)...")
    if pkg_name == "yarn":
        runner.run(
            [pkg_exe_path, "create", "vite", name, "--template", template], 
            str(target),
            input_text="\n"
        )
    else:
        runner.run(
            [pkg_exe_path, "create", "vite@latest", name, "--", "--template", template], 
            str(target)
        )

    print("\nStep 2: Installing base dependencies...")
    runner.run([pkg_exe_path], str(frontend_path))

    print("\nStep 3: Installing TailwindCSS and official @tailwindcss/vite plugin...")
    if pkg_name == "yarn":
        runner.run([pkg_exe_path, "add", "-D", "tailwindcss", "@tailwindcss/vite"], str(frontend_path))
    else:
        runner.run([pkg_exe_path, "install", "-D", "tailwindcss", "@tailwindcss/vite"], str(frontend_path))

    print("\nStep 4: Configuring vite.config.ts with Tailwind plugin...")
    vite_config_path = frontend_path / "vite.config.ts"

    if vite_config_path.exists():
        updated = (
            "import { defineConfig } from 'vite'\n"
            "import react from '@vitejs/plugin-react'\n"
            "import tailwindcss from '@tailwindcss/vite'\n\n"
            "export default defineConfig({\n"
            "  plugins: [react(), tailwindcss()],\n"
            "})\n"
        )
        file_manager.create_file(str(vite_config_path), updated)
    else:
        print("⚠️ vite.config.ts not found — skipping modification.")

    print("\nStep 5: Configuring main CSS file...")
    css_path = frontend_path / "src" / "index.css"
    file_manager.create_file(str(css_path), '@import "tailwindcss";\n')

    print(f"\nFrontend configured successfully at: {frontend_path}")
    print("Run `yarn dev` or `npm run dev` to start the development server.\n")