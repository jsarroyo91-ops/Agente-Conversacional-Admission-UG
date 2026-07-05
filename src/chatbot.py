"""
Módulo del motor conversacional del Agente Conversacional UG.


Etapas:
1. Detección de intención mediante similitud coseno.
2. Umbral de confianza y respuesta fallback para consultas no reconocidas.

Proyecto: Agente Conversacional para Admisión y Nivelación de la UG

Este módulo usa el preprocesamiento (src/preprocessing.py) y el modelo
TF-IDF (src/tfidf.py) ya construidos para:
1. Vectorizar cada consulta nueva del usuario.
2. Compararla mediante similitud coseno contra todas las utterances
   de entrenamiento del archivo data/intents.json.
3. Determinar la intención candidata (la de mayor similitud).
4. Aplicar un umbral de confianza: si la similitud máxima es menor al
   umbral, no se confía en la intención y se responde con un mensaje
   de fallback en lugar de arriesgar una respuesta incorrecta.
"""

import math
import random
from typing import Dict, List, Any

try:
    from tfidf import construir_modelo_tfidf, vectorizar_consulta
except ImportError:
    from src.tfidf import construir_modelo_tfidf, vectorizar_consulta


# Umbral mínimo de similitud coseno para aceptar una intención como válida.
# Si la similitud máxima encontrada es menor a este valor, se considera
# que el chatbot no tiene suficiente confianza y se usa el fallback.
UMBRAL_CONFIANZA = 0.3

# Cantidad mínima de términos (tokens preprocesados) que la consulta debe
# compartir con la utterance más parecida. Esta segunda condición evita
# falsos positivos: una sola palabra coincidente puede dar una similitud
# coseno alta si la utterance de entrenamiento es muy corta (ej. "hola"),
# sin que eso signifique que la consulta realmente pertenece a esa
# intención (ej. "futbol en guayaquil" no debería activar "saludo").
MIN_TOKENS_COMPARTIDOS = 2


def similitud_coseno(vector_a: Dict[str, float], vector_b: Dict[str, float]) -> float:
    """
    Calcula la similitud coseno entre dos vectores TF-IDF dispersos.

    Los vectores están representados como diccionarios {termino: peso},
    por lo que solo se recorren los términos presentes (no todo el
    vocabulario), lo cual es más eficiente para vectores dispersos.

    Fórmula:
        coseno(A, B) = (A · B) / (||A|| * ||B||)

    Args:
        vector_a (Dict[str, float]): vector TF-IDF de la consulta.
        vector_b (Dict[str, float]): vector TF-IDF de una utterance.

    Returns:
        float: valor de similitud entre 0 y 1. Devuelve 0 si alguno
        de los vectores está vacío (consulta sin términos conocidos).
    """
    if not vector_a or not vector_b:
        return 0.0

    # Producto punto: se recorre solo el vector más pequeño por eficiencia.
    if len(vector_a) > len(vector_b):
        vector_a, vector_b = vector_b, vector_a

    producto_punto = sum(
        peso * vector_b[termino]
        for termino, peso in vector_a.items()
        if termino in vector_b
    )

    norma_a = math.sqrt(sum(peso ** 2 for peso in vector_a.values()))
    norma_b = math.sqrt(sum(peso ** 2 for peso in vector_b.values()))

    if norma_a == 0 or norma_b == 0:
        return 0.0

    return producto_punto / (norma_a * norma_b)


def contar_tokens_compartidos(vector_a: Dict[str, float], vector_b: Dict[str, float]) -> int:
    """
    Cuenta cuántos términos (tokens) tienen en común dos vectores TF-IDF.

    Esta señal complementa la similitud coseno: una consulta de una sola
    palabra puede dar coseno = 1.0 con una utterance corta sin que eso
    signifique realmente que la consulta pertenece a esa intención (por
    ejemplo, una palabra suelta que coincide por casualidad). Exigir un
    mínimo de tokens compartidos evita ese tipo de falso positivo.

    Args:
        vector_a (Dict[str, float]): vector TF-IDF de la consulta.
        vector_b (Dict[str, float]): vector TF-IDF de una utterance.

    Returns:
        int: cantidad de términos presentes en ambos vectores.
    """
    return len(set(vector_a.keys()) & set(vector_b.keys()))


def detectar_intencion(consulta: str, modelo: Dict[str, Any]) -> Dict[str, Any]:
    """
    Detecta la intención candidata de una consulta mediante similitud coseno.

    Compara el vector TF-IDF de la consulta contra el vector TF-IDF de
    cada utterance de entrenamiento y se queda con la intención (tag)
    de la utterance más parecida.

    Args:
        consulta (str): texto escrito por el usuario.
        modelo (Dict[str, Any]): modelo TF-IDF construido con construir_modelo_tfidf().

    Returns:
        Dict[str, Any]: diccionario con:
            - consulta_original
            - consulta_preprocesada
            - tag_candidato
            - similitud_maxima
            - utterance_mas_parecida
            - ranking (lista de las 3 mejores coincidencias, para depuración)
    """
    resultado_vectorizacion = vectorizar_consulta(consulta, modelo)
    vector_consulta = resultado_vectorizacion["vector_tfidf"]

    similitudes = []

    for registro, vector_utterance in zip(modelo["registros"], modelo["matriz_tfidf"]):
        score = similitud_coseno(vector_consulta, vector_utterance)
        tokens_compartidos = contar_tokens_compartidos(vector_consulta, vector_utterance)
        similitudes.append({
            "tag": registro["tag"],
            "utterance_original": registro["utterance_original"],
            "similitud": score,
            "tokens_compartidos": tokens_compartidos
        })

    # Se ordena de mayor a menor similitud.
    similitudes.sort(key=lambda item: item["similitud"], reverse=True)

    if similitudes:
        mejor = similitudes[0]
        tag_candidato = mejor["tag"]
        similitud_maxima = mejor["similitud"]
        utterance_mas_parecida = mejor["utterance_original"]
        tokens_compartidos_max = mejor["tokens_compartidos"]
    else:
        tag_candidato = "fallback"
        similitud_maxima = 0.0
        utterance_mas_parecida = None
        tokens_compartidos_max = 0

    return {
        "consulta_original": consulta,
        "consulta_preprocesada": resultado_vectorizacion["consulta_preprocesada"],
        "tag_candidato": tag_candidato,
        "similitud_maxima": similitud_maxima,
        "tokens_compartidos": tokens_compartidos_max,
        "utterance_mas_parecida": utterance_mas_parecida,
        "ranking": similitudes[:3]
    }


# Intenciones "conversacionales" cuyas utterances de entrenamiento son muy
# cortas (1 o 2 palabras), como "hola" o "gracias". Para estas intenciones
# se acepta un solo token compartido, porque la utterance de entrenamiento
# en sí misma es así de corta.
INTENTS_CONVERSACIONALES_CORTOS = {"saludo", "despedida"}

# Raíces distintivas que permiten aceptar una intención conversacional con
# un solo token compartido. Esto evita que palabras genéricas como "noche"
# o "más" activen saludo/despedida en consultas fuera del dominio.
MARCADORES_CONVERSACIONALES = {
    "saludo": {"hola", "buen", "salud", "ayud", "orient", "apoy"},
    "despedida": {"graci", "adi", "lueg", "pront", "vem", "resolv", "agradez"}
}


def aplicar_umbral_confianza(
    deteccion: Dict[str, Any],
    umbral: float = UMBRAL_CONFIANZA,
    min_tokens: int = MIN_TOKENS_COMPARTIDOS
) -> Dict[str, Any]:
    """
    Aplica el umbral de confianza sobre el resultado de detectar_intencion().

    Se usan dos condiciones combinadas para aceptar la intención candidata:

    1. La similitud coseno máxima debe ser mayor o igual al umbral.
    2. La consulta y la utterance ganadora deben compartir al menos
       `min_tokens` términos (después del preprocesamiento), EXCEPTO si
       la intención candidata es conversacional corta (saludo/despedida),
       donde se acepta con un solo token porque sus utterances de
       entrenamiento también son cortas (ej. "hola", "gracias").

    La segunda condición es necesaria porque, con vectores TF-IDF, una
    sola palabra en común con una utterance de entrenamiento corta puede
    producir una similitud coseno alta sin que exista relación real entre
    la consulta y esa intención (ej. "Cuánto es 25 más 17" puede coincidir
    por casualidad con una sola palabra y dar coseno alto).

    Si cualquiera de las dos condiciones falla, la intención se reemplaza
    por "fallback".

    Args:
        deteccion (Dict[str, Any]): resultado de detectar_intencion().
        umbral (float): similitud coseno mínima para confiar en la intención.
        min_tokens (int): cantidad mínima de tokens compartidos exigida.

    Returns:
        Dict[str, Any]: el mismo diccionario de entrada, agregando:
            - tag_final
            - es_fallback
            - umbral_usado
    """
    supera_umbral_coseno = deteccion["similitud_maxima"] >= umbral

    tag_candidato = deteccion["tag_candidato"]
    es_intent_corto = tag_candidato in INTENTS_CONVERSACIONALES_CORTOS
    tokens_consulta = set(deteccion.get("consulta_preprocesada", "").split())
    marcadores = MARCADORES_CONVERSACIONALES.get(tag_candidato, set())
    contiene_marcador_conversacional = bool(tokens_consulta & marcadores)

    # Saludo y despedida pueden aceptarse con una coincidencia cuando existe
    # un marcador inequívoco. De lo contrario se conservan los dos tokens
    # mínimos para evitar falsos positivos en consultas fuera del dominio.
    if es_intent_corto and contiene_marcador_conversacional:
        tokens_minimos_exigidos = 1
    else:
        tokens_minimos_exigidos = min_tokens

    supera_tokens_minimos = deteccion["tokens_compartidos"] >= tokens_minimos_exigidos
    es_fallback = not (supera_umbral_coseno and supera_tokens_minimos)

    deteccion["tag_final"] = "fallback" if es_fallback else deteccion["tag_candidato"]
    deteccion["es_fallback"] = es_fallback
    deteccion["umbral_usado"] = umbral

    return deteccion


def obtener_respuesta(tag: str, datos_intents: Dict[str, Any]) -> str:
    """
    Obtiene una respuesta aleatoria asociada a un tag de intención.

    Si el tag es "fallback" o no existe en intents.json, se usa la
    sección "fallback" definida en el propio archivo data/intents.json.

    Args:
        tag (str): intención final ya filtrada por el umbral de confianza.
        datos_intents (Dict[str, Any]): contenido completo de intents.json.

    Returns:
        str: una respuesta de ejemplo para el tag indicado.
    """
    for intent in datos_intents.get("intents", []):
        if intent.get("tag") == tag:
            respuestas = intent.get("responses", [])
            if respuestas:
                return random.choice(respuestas)

    # Si no se encontró el tag o no hay respuestas, se usa el fallback.
    fallback = datos_intents.get("fallback", {})
    respuestas_fallback = fallback.get(
        "responses",
        ["No logré identificar tu consulta. ¿Puedes reformularla?"]
    )
    return random.choice(respuestas_fallback)


def procesar_mensaje(
    consulta: str,
    modelo: Dict[str, Any],
    datos_intents: Dict[str, Any],
    umbral: float = UMBRAL_CONFIANZA
) -> Dict[str, Any]:
    """
    Ejecuta el flujo completo: detección de intención + umbral + respuesta.

    Esta es la función principal que debe usar la interfaz (consola,
    Streamlit o Gradio) para conversar con el usuario.

    Args:
        consulta (str): mensaje escrito por el usuario.
        modelo (Dict[str, Any]): modelo TF-IDF ya construido.
        datos_intents (Dict[str, Any]): contenido de intents.json.
        umbral (float): umbral de confianza a aplicar.

    Returns:
        Dict[str, Any]: información de la detección más la respuesta final.
    """
    deteccion = detectar_intencion(consulta, modelo)
    deteccion = aplicar_umbral_confianza(deteccion, umbral)
    deteccion["respuesta"] = obtener_respuesta(deteccion["tag_final"], datos_intents)

    return deteccion


if __name__ == "__main__":
    from tfidf import cargar_intenciones

    print("PRUEBA DEL MOTOR DE DETECCIÓN DE INTENCIÓN (SIMILITUD COSENO)\n")

    modelo = construir_modelo_tfidf()
    datos_intents = cargar_intenciones()

    consultas_prueba = [
        "Hola, buenas tardes",
        "Qué documentos necesito para matricularme en nivelación",
        "Cuáles son las etapas del proceso de admisión",
        "Cómo está el clima hoy",  # debería caer en fallback
        "Gracias por la ayuda"
    ]

    for consulta in consultas_prueba:
        resultado = procesar_mensaje(consulta, modelo, datos_intents)

        print("=" * 80)
        print("Consulta:", resultado["consulta_original"])
        print("Tag candidato:", resultado["tag_candidato"])
        print("Similitud máxima: {:.4f}".format(resultado["similitud_maxima"]))
        print("¿Fallback?:", resultado["es_fallback"])
        print("Tag final:", resultado["tag_final"])
        print("Respuesta:", resultado["respuesta"])
        print()
