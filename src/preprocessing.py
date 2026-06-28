
"""
Módulo de preprocesamiento de texto para el Agente Conversacional UG.

Responsable: ARROYO CHUQUÍN JORGE SANTIAGO
Etapa: Preprocesamiento de texto
Proyecto: Agente Conversacional para Admisión y Nivelación de la UG

Este módulo realiza:
1. Normalización de texto.
2. Conversión a minúsculas.
3. Eliminación de signos de puntuación y caracteres especiales.
4. Eliminación de acentos.
5. Tokenización.
6. Eliminación de stopwords en español.
7. Stemming básico en español usando SnowballStemmer de NLTK.

Nota:
El documento del proyecto permite usar lematización o stemming básico.
En este archivo se usa stemming porque es liviano, fácil de instalar y adecuado
para un chatbot clásico basado en TF-IDF.
"""

import re
import unicodedata
from typing import List, Dict

try:
    from nltk.corpus import stopwords
    from nltk.stem import SnowballStemmer
except ImportError:
    stopwords = None
    SnowballStemmer = None


# Lista mínima de stopwords en español como respaldo si NLTK no está disponible.
STOPWORDS_RESPALDO = {
    "a", "al", "algo", "algunas", "algunos", "ante", "antes", "como", "con",
    "contra", "cual", "cuando", "de", "del", "desde", "donde", "durante",
    "e", "el", "ella", "ellas", "ellos", "en", "entre", "era", "erais",
    "eran", "eras", "eres", "es", "esa", "esas", "ese", "eso", "esos",
    "esta", "estaba", "estaban", "estado", "estais", "estamos", "estan",
    "estar", "este", "esto", "estos", "estoy", "fue", "fueron", "ha",
    "hace", "hacen", "hacer", "han", "hasta", "hay", "la", "las", "le",
    "les", "lo", "los", "me", "mi", "mis", "mucho", "muy", "no", "nos",
    "o", "otra", "otros", "para", "pero", "por", "porque", "que", "se",
    "sea", "ser", "si", "sin", "sobre", "son", "su", "sus", "te", "tiene",
    "tienen", "tu", "tus", "un", "una", "uno", "unos", "y", "ya"
}


def cargar_stopwords() -> set:
    """
    Carga stopwords en español.

    Primero intenta usar NLTK. Si no está instalado el recurso,
    utiliza una lista de respaldo para que el programa no se detenga.

    Returns:
        set: conjunto de palabras vacías en español.
    """
    if stopwords is not None:
        try:
            return set(stopwords.words("spanish"))
        except LookupError:
            # Si falta descargar el corpus de NLTK, se usa la lista de respaldo.
            return STOPWORDS_RESPALDO

    return STOPWORDS_RESPALDO


def quitar_acentos(texto: str) -> str:
    """
    Elimina acentos y diacríticos del texto.

    Ejemplo:
        "admisión" -> "admision"
        "nivelación" -> "nivelacion"

    Args:
        texto (str): texto original.

    Returns:
        str: texto sin acentos.
    """
    texto_normalizado = unicodedata.normalize("NFD", texto)
    texto_sin_acentos = "".join(
        caracter for caracter in texto_normalizado
        if unicodedata.category(caracter) != "Mn"
    )
    return texto_sin_acentos


def normalizar_texto(texto: str) -> str:
    """
    Normaliza el texto antes de la tokenización.

    Procesos aplicados:
    - Conversión a minúsculas.
    - Eliminación de acentos.
    - Eliminación de URLs.
    - Eliminación de correos electrónicos.
    - Eliminación de signos de puntuación y caracteres especiales.
    - Eliminación de espacios múltiples.

    Args:
        texto (str): consulta del usuario o frase de entrenamiento.

    Returns:
        str: texto limpio y normalizado.
    """
    if texto is None:
        return ""

    texto = str(texto)
    texto = texto.lower()
    texto = quitar_acentos(texto)
    texto = re.sub(r"http\S+|www\S+", " ", texto)
    texto = re.sub(r"\S+@\S+", " ", texto)
    texto = re.sub(r"[^a-zA-Z0-9ñÑ\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto


def tokenizar(texto: str) -> List[str]:
    """
    Divide el texto normalizado en tokens.

    Args:
        texto (str): texto normalizado.

    Returns:
        List[str]: lista de palabras o tokens.
    """
    if not texto:
        return []

    return texto.split()


def eliminar_stopwords(tokens: List[str]) -> List[str]:
    """
    Elimina palabras vacías del español.

    Ejemplo:
        ["que", "necesito", "para", "admision"] -> ["necesito", "admision"]

    Args:
        tokens (List[str]): lista de tokens.

    Returns:
        List[str]: tokens sin stopwords.
    """
    stopwords_es = cargar_stopwords()

    return [
        token for token in tokens
        if token not in stopwords_es and len(token) > 1
    ]


def aplicar_stemming(tokens: List[str]) -> List[str]:
    """
    Aplica stemming básico en español.

    El stemming reduce las palabras a una raíz aproximada.

    Args:
        tokens (List[str]): lista de tokens sin stopwords.

    Returns:
        List[str]: tokens procesados con stemming.
    """
    if SnowballStemmer is None:
        return tokens

    stemmer = SnowballStemmer("spanish")
    return [stemmer.stem(token) for token in tokens]


def preprocesar_texto(texto: str, usar_stemming: bool = True) -> str:
    """
    Ejecuta todo el flujo de preprocesamiento.

    Args:
        texto (str): texto original.
        usar_stemming (bool): indica si se aplica stemming.

    Returns:
        str: texto final listo para vectorización TF-IDF.
    """
    texto_normalizado = normalizar_texto(texto)
    tokens = tokenizar(texto_normalizado)
    tokens = eliminar_stopwords(tokens)

    if usar_stemming:
        tokens = aplicar_stemming(tokens)

    return " ".join(tokens)


def explicar_preprocesamiento(texto: str, usar_stemming: bool = True) -> Dict[str, object]:
    """
    Devuelve cada etapa del preprocesamiento para fines de prueba y explicación.

    Esta función es útil para demostrar en el informe o exposición cómo cambia
    una consulta antes de pasar al vectorizador TF-IDF.

    Args:
        texto (str): texto original.
        usar_stemming (bool): indica si se aplica stemming.

    Returns:
        Dict[str, object]: diccionario con las etapas del procesamiento.
    """
    texto_normalizado = normalizar_texto(texto)
    tokens = tokenizar(texto_normalizado)
    tokens_sin_stopwords = eliminar_stopwords(tokens)

    if usar_stemming:
        tokens_finales = aplicar_stemming(tokens_sin_stopwords)
    else:
        tokens_finales = tokens_sin_stopwords

    return {
        "texto_original": texto,
        "texto_normalizado": texto_normalizado,
        "tokens": tokens,
        "tokens_sin_stopwords": tokens_sin_stopwords,
        "tokens_finales": tokens_finales,
        "texto_preprocesado": " ".join(tokens_finales)
    }


if __name__ == "__main__":
    consultas = [
        "¿Cuáles son los requisitos para la admisión en la UG?",
        "Necesito saber cómo matricularme en el curso de nivelación.",
        "¿Dónde puedo revisar la oferta académica de la Universidad de Guayaquil?",
        "Tengo problemas para crear mi cuenta SIUG.",
        "Qué pasa si no acepté el cupo a tiempo?"
    ]

    print("PRUEBA DEL MÓDULO DE PREPROCESAMIENTO\n")

    for consulta in consultas:
        resultado = explicar_preprocesamiento(consulta)

        print("=" * 80)
        print("Texto original:")
        print(resultado["texto_original"])
        print("\nTexto normalizado:")
        print(resultado["texto_normalizado"])
        print("\nTokens:")
        print(resultado["tokens"])
        print("\nTokens sin stopwords:")
        print(resultado["tokens_sin_stopwords"])
        print("\nTokens finales:")
        print(resultado["tokens_finales"])
        print("\nTexto listo para TF-IDF:")
        print(resultado["texto_preprocesado"])
        print()
