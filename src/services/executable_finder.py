import os
import platform
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

    home = Path.home()
    system = platform.system().lower() 

    if system != 'windows':
        linux_local_bin = home / ".local" / "bin" / name
        if linux_local_bin.exists() and os.access(linux_local_bin, os.X_OK):
            return str(linux_local_bin)
    else:
        program_files = os.environ.get("ProgramFiles", "C:\\Program Files")
        node_pf = Path(program_files) / "nodejs" / f"{name}.cmd"
        if node_pf.exists(): return str(node_pf)

        appdata = os.environ.get("APPDATA")
        if appdata:
            npm_global = Path(appdata) / "npm" / f"{name}.cmd"
            if npm_global.exists(): return str(npm_global)

        if name == "poetry":
            local_appdata = os.environ.get("LOCALAPPDATA")
            if local_appdata:
                poetry_bin = Path(local_appdata) / "pypoetry" / "venv" / "Scripts" / "poetry.exe"
                if poetry_bin.exists(): return str(poetry_bin)

                poetry_bin_alt = Path(appdata) / "pypoetry" / "venv" / "Scripts" / "poetry.exe"
                if poetry_bin_alt.exists(): return str(poetry_bin_alt)

    return None