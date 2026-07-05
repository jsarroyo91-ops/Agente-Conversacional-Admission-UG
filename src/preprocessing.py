"""
Preprocesamiento de texto para el Agente Conversacional UG.

Aplica normalización, corrección tipográfica básica, tokenización,
eliminación de stopwords y stemming en español.
"""

import re
import unicodedata
from typing import Dict, List

try:
    from nltk.corpus import stopwords
    from nltk.stem import SnowballStemmer
except ImportError:
    stopwords = None
    SnowballStemmer = None

PALABRAS_RELEVANTES = {
    "cuando",
    "donde"
}

STOPWORDS_RESPALDO = {
    "a", "al", "algo", "algunas", "algunos", "ante", "antes", "como", "con",
    "contra", "cual", "cuando", "de", "del", "desde", "donde", "durante",
    "e", "el", "ella", "ellas", "ellos", "en", "entre", "era", "erais",
    "eran", "eras", "eres", "es", "esa", "esas", "ese", "eso", "esos",
    "esta", "estaba", "estaban", "estado", "estas", "estamos", "estan",
    "estar", "este", "esto", "estos", "estoy", "fue", "fueron", "ha",
    "hace", "hacen", "hacer", "han", "hasta", "hay", "la", "las", "le",
    "les", "lo", "los", "me", "mi", "mis", "mucho", "muy", "no", "nos",
    "o", "otra", "otros", "para", "pero", "por", "porque", "que", "se",
    "sea", "ser", "si", "sin", "sobre", "son", "su", "sus", "te", "tiene",
    "tienen", "tu", "tus", "un", "una", "uno", "unos", "y", "ya"
}

# Correcciones controladas para errores frecuentes del dominio. No sustituye
# a un corrector ortográfico general; evita alterar palabras desconocidas.
CORRECCIONES_TIPOGRAFICAS = {
    "ofisiales": "oficiales",
    "ofisial": "oficial",
    "nasional": "nacional",
    "conosimientos": "conocimientos",
    "conosimiento": "conocimiento",
    "matrikula": "matricula",
    "nivellacion": "nivelacion",
    "postulasion": "postulacion",
    "inscripsion": "inscripcion",
    "evalucion": "evaluacion",
    "cronogama": "cronograma",
    "asiganacion": "asignacion"
}


def cargar_stopwords() -> set:
    """
    Carga las stopwords en español, conservando términos interrogativos
    relevantes para la detección de intenciones.
    """
    if stopwords is not None:
        try:
            stopwords_es = set(stopwords.words("spanish"))
        except LookupError:
            stopwords_es = set(STOPWORDS_RESPALDO)
    else:
        stopwords_es = set(STOPWORDS_RESPALDO)

    return stopwords_es - PALABRAS_RELEVANTES


def quitar_acentos(texto: str) -> str:
    texto_normalizado = unicodedata.normalize("NFD", texto)
    return "".join(
        caracter for caracter in texto_normalizado
        if unicodedata.category(caracter) != "Mn"
    )


def normalizar_texto(texto: str) -> str:
    if texto is None:
        return ""
    texto = quitar_acentos(str(texto).lower())
    texto = re.sub(r"http\S+|www\S+", " ", texto)
    texto = re.sub(r"\S+@\S+", " ", texto)
    texto = re.sub(r"[^a-zA-Z0-9ñÑ\s]", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def tokenizar(texto: str) -> List[str]:
    return texto.split() if texto else []


def corregir_errores_tipograficos(tokens: List[str]) -> List[str]:
    return [CORRECCIONES_TIPOGRAFICAS.get(token, token) for token in tokens]


def eliminar_stopwords(tokens: List[str]) -> List[str]:
    stopwords_es = cargar_stopwords()
    return [token for token in tokens if token not in stopwords_es and len(token) > 1]


def aplicar_stemming(tokens: List[str]) -> List[str]:
    if SnowballStemmer is None:
        return tokens
    stemmer = SnowballStemmer("spanish")
    return [stemmer.stem(token) for token in tokens]


def preprocesar_texto(texto: str, usar_stemming: bool = True) -> str:
    texto_normalizado = normalizar_texto(texto)
    tokens = corregir_errores_tipograficos(tokenizar(texto_normalizado))
    tokens = eliminar_stopwords(tokens)
    if usar_stemming:
        tokens = aplicar_stemming(tokens)
    return " ".join(tokens)


def explicar_preprocesamiento(texto: str, usar_stemming: bool = True) -> Dict[str, object]:
    texto_normalizado = normalizar_texto(texto)
    tokens = tokenizar(texto_normalizado)
    tokens_corregidos = corregir_errores_tipograficos(tokens)
    tokens_sin_stopwords = eliminar_stopwords(tokens_corregidos)
    tokens_finales = aplicar_stemming(tokens_sin_stopwords) if usar_stemming else tokens_sin_stopwords
    return {
        "texto_original": texto,
        "texto_normalizado": texto_normalizado,
        "tokens": tokens,
        "tokens_corregidos": tokens_corregidos,
        "tokens_sin_stopwords": tokens_sin_stopwords,
        "tokens_finales": tokens_finales,
        "texto_preprocesado": " ".join(tokens_finales)
    }


if __name__ == "__main__":
    consultas = [
        "¿Cuáles son los requisitos para la admisión en la UG?",
        "Canales ofisiales de admisión",
        "Debo hacer el registro nasional",
        "Evaluación por bloque de conosimientos"
    ]
    print("PRUEBA DEL MÓDULO DE PREPROCESAMIENTO\n")
    for consulta in consultas:
        resultado = explicar_preprocesamiento(consulta)
        print("=" * 70)
        for clave, valor in resultado.items():
            print(f"{clave}: {valor}")
