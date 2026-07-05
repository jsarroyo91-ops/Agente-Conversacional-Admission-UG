"""Extracción de entidades del dominio de admisión y nivelación de la UG."""

import re
from typing import Dict, List

try:
    from preprocessing import quitar_acentos
except ImportError:
    from src.preprocessing import quitar_acentos

ETAPAS = {
    "registro nacional": "Registro Nacional",
    "inscripcion": "Inscripción",
    "postulacion": "Postulación",
    "cronograma": "Cronograma de evaluaciones",
    "evaluacion": "Evaluación",
    "examen": "Evaluación",
    "asignacion de cupo": "Asignación de cupo",
    "asignacion de cupos": "Asignación de cupo",
    "aceptacion del cupo": "Aceptación del cupo",
    "aceptacion de cupo": "Aceptación del cupo",
    "confirmar el cupo": "Aceptación del cupo",
    "matricula": "Matrícula",
    "nivelacion": "Curso de Nivelación"
}

DOCUMENTOS = {
    "cedula": "Cédula de identidad",
    "pasaporte": "Pasaporte",
    "titulo de bachiller": "Título de bachiller",
    "registro del titulo": "Registro del título de bachiller",
    "certificado de votacion": "Certificado de votación",
    "carnet del conadis": "Carné del CONADIS",
    "conadis": "Carné del CONADIS",
    "foto tamano carnet": "Foto tamaño carné",
    "foto carnet": "Foto tamaño carné"
}

PLATAFORMAS = {
    "siug": "SIUG",
    "moodle": "Campus Virtual de Nivelación (Moodle)",
    "campus virtual": "Campus Virtual de Nivelación",
    "aula virtual": "Campus Virtual de Nivelación",
    "minedec": "Plataforma del MINEDEC"
}

# Lista orientativa, ampliable desde datos institucionales.
CARRERAS = {
    "ciencia de datos": "Ingeniería en Ciencia de Datos e Inteligencia Artificial",
    "inteligencia artificial": "Ingeniería en Ciencia de Datos e Inteligencia Artificial",
    "ingenieria de software": "Ingeniería de Software",
    "sistemas de informacion": "Sistemas de Información",
    "medicina": "Medicina",
    "enfermeria": "Enfermería",
    "odontologia": "Odontología",
    "derecho": "Derecho",
    "arquitectura": "Arquitectura",
    "ingenieria civil": "Ingeniería Civil",
    "economia": "Economía",
    "psicologia": "Psicología",
    "contabilidad": "Contabilidad y Auditoría",
    "administracion de empresas": "Administración de Empresas"
}

PATRON_ANIO = re.compile(r"\b(20\d{2})\b")
PATRON_CEDULA = re.compile(r"(?<!\d)(\d{10})(?!\d)")
PATRON_FECHA_NUMERICA = re.compile(r"\b(?:0?[1-9]|[12]\d|3[01])[/-](?:0?[1-9]|1[0-2])[/-](?:20\d{2})\b")
MESES = "enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre"
PATRON_FECHA_TEXTUAL = re.compile(rf"\b(?:0?[1-9]|[12]\d|3[01])\s+de\s+(?:{MESES})(?:\s+de\s+20\d{{2}})?\b")
PATRON_PORCENTAJE = re.compile(r"\b(\d{1,3})\s?(?:%|por ciento\b)")
PATRON_NOTA = re.compile(r"\b(\d{1,2})\s?(?:/|sobre)\s?(\d{1,2})\b")


def _normalizar_para_busqueda(texto: str) -> str:
    return quitar_acentos(str(texto).lower())


def _buscar_coincidencias(texto: str, diccionario: Dict[str, str]) -> List[str]:
    encontrados = []
    for clave, nombre in diccionario.items():
        if re.search(rf"(?<!\w){re.escape(clave)}(?!\w)", texto) and nombre not in encontrados:
            encontrados.append(nombre)
    return encontrados


def extraer_fechas(texto: str) -> List[str]:
    fechas = PATRON_FECHA_NUMERICA.findall(texto) + PATRON_FECHA_TEXTUAL.findall(texto)
    # findall de la fecha textual puede retornar valores completos porque no hay grupos capturantes.
    return list(dict.fromkeys(fechas))


def extraer_porcentajes_y_notas(texto: str) -> List[str]:
    resultados = [f"{valor}%" for valor in PATRON_PORCENTAJE.findall(texto)]
    resultados.extend(f"{nota}/{sobre}" for nota, sobre in PATRON_NOTA.findall(texto))
    return list(dict.fromkeys(resultados))


def extraer_entidades(texto: str) -> Dict[str, List[str]]:
    texto_normalizado = _normalizar_para_busqueda(texto)
    return {
        "ETAPA": _buscar_coincidencias(texto_normalizado, ETAPAS),
        "DOCUMENTO": _buscar_coincidencias(texto_normalizado, DOCUMENTOS),
        "PLATAFORMA": _buscar_coincidencias(texto_normalizado, PLATAFORMAS),
        "CARRERA": _buscar_coincidencias(texto_normalizado, CARRERAS),
        "CEDULA": PATRON_CEDULA.findall(texto_normalizado),
        "FECHA": extraer_fechas(texto_normalizado),
        "PERIODO": PATRON_ANIO.findall(texto_normalizado),
        "PORCENTAJE_O_NOTA": extraer_porcentajes_y_notas(texto_normalizado)
    }


def hay_entidades(entidades: Dict[str, List[str]]) -> bool:
    return any(bool(valores) for valores in entidades.values())


if __name__ == "__main__":
    consultas = [
        "Mi cédula es 0912345678 y la matrícula es el 10/07/2026",
        "Quiero estudiar Ciencia de Datos y revisar el SIUG",
        "La evaluación será el 10 de julio de 2026",
        "Necesito 70% de asistencia y 7/10 para aprobar nivelación"
    ]
    for consulta in consultas:
        print("=" * 70)
        print("Consulta:", consulta)
        print("Entidades:", extraer_entidades(consulta))
