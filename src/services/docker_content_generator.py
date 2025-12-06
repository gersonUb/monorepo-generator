from pathlib import Path
from ..core.models.project_config import ProjectConfig, BackendFramework, Admin_package

class DockerContentGenerator:
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir

    def get_docker_compose_content(self, config: ProjectConfig) -> str:
        template_path = self.templates_dir / "compose.template"
        return self._read_and_replace(template_path, "{{PROJECT_NAME}}", config.name)

    def get_docker_compose_test_content(self, config: ProjectConfig) -> str:
        template_path = self.templates_dir / "compose.test.template"
        return self._read_and_replace(template_path, "{{PROJECT_NAME}}", config.name)

    def get_env_example_content(self) -> str:
        return (self.templates_dir / "env.example.template").read_text(encoding="utf-8")

    def get_dockerignore_content(self) -> str:
        return (self.templates_dir / "ignore.template").read_text(encoding="utf-8")

    def get_monolithic_dockerfile(self, config: ProjectConfig) -> str:
        """Genera un Dockerfile multi-stage unificado."""
        fe_part = self._get_frontend_dockerfile_part(config)
        be_part = self._get_backend_dockerfile_part(config)

        return f"""
# ==========================================
# MULTI-STAGE DOCKERFILE GENERATED AUTOMATICALLY
# ==========================================

{fe_part}

{be_part}
"""

    def _read_and_replace(self, path: Path, placeholder: str, value: str) -> str:
        """Helper para evitar repetir código de lectura y reemplazo."""
        content = path.read_text(encoding="utf-8")
        return content.replace(placeholder, value)

    def _get_frontend_dockerfile_part(self, config: ProjectConfig) -> str:
        template = (self.templates_dir / "dockerfile_frontend.template").read_text(encoding="utf-8")
        
        is_yarn = config.admin_package == Admin_package.YARN
        
        lock_file = "yarn.lock" if is_yarn else "package-lock.json"
        install_cmd = "yarn install" if is_yarn else "npm install"
        # Nota: npm requiere '--' para pasar argumentos al script
        run_cmd = "yarn dev --host 0.0.0.0" if is_yarn else "npm run dev -- --host 0.0.0.0"
        
        return template.replace(
            "{{LOCK_FILE}}", lock_file
        ).replace(
            "{{INSTALL_CMD}}", install_cmd
        ).replace(
            "{{RUN_CMD_LIST}}", run_cmd
        )

    def _get_backend_dockerfile_part(self, config: ProjectConfig) -> str:
        if config.backend == BackendFramework.FASTAPI:
            return (self.templates_dir / "dockerfile_backend_fastapi.template").read_text(encoding="utf-8")
        
        elif config.backend == BackendFramework.NODE:
            template = (self.templates_dir / "dockerfile_backend_node.template").read_text(encoding="utf-8")
            
            is_yarn = config.admin_package == Admin_package.YARN
            
            lock_file = "yarn.lock" if is_yarn else "package-lock.json"
            install_cmd = "yarn install" if is_yarn else "npm install"
            build_cmd = "yarn build" if is_yarn else "npm run build"

            return template.replace(
                "{{LOCK_FILE}}", lock_file
            ).replace(
                "{{INSTALL_CMD}}", install_cmd
            ).replace(
                "{{BUILD_CMD}}", build_cmd
            )
        
        return "# WARN: Backend framework not supported in Dockerfile generation"