import subprocess
from typing import List

class CommandRunner:
    
    def run(self, command: List[str], cwd: str = ".", input_text: str = None):
        print(f" Running: {' '.join(command)}  (in directory: {cwd})")
        
        try:
            subprocess.run(
                command, 
                cwd=cwd, 
                check=True,
                text=True,
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