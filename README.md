#  Project Generator - Clean Architecture Monorepo

Una herramienta CLI interactiva para generar estructuras de proyectos robustas basadas en Clean Architecture, soportando múltiples frameworks de Frontend y Backend.

##  Requisitos Previos

* **Python 3.10** o superior.
* **Git** instalado.

---

##  Instalación y Uso

Sigue estos pasos para ejecutar la herramienta en tu entorno local. Se recomienda encarecidamente usar un **entorno virtual** para evitar conflictos con las librerías del sistema.

### 1. Clonar el repositorio

```bash
git clone [https://github.com/TU-USUARIO/monorepo-generator.git](https://github.com/TU-USUARIO/monorepo-generator.git)
cd monorepo-generator
```

### 2. Crear y Activar un Entorno Virtual (Recomendado)

Esto aísla las dependencias del proyecto y evita errores de permisos (especialmente en Linux/Ubuntu debido al PEP 668).

**En Windows:**
```bash
# Crear el entorno
python -m venv .venv

# Activar el entorno
.\.venv\Scripts\Activate
```

**En Linux / Mac:**
```bash
# Instalar venv (solo si es necesario en Ubuntu/Debian)
sudo apt install python3-venv

# Crear el entorno
python3 -m venv .venv

# Activar el entorno
source .venv/bin/activate
```

> 💡 **Nota:** Sabrás que el entorno está activo porque verás `(.venv)` al inicio de tu terminal.

### 3. Instalar Dependencias

Una vez activo el entorno virtual, instala las librerías necesarias (`InquirerPy`, `rich`, etc.) automáticamente usando el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Ejecutar el Generador

¡Listo! Ahora puedes iniciar la herramienta:

```bash
python main.py
```

---

##  Características Principales

* **Interfaz Interactiva:** Selección visual de opciones con soporte de mouse y teclado.
* **Arquitectura Limpia:** Genera una estructura de carpetas profesional tipo Monorepo.
* **Atomicidad (Rollback):** Si algo falla durante la creación (ej. error de red), el sistema limpia automáticamente los archivos parciales para mantener tu entorno limpio.
* **UI Moderna:** Feedback visual con barras de carga y colores gracias a la librería `Rich`.

## 📂 Estructura Generada

El generador crea un proyecto con la siguiente estructura base:

```text
my-project/
├── apps/
│   ├── frontend/         # (React/Vue/Angular + Vite)
│   └── api/              # (FastAPI/Node)
├── domain/               # Lógica de negocio compartida
├── docker-compose.yml    # Configuración de Docker
└── README.md
```

##  Contribución

Si deseas contribuir al código:

1. Haz un Fork del repositorio.
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`).
3. Si instalas nuevas librerías, actualiza el archivo de requisitos:
   ```bash
   pip freeze > requirements.txt
   ```
4. Haz Commit y Push de tus cambios.
5. Abre un Pull Request.
