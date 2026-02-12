# Manual de Operación y Documentación Técnica - Sports AI

Este documento explica en detalle cómo instalar, configurar y entender la lógica operativa de la plataforma de IA para apuestas deportivas.

---

## 🚀 1. Instalación y Despliegue

### Opción A: Hosting Compartido (cPanel)
Esta es la opción más sencilla para principiantes.

1.  **Requisitos:**
    -   Hosting con soporte para **Python** (CloudLinux + Python Selector).
    -   Acceso a base de datos MySQL (opcional, por defecto usa SQLite que no requiere configuración).

2.  **Pasos:**
    -   Sube todos los archivos del repositorio a la carpeta raíz de tu dominio (ej: `public_html`).
    -   En cPanel, busca la opción **"Setup Python App"**.
    -   Crea una nueva aplicación:
        -   **Python Version:** Selecciona 3.9 o superior (3.12 recomendado).
        -   **App Directory:** La carpeta donde subiste los archivos.
        -   **App Domain:** Tu dominio.
        -   **Startup File:** Escribe `passenger_wsgi.py`.
        -   **Entry Point:** Escribe `application`.
    -   Haz clic en **Create**.
    -   Entra a la terminal virtual (o SSH) y ejecuta:
        ```bash
        pip install -r requirements.txt
        python install.py
        ```
    -   Reinicia la aplicación desde cPanel.
    -   Accede a tu dominio. El usuario por defecto es `admin` y la contraseña `admin123`.

### Opción B: Servidor VPS (Ubuntu/Debian)
Para mayor rendimiento y control.

1.  **Actualizar el servidor:**
    ```bash
    sudo apt update && sudo apt upgrade -y
    sudo apt install python3-pip python3-venv nginx
    ```

2.  **Clonar y Configurar:**
    ```bash
    git clone <tu-repo> /var/www/sports-ai
    cd /var/www/sports-ai
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python install.py
    ```

3.  **Configurar Gunicorn (Servidor de Aplicación):**
    -   Prueba que funcione: `gunicorn --bind 0.0.0.0:8000 app:app`
    -   (Opcional) Crea un servicio systemd para que inicie automático.

4.  **Configurar Nginx (Proxy Inverso):**
    -   Edita `/etc/nginx/sites-available/default` y añade:
        ```nginx
        server {
            listen 80;
            server_name tu-dominio.com;

            location / {
                proxy_pass http://127.0.0.1:8000;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
            }
        }
        ```
    -   Reinicia Nginx: `sudo systemctl restart nginx`.

---

## 🧠 2. Funcionamiento del Sistema

### Flujo de Datos (Data Pipeline)
1.  **Obtención de Partidos:**
    -   El módulo `sports_data.py` se conecta a APIs públicas de deportes (como los endpoints de ESPN) para obtener la cartelera del día en tiempo real.
    -   Estos datos (Equipos, Hora, Liga) se muestran en el Dashboard.

2.  **Solicitud de Análisis:**
    -   Cuando el usuario hace clic en "ANALIZAR PARTIDO" (o sube una imagen), el sistema empaqueta esta información en un **Prompt de Ingeniería**.
    -   El prompt incluye: Nombres de equipos, contexto del deporte y una instrucción estricta de actuar como experto en apuestas (Tipster Profesional).

3.  **Motor de Inteligencia Artificial (`ai_engine.py`):**
    -   El sistema consulta la base de datos para ver qué proveedor está activo (OpenAI GPT-5 o Gemini 3.0 Pro).
    -   Envía el prompt + datos al modelo seleccionado.
    -   Si es una imagen, la codifica en Base64 y la envía para visión por computadora (Computer Vision).

4.  **Procesamiento y Respuesta:**
    -   La IA analiza los datos basándose en su vasto conocimiento entrenado hasta 2024-2025.
    -   Devuelve un objeto JSON estructurado con predicciones, porcentajes y justificaciones.
    -   El Dashboard renderiza este JSON en tarjetas visuales modernas.

---

## 📊 3. Lógica de Pronósticos y Parleys

### Factores de Análisis
La IA no "adivina", sino que evalúa probabilidades basándose en múltiples vectores:

1.  **Forma Reciente:** Analiza (si se le provee en el texto o imagen) los últimos 5 partidos.
2.  **Alineaciones:** Busca jugadores clave lesionados o suspendidos (simulado por su conocimiento general o datos provistos).
3.  **Factor Localía:** Pondera fuertemente al equipo de casa en ciertas ligas (ej: NBA, MLS).
4.  **Historial H2H:** Enfrentamientos directos previos entre ambos equipos.

### Construcción de Parleys (Combinadas)
El sistema está instruido para buscar "Value Bets" (Apuestas de Valor) y combinarlas inteligentemente:

-   **Seguridad:** Combina 2 o 3 selecciones de alta probabilidad (>75%) para formar un parley seguro (Stake Alto).
-   **Correlación:** Evita combinar eventos contradictorios (ej: "Baja de goles" y "Ambos anotan").
-   **Underdogs:** Identifica equipos no favoritos que tienen ventajas tácticas específicas contra su rival de turno para sugerir sorpresas de alta cuota.

---

## 🛠 Mantenimiento

-   **Actualizar Modelos:** Ve a `/admin` para cambiar entre GPT-5 y Gemini 3.0 Pro según precios o rendimiento.
-   **Base de Datos:** El archivo `instance/sports_ai.db` contiene todo. Hazle backup regularmente.
