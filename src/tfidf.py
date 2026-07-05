"""
Módulo de representación TF-IDF para el Agente Conversacional UG.


Etapa: Representación textual con TF-IDF
Proyecto: Agente Conversacional para Admisión y Nivelación de la UG

Este módulo realiza:
1. Carga de utterances desde data/intents.json.
2. Preprocesamiento usando src/preprocessing.py.
3. Construcción del vocabulario.
4. Cálculo de TF.
5. Cálculo de IDF.
6. Representación TF-IDF de utterances.
7. Representación TF-IDF de una consulta nueva del usuario.
"""

import json
import math
from pathlib import Path
from collections import Counter
from typing import Dict, List, Any


try:
    from preprocessing import preprocesar_texto
except ImportError:
    from src.preprocessing import preprocesar_texto


BASE_DIR = Path(__file__).resolve().parents[1]
RUTA_INTENTS = BASE_DIR / "data" / "intents.json"


def cargar_intenciones(ruta_json: Path = RUTA_INTENTS) -> Dict[str, Any]:
    """
    Carga el archivo de intenciones en formato JSON.

    Args:
        ruta_json (Path): ruta del archivo intents.json.

    Returns:
        Dict[str, Any]: contenido del archivo JSON.
    """
    with open(ruta_json, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    return datos


def extraer_utterances(datos_intents: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Extrae las frases de entrenamiento del archivo intents.json.

    El archivo puede usar la clave:
    - "utterances", o
    - "patterns"

    Cada frase queda asociada a su intención o tag.
    """
    registros = []

    for intent in datos_intents.get("intents", []):
        tag = intent.get("tag", "sin_tag")

        # Se aceptan ambos nombres para evitar errores:
        # utterances = nombre recomendado para el informe
        # patterns = nombre usado actualmente en tu archivo JSON
        frases = intent.get("utterances", intent.get("patterns", []))

        for frase in frases:
            texto_preprocesado = preprocesar_texto(frase)

            if texto_preprocesado.strip() != "":
                registros.append({
                    "tag": tag,
                    "utterance_original": frase,
                    "utterance_preprocesada": texto_preprocesado
                })

    return registros


def construir_vocabulario(registros: List[Dict[str, str]]) -> List[str]:
    """
    Construye el vocabulario a partir de las utterances preprocesadas.

    Args:
        registros (List[Dict[str, str]]): lista de utterances procesadas.

    Returns:
        List[str]: vocabulario ordenado alfabéticamente.
    """
    vocabulario = set()

    for registro in registros:
        tokens = registro["utterance_preprocesada"].split()
        vocabulario.update(tokens)

    return sorted(vocabulario)


def calcular_tf(tokens: List[str]) -> Dict[str, float]:
    """
    Calcula la frecuencia de término, TF.

    TF indica qué tan frecuente es una palabra dentro de un documento.

    Args:
        tokens (List[str]): tokens de una utterance.

    Returns:
        Dict[str, float]: valores TF por término.
    """
    total_tokens = len(tokens)

    if total_tokens == 0:
        return {}

    conteo = Counter(tokens)

    tf = {
        termino: frecuencia / total_tokens
        for termino, frecuencia in conteo.items()
    }

    return tf


def calcular_idf(registros: List[Dict[str, str]], vocabulario: List[str]) -> Dict[str, float]:
    """
    Calcula el IDF de cada término del vocabulario.

    IDF reduce la importancia de palabras que aparecen en muchos documentos
    y aumenta la importancia de palabras más específicas.

    Fórmula usada:
        idf = log((N + 1) / (df + 1)) + 1

    Args:
        registros (List[Dict[str, str]]): utterances procesadas.
        vocabulario (List[str]): lista de términos únicos.

    Returns:
        Dict[str, float]: valores IDF por término.
    """
    numero_documentos = len(registros)
    idf = {}

    for termino in vocabulario:
        documentos_con_termino = 0

        for registro in registros:
            tokens = set(registro["utterance_preprocesada"].split())

            if termino in tokens:
                documentos_con_termino += 1

        idf[termino] = math.log(
            (numero_documentos + 1) / (documentos_con_termino + 1)
        ) + 1

    return idf


def vectorizar_tfidf(texto_preprocesado: str, idf: Dict[str, float]) -> Dict[str, float]:
    """
    Convierte un texto preprocesado en un vector TF-IDF.

    Args:
        texto_preprocesado (str): texto ya limpiado y procesado.
        idf (Dict[str, float]): valores IDF del vocabulario.

    Returns:
        Dict[str, float]: vector TF-IDF en formato disperso.
    """
    tokens = texto_preprocesado.split()
    tf = calcular_tf(tokens)

    vector = {}

    for termino, valor_tf in tf.items():
        if termino in idf:
            vector[termino] = valor_tf * idf[termino]

    return vector


def construir_modelo_tfidf(ruta_json: Path = RUTA_INTENTS) -> Dict[str, Any]:
    """
    Construye el modelo TF-IDF completo desde intents.json.

    Returns:
        Dict[str, Any]: modelo con registros, vocabulario, IDF y matriz TF-IDF.
    """
    datos = cargar_intenciones(ruta_json)
    registros = extraer_utterances(datos)
    vocabulario = construir_vocabulario(registros)
    idf = calcular_idf(registros, vocabulario)

    matriz_tfidf = []

    for registro in registros:
        vector = vectorizar_tfidf(
            registro["utterance_preprocesada"],
            idf
        )

        matriz_tfidf.append(vector)

    modelo = {
        "registros": registros,
        "vocabulario": vocabulario,
        "idf": idf,
        "matriz_tfidf": matriz_tfidf
    }

    return modelo


def vectorizar_consulta(consulta: str, modelo: Dict[str, Any]) -> Dict[str, Any]:
    """
    Vectoriza una consulta nueva del usuario usando el IDF del modelo.

    Args:
        consulta (str): pregunta escrita por el usuario.
        modelo (Dict[str, Any]): modelo TF-IDF construido con las utterances.

    Returns:
        Dict[str, Any]: consulta original, consulta procesada y vector TF-IDF.
    """
    consulta_preprocesada = preprocesar_texto(consulta)

    vector_consulta = vectorizar_tfidf(
        consulta_preprocesada,
        modelo["idf"]
    )

    return {
        "consulta_original": consulta,
        "consulta_preprocesada": consulta_preprocesada,
        "vector_tfidf": vector_consulta
    }


def mostrar_resumen_modelo(modelo: Dict[str, Any]) -> None:
    """
    Muestra un resumen del modelo TF-IDF construido.
    """
    print("RESUMEN DEL MODELO TF-IDF")
    print("-" * 60)
    print("Cantidad de utterances:", len(modelo["registros"]))
    print("Tamaño del vocabulario:", len(modelo["vocabulario"]))
    print("Cantidad de vectores TF-IDF:", len(modelo["matriz_tfidf"]))
    print()
    print("Primeros 20 términos del vocabulario:")
    print(modelo["vocabulario"][:20])
    print()


if __name__ == "__main__":
    try:
        modelo = construir_modelo_tfidf()

        mostrar_resumen_modelo(modelo)

        consulta = "¿Cuáles son los requisitos para ingresar a la UG?"
        resultado = vectorizar_consulta(consulta, modelo)

        print("PRUEBA CON CONSULTA DE USUARIO")
        print("-" * 60)
        print("Consulta original:")
        print(resultado["consulta_original"])
        print()
        print("Consulta preprocesada:")
        print(resultado["consulta_preprocesada"])
        print()
        print("Vector TF-IDF de la consulta:")
        print(resultado["vector_tfidf"])

        print()
        print("Primer vector TF-IDF de utterance:")

        if len(modelo["matriz_tfidf"]) > 0:
            print(modelo["matriz_tfidf"][0])
        else:
            print("No se generó ningún vector TF-IDF porque no se encontraron frases de entrenamiento.")

    except FileNotFoundError:
        print("Error: no se encontró el archivo data/intents.json.")
        print("Verifica que exista la carpeta data/ y el archivo intents.json.")

    except Exception as error:
        print("Ocurrió un error al construir el modelo TF-IDF:")
        print(error)