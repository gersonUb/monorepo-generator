import subprocess
from typing import List

class CommandRunner:
    @staticmethod
    def run(command: List[str], cwd: str): 
            try:
                description = f"Running: {' '.join(command)}"
                print(f"{description} in {cwd}")
                
                subprocess.run(
                    command, 
                    check=True, 
                    cwd=cwd, 
                    text=True, 
                    capture_output=False
                )
                print(f"Success in execution {command[0]}.")
                
            except FileNotFoundError:
                program_name = command[0]
                print(f"Error: The program '{program_name}' was not found on your system.")
                raise
                
            except subprocess.CalledProcessError as e:
                print(f"Error during execution of {command[0]}.")
                print(f"The process ended with return code:{e.returncode}")
                raise