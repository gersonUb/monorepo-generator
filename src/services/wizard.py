from typing import Callable, Any, Dict, List
from dataclasses import dataclass
from src.core.exceptions import UserGoBack

@dataclass
class WizardStep:
    key: str
    action: Callable[[Dict[str, Any]], Any]

class WizardRunner:
    def __init__(self):
        self.steps: List[WizardStep] = []
        self.context: Dict[str, Any] = {}

    def add_step(self, key: str, action: Callable[[Dict[str, Any]], Any]):
        """
        Register a new step.
        :param key: Dictionary key where to save the result.
        :param action: Function that receives the current context and returns the value.
        """
        self.steps.append(WizardStep(key, action))

    def run(self) -> Dict[str, Any]:
        current_index = 0
        total_steps = len(self.steps)

        while current_index < total_steps:
            step = self.steps[current_index]
            
            try:
                result = step.action(self.context)
                self.context[step.key] = result
                current_index += 1

            except UserGoBack:
                current_index -= 1
                if current_index < 0:
                    current_index = 0
        
        return self.context