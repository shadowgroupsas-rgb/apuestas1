# Plataforma de Apuestas Deportivas con IA

Esta es una plataforma web para analizar encuentros deportivos usando OpenAI (GPT-4) o Google Gemini Pro Vision. Incluye un dashboard con tema oscuro y alimentación de datos de partidos en vivo.

## Características

- **Análisis con IA:** Predicciones, alineaciones y parleys usando ChatGPT o Gemini.
- **Dashboard en Vivo:** Visualización de partidos del día (Fútbol, NBA, MLB).
- **Tema Oscuro:** Interfaz profesional estilo "Casa de Apuestas".
- **Auto-instalable:** Script de instalación de base de datos incluido.

## Instalación en cPanel / VPS

1. **Subir Archivos:** Sube todos los archivos a tu carpeta raíz de la aplicación (ej: `public_html` o la carpeta de la app Python).
2. **Configurar Python:**
    - En cPanel, ve a "Setup Python App".
    - Crea una nueva aplicación.
    - Selecciona la versión de Python recomendada (3.10+).
    - El "Application startup file" debe ser `passenger_wsgi.py`.
    - La "Application Entry point" debe ser `application`.
3. **Instalar Dependencias:**
    - En la terminal virtual o vía SSH, entra a la carpeta de tu app.
    - Ejecuta: `pip install -r requirements.txt`
4. **Instalar Base de Datos:**
    - Ejecuta: `python install.py`
    - Esto creará la base de datos (carpeta `instance/sports_ai.db`) y el usuario **admin** con contraseña **admin123**.

## Uso

1. Entra a tu dominio.
2. Logueate con `admin` / `admin123`.
3. Ve a la sección **Admin** (en el menú lateral) y configura tus API Keys de OpenAI o Google Gemini.
4. En el **Dashboard**, verás los partidos del día. Haz clic en el rayo (⚡) para analizar un partido específico.
5. También puedes subir capturas de pantalla de casas de apuestas para que la IA las analice.

## Migración

Para migrar a otro servidor, solo necesitas copiar toda la carpeta, incluyendo la carpeta `instance/` (que contiene tu base de datos) y `static/uploads`.
