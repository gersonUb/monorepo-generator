import subprocess
import os
from typing import List

class CommandRunner:
    def run(self, command: List[str], cwd: str = ".", input_text: str = None):
        env_vars = os.environ.copy()
        env_vars["PYTHON_KEYRING_BACKEND"] = "keyring.backends.null.Keyring"
        print(f" Running: {' '.join(command)}  (in directory: {cwd})")
        
        try:
            subprocess.run(
                command, 
                cwd=cwd, 
                check=True,
                text=True,
                env=env_vars,
                input=input_text
            )

        except subprocess.CalledProcessError as e:
            print(f"❌ Command execution failed! ❌")
            print(f"Command: {e.cmd}")
            print(f"Return Code: {e.returncode}")
            raise e
            
        except FileNotFoundError as e:
            print(f"❌ Error! Command not found: {command[0]}")
            print("Please ensure the tool is installed and in your system PATH.")
            raise e