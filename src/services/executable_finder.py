import os
import shutil
from pathlib import Path
from typing import Optional

def find_executable(name: str) -> Optional[str]:
    """
    Finds an executable in common locations, bypassing a broken PATH.
    """
    path_from_which = shutil.which(name)
    if path_from_which:
        return path_from_which

    program_files = os.environ.get("ProgramFiles", "C:\\Program Files")
    node_dir = Path(program_files) / "nodejs"
    exe_path_pf = node_dir / f"{name}.cmd"
    
    if exe_path_pf.exists():
        return str(exe_path_pf)

    appdata = os.environ.get("APPDATA")
    if appdata:
        npm_global_dir = Path(appdata) / "npm"
        exe_path_appdata = npm_global_dir / f"{name}.cmd"
        if exe_path_appdata.exists():
            return str(exe_path_appdata)

    if name == "poetry":
        local_appdata = os.environ.get("LOCALAPPDATA")
        if local_appdata:
            poetry_bin = Path(local_appdata) / "pypoetry" / "venv" / "Scripts" / "poetry.exe"
            if poetry_bin.exists():
                return str(poetry_bin)
                
    return None