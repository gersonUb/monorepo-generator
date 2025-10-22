from core.interfaces.file_manager_interface import FileManager;

class MonorepoBootstrapper:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.file_manager = FileManager(project_name)
