import json
import logging
from datetime import datetime

import httpx

logger = logging.getLogger(__name__)


class MemoriaAfectiva:
    """
    Sistema de memoria que usa Ministral para analizar y extraer
    información relevante de las conversaciones de forma inteligente.
    """

    PROMPT_ANALISIS = """Analiza esta conversación y extrae información clave en formato JSON:

Conversación:
{conversacion}

Extrae SOLO si está presente:
- temas_principales: lista de temas discutidos (ej: ["trabajo", "familia"])
- emociones_detectadas: emociones del usuario (ej: ["feliz", "preocupado"])
- entidades_importantes: nombres, lugares, fechas mencionadas (ej: ["María", "Madrid"])
- intenciones: qué quiere el usuario (ej: ["consejo", "desahogo"])
- datos_personales: información personal revelada (ej: "estudia medicina")
- nivel_urgencia: 1-5, qué tan importante es recordar esto

Responde SOLO con JSON válido, sin explicaciones."""

    PROMPT_BUSQUEDA = """Dada esta consulta del usuario y estos recuerdos previos,
indica cuáles son relevantes (responde con los números separados por comas, o "ninguno"):

Consulta: {consulta}

Recuerdos:
{recuerdos}

Números relevantes:"""

    def __init__(
        self, token: str, modelo: str = "mistral-small-latest", max_recuerdos: int = 50
    ):
        self.token = token
        self.modelo = modelo
        self.max_recuerdos = max_recuerdos
        self.recuerdos = []

        self.http_client = httpx.AsyncClient(
            timeout=30.0, headers={"Authorization": f"Bearer {token}"}
        )

    async def _llamar_ministral(self, prompt: str, max_tokens: int = 300) -> str:
        """Hace una llamada ligera a Ministral para análisis"""
        try:
            response = await self.http_client.post(
                "https://api.mistral.ai/v1/chat/completions",
                json={
                    "model": self.modelo,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": 0.3,  # Baja para respuestas más consistentes
                },
            )

            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
            else:
                logger.error(f"Error en llamada a Ministral: {response.status_code}")
                return ""

        except Exception as e:
            logger.error(f"Excepción en _llamar_ministral: {e}")
            return ""

    async def analizar_y_guardar(
        self, usuario_msg: str, lunita_msg: str, emocion_lunita: str
    ) -> dict:
        """
        Analiza la conversación con IA y guarda un recuerdo estructurado
        """
        conversacion = f"Usuario: {usuario_msg}\nLunita: {lunita_msg}"

        # Llamar a Ministral para extraer información
        prompt = self.PROMPT_ANALISIS.format(conversacion=conversacion)
        respuesta = await self._llamar_ministral(prompt, max_tokens=400)

        # Parsear el JSON de respuesta
        try:
            analisis = json.loads(respuesta)
        except json.JSONDecodeError:
            logger.warning("No se pudo parsear respuesta de análisis, usando fallback")
            analisis = self._analisis_fallback(usuario_msg)

        # Crear recuerdo enriquecido
        recuerdo = {
            "timestamp": datetime.now(),
            "conversacion_original": {
                "usuario": usuario_msg[:200],  # Truncar para ahorrar espacio
                "lunita": lunita_msg[:200],
            },
            "analisis": analisis,
            "emocion_lunita": emocion_lunita,
            "relevancia": analisis.get("nivel_urgencia", 3) / 5.0,  # Normalizar a 0-1
            "veces_recordado": 0,
        }

        self.recuerdos.append(recuerdo)

        # Limitar tamaño
        if len(self.recuerdos) > self.max_recuerdos:
            self._consolidar_recuerdos()

        logger.info(
            f"Recuerdo analizado y guardado. Temas: {analisis.get('temas_principales', [])}"
        )
        return recuerdo

    def _analisis_fallback(self, texto: str) -> dict:
        """Análisis básico si falla la IA"""
        texto_lower = texto.lower()

        # Detección simple de emociones
        emociones_pos = ["feliz", "alegre", "bien", "genial", "contento"]
        emociones_neg = ["triste", "mal", "enojado", "frustrado", "preocupado"]

        emociones = []
        if any(e in texto_lower for e in emociones_pos):
            emociones.append("positivo")
        if any(e in texto_lower for e in emociones_neg):
            emociones.append("negativo")

        return {
            "temas_principales": ["general"],
            "emociones_detectadas": emociones or ["neutral"],
            "entidades_importantes": [],
            "nivel_urgencia": 2,
        }

    async def buscar_recuerdos_relevantes(
        self, mensaje_actual: str, limite: int = 3, usar_ia: bool = True
    ) -> list[dict]:
        """
        Busca recuerdos relevantes, opcionalmente usando IA para mejor precisión
        """
        if not self.recuerdos:
            return []

        if usar_ia and len(self.recuerdos) <= 20:
            # Si hay pocos recuerdos, usar IA para búsqueda precisa
            return await self._buscar_con_ia(mensaje_actual, limite)
        else:
            # Búsqueda rápida por keywords
            return self._buscar_por_keywords(mensaje_actual, limite)

    async def _buscar_con_ia(self, mensaje: str, limite: int) -> list[dict]:
        """Usa Ministral para identificar recuerdos relevantes"""
        # Crear texto con recuerdos numerados
        recuerdos_texto = []
        for i, rec in enumerate(self.recuerdos[-20:], 1):  # Solo últimos 20
            resumen = f"{i}. {rec['analisis'].get('temas_principales', [])} - "
            resumen += rec["conversacion_original"]["usuario"][:80]
            recuerdos_texto.append(resumen)

        prompt = self.PROMPT_BUSQUEDA.format(
            consulta=mensaje, recuerdos="\n".join(recuerdos_texto)
        )

        respuesta = await self._llamar_ministral(prompt, max_tokens=50)

        # Parsear números de respuesta
        try:
            if "ninguno" in respuesta.lower():
                return []

            indices = [
                int(n.strip()) - 1 for n in respuesta.split(",") if n.strip().isdigit()
            ]
            indices = [i for i in indices if 0 <= i < len(self.recuerdos[-20:])]

            # Obtener recuerdos seleccionados
            base_idx = max(0, len(self.recuerdos) - 20)
            recuerdos_seleccionados = [
                self.recuerdos[base_idx + i] for i in indices[:limite]
            ]

            # Incrementar contador de uso
            for rec in recuerdos_seleccionados:
                rec["veces_recordado"] += 1
                rec["relevancia"] = min(1.0, rec["relevancia"] + 0.1)

            return recuerdos_seleccionados

        except Exception as e:
            logger.error(f"Error en búsqueda con IA: {e}")
            return self._buscar_por_keywords(mensaje, limite)

    def _buscar_por_keywords(self, mensaje: str, limite: int) -> list[dict]:
        """Búsqueda rápida sin IA"""
        mensaje_lower = mensaje.lower()
        palabras_clave = set(mensaje_lower.split())

        puntuaciones = []

        for rec in self.recuerdos:
            puntos = 0.0

            # Coincidencia de temas
            temas = rec["analisis"].get("temas_principales", [])
            for tema in temas:
                if tema.lower() in mensaje_lower:
                    puntos += 3.0

            # Coincidencia de entidades
            entidades = rec["analisis"].get("entidades_importantes", [])
            for entidad in entidades:
                if entidad.lower() in mensaje_lower:
                    puntos += 5.0

            # Coincidencia de palabras
            texto_rec = rec["conversacion_original"]["usuario"].lower()
            palabras_rec = set(texto_rec.split())
            coincidencias = palabras_clave & palabras_rec
            puntos += len(coincidencias) * 0.3

            # Bonus por relevancia y uso previo
            puntos *= rec["relevancia"]
            puntos += rec["veces_recordado"] * 0.5

            if puntos > 0:
                puntuaciones.append((puntos, rec))

        # Ordenar y devolver mejores
        puntuaciones.sort(reverse=True, key=lambda x: x[0])
        return [r[1] for r in puntuaciones[:limite]]

    def _consolidar_recuerdos(self):
        """Mantiene los recuerdos más importantes"""
        # Ordenar por relevancia, uso y fecha
        self.recuerdos.sort(
            key=lambda r: (r["relevancia"], r["veces_recordado"], r["timestamp"]),
            reverse=True,
        )

        self.recuerdos = self.recuerdos[: self.max_recuerdos]

    def generar_contexto_para_prompt(self, recuerdos_relevantes: list[dict]) -> str:
        """Genera contexto legible para incluir en el prompt de Lunita"""
        if not recuerdos_relevantes:
            return ""

        lineas = ["[RECUERDOS RELEVANTES]:"]

        for i, rec in enumerate(recuerdos_relevantes, 1):
            fecha = rec["timestamp"].strftime("%d/%m")
            temas = ", ".join(rec["analisis"].get("temas_principales", []))
            texto_usuario = rec["conversacion_original"]["usuario"][:100]

            lineas.append(f"{i}. ({fecha}) Temas: {temas}")
            lineas.append(f'   Usuario dijo: "{texto_usuario}..."')

        return "\n".join(lineas)

    def obtener_perfil_usuario(self) -> dict:
        """Construye un perfil del usuario basado en todos los recuerdos"""
        if not self.recuerdos:
            return {}

        # Agregar temas
        todos_los_temas = []
        todas_las_emociones = []
        todas_las_entidades = []

        for rec in self.recuerdos:
            todos_los_temas.extend(rec["analisis"].get("temas_principales", []))
            todas_las_emociones.extend(rec["analisis"].get("emociones_detectadas", []))
            todas_las_entidades.extend(rec["analisis"].get("entidades_importantes", []))

        # Contar frecuencias
        from collections import Counter

        return {
            "temas_frecuentes": Counter(todos_los_temas).most_common(5),
            "emociones_comunes": Counter(todas_las_emociones).most_common(3),
            "entidades_mencionadas": Counter(todas_las_entidades).most_common(5),
            "total_conversaciones": len(self.recuerdos),
        }

    async def close(self):
        """Cierra el cliente HTTP"""
        await self.http_client.aclose()
