# Plataforma de Apuestas Deportivas con IA

Esta es una plataforma web para analizar encuentros deportivos usando OpenAI (GPT-4) o Google Gemini Pro Vision.

## Instalación en cPanel / VPS

1. **Subir Archivos:** Sube todos los archivos a tu carpeta raíz de la aplicación (ej: `public_html` o la carpeta de la app Python).
2. **Configurar Python:**
    - En cPanel, ve a "Setup Python App".
    - Crea una nueva aplicación.
    - Selecciona la versión de Python recomendada (3.9+).
    - El "Application startup file" debe ser `passenger_wsgi.py`.
    - La "Application Entry point" debe ser `application`.
3. **Instalar Dependencias:**
    - En la terminal virtual o vía SSH, entra a la carpeta de tu app.
    - Ejecuta: `pip install -r requirements.txt`
4. **Instalar Base de Datos:**
    - Ejecuta: `python install.py`
    - Esto creará la base de datos `sports_ai.db` y el usuario **admin** con contraseña **admin123**.

## Uso

1. Entra a tu dominio.
2. Logueate con `admin` / `admin123`.
3. Ve a la sección **Admin** (en el menú superior) y configura tus API Keys de OpenAI o Google Gemini.
4. Ve al **Dashboard** y sube una imagen con los partidos del día o escribe tu consulta.
5. La IA analizará la información y te dará predicciones.

## Migración

Para migrar a otro servidor, solo necesitas copiar toda la carpeta, incluyendo el archivo `sports_ai.db` (que contiene tus datos) y la carpeta `static/uploads`.
