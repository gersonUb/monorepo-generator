from typing import Dict, Any

def base_template(project_name: str) -> Dict[str, Any]:
    return {
        project_name: {
            "api": None,
            "domain": None,
        }
    }
