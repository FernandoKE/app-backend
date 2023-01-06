# Plantilla para proyecto full stack FastAPI + Vue

# ¿Qué contiene?
- Archivos de configuración de proyecto con todas las dependencias esenciales, tanto en backend como en frontend
- Estructura básica del proyecto en lo que respecta a directorios y archivos
- Algunas configuraciones de uso común

# ¿Cómo utilizarla?
- Inicializar backend:
  ```bash
  cd app-backend
  poetry install
  cp env.example .env  # y modificar .env según corresponda

  # iniciar el servidor
  poetry run poe start
  ```
- Inicializar frontend
  ```bash
  cd app-frontend
  pnpm install

  # iniciar el servidor
  pnpm dev
  ```

# Consideraciones
- Buscar los comentarios que empiezan con `TODO:`, y completar la implementación.
- Para abrir simultáneamente backend y frontend en la misma ventana de VS Code sin tener problemas de resolución de dependencias:
  - Abrir primero el directorio del `app-backend` en VS Code.
  - Ir a `File > Add Folder to Workspace`, y seleccionar el directorio del `app-frontend`.
  - Con esto aparecerán dos secciones en el navegador de archivos, que actúan de forma independiente.