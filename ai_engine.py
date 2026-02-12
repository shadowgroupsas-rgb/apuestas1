import base64
import json
import os
from openai import OpenAI
import google.generativeai as genai
from PIL import Image

class SportsAI:
    def __init__(self):
        # 2026 Model Mapping
        self.MODEL_MAPPING = {
            'openai': 'gpt-4o', # Fallback for 'GPT-5' until public API access
            'gemini': 'gemini-1.5-pro' # Fallback for 'Gemini 3.0' until public API access
        }

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze(self, input_type, input_content, settings):
        """
        Main entry point for analysis.
        input_type: 'text' or 'image'
        input_content: text string or image path
        settings: Settings object from DB
        """
        system_prompt = settings.system_prompt or """
        Eres un experto analista de apuestas deportivas y deportes. Tu trabajo es analizar la información proporcionada (imágenes de partidos, cuotas, o texto) y generar un reporte detallado.

        Debes buscar y proporcionar para cada encuentro identificado:
        1. Alineaciones probables (si es posible inferir o conocer).
        2. Bajas/Lesiones importantes.
        3. Ventajas y desventajas de cada equipo.
        4. Underdogs (equipos no favoritos) con potencial.
        5. Probabilidades de victoria (%).
        6. Sugerencias de apuestas (Ganador, Más/Menos goles, Primer gol).
        7. Posibles Parleys (combinadas) de alto valor.

        Formato de respuesta deseado: JSON con la estructura:
        {
            "matches": [
                {
                    "teams": "Equipo A vs Equipo B",
                    "analysis": "Análisis detallado...",
                    "prediction": "Gana Equipo A",
                    "confidence": "85%",
                    "betting_tips": ["Tip 1", "Tip 2"]
                }
            ],
            "parlay_suggestions": ["Parlay 1...", "Parlay 2..."]
        }
        Si no puedes devolver JSON, devuelve un reporte estructurado en Markdown limpio.
        """

        if settings.default_provider == 'openai':
            return self._analyze_openai(input_type, input_content, settings.openai_api_key, system_prompt)
        elif settings.default_provider == 'gemini':
            return self._analyze_gemini(input_type, input_content, settings.gemini_api_key, system_prompt)
        else:
            return {"error": "Proveedor de IA no configurado."}

    def _analyze_openai(self, input_type, input_content, api_key, system_prompt):
        if not api_key:
            return {"error": "API Key de OpenAI no configurada."}

        client = OpenAI(api_key=api_key)

        messages = [
            {"role": "system", "content": system_prompt}
        ]

        if input_type == 'text':
            messages.append({"role": "user", "content": input_content})
        elif input_type == 'image':
            base64_image = self.encode_image(input_content)
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analiza esta imagen de eventos deportivos y dame las predicciones."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            })

        try:
            model = self.MODEL_MAPPING.get('openai', 'gpt-4o')
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": str(e), "raw_response": "Error al procesar con OpenAI"}

    def _analyze_gemini(self, input_type, input_content, api_key, system_prompt):
        if not api_key:
            return {"error": "API Key de Gemini no configurada."}

        genai.configure(api_key=api_key)

        # Setup the model
        generation_config = {
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": 4096,
        }

        model_name = self.MODEL_MAPPING.get('gemini', 'gemini-1.5-pro')
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            system_instruction=system_prompt
        )

        try:
            if input_type == 'text':
                response = model.generate_content(input_content)
            elif input_type == 'image':
                img = Image.open(input_content)
                response = model.generate_content(["Analiza esta imagen de eventos deportivos y dame las predicciones en formato JSON.", img])

            # Gemini sometimes returns markdown wrapped JSON
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                 text = text.split("```")[1].split("```")[0]

            return json.loads(text)
        except Exception as e:
             # Fallback if not JSON
            raw_text = "Error desconocido"
            if 'response' in locals() and hasattr(response, 'text'):
                raw_text = response.text
            return {"raw_text": raw_text, "error": f"Error al procesar o formato no JSON: {str(e)}"}
