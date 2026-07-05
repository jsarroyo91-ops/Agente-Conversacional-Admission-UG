"""Evaluación del Agente Conversacional UG."""

import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List

try:
    from tfidf import construir_modelo_tfidf, cargar_intenciones
    from chatbot import procesar_mensaje
except ImportError:
    from src.tfidf import construir_modelo_tfidf, cargar_intenciones
    from src.chatbot import procesar_mensaje

BASE_DIR = Path(__file__).resolve().parents[1]
RUTA_CSV_PRUEBA = BASE_DIR / "tests" / "consultas_prueba.csv"
RUTA_SALIDA_CSV = BASE_DIR / "tests" / "resultados_evaluacion.csv"


def cargar_casos_prueba(ruta_csv: Path = RUTA_CSV_PRUEBA) -> List[Dict[str, str]]:
    casos = []
    with open(ruta_csv, "r", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo)
        columnas = set(lector.fieldnames or [])
        requeridas = {"id", "consulta", "intencion_esperada"}
        faltantes = requeridas - columnas
        if faltantes:
            raise ValueError(f"Faltan columnas en el CSV: {sorted(faltantes)}")
        for fila in lector:
            consulta = fila["consulta"].strip()
            esperada = fila["intencion_esperada"].strip()
            if not consulta or not esperada:
                continue
            casos.append({
                "id": fila["id"],
                "consulta": consulta,
                "intencion_esperada": esperada,
                "tipo_variacion": fila.get("tipo_variacion", ""),
                "observacion": fila.get("observacion", "")
            })
    return casos


def ejecutar_evaluacion(casos, modelo, datos_intents):
    resultados = []
    for caso in casos:
        deteccion = procesar_mensaje(caso["consulta"], modelo, datos_intents)
        esperada = caso["intencion_esperada"]
        predicha = deteccion.get("tag_final", "fallback")
        resultados.append({
            "id": caso["id"],
            "consulta": caso["consulta"],
            "intencion_esperada": esperada,
            "intencion_predicha": predicha,
            "tag_candidato": deteccion.get("tag_candidato", "fallback"),
            "similitud_maxima": round(float(deteccion.get("similitud_maxima", 0.0)), 4),
            "tokens_compartidos": int(deteccion.get("tokens_compartidos", 0)),
            "acierto": predicha == esperada,
            "tipo_variacion": caso["tipo_variacion"],
            "observacion": caso["observacion"]
        })
    return resultados


def calcular_metricas(resultados: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(resultados)
    aciertos = sum(bool(r["acierto"]) for r in resultados)
    accuracy = aciertos / total if total else 0.0

    tp, fp, fn = defaultdict(int), defaultdict(int), defaultdict(int)
    clases = sorted(
        {r["intencion_esperada"] for r in resultados}
        | {r["intencion_predicha"] for r in resultados}
    )

    for r in resultados:
        esperada, predicha = r["intencion_esperada"], r["intencion_predicha"]
        if esperada == predicha:
            tp[esperada] += 1
        else:
            fp[predicha] += 1
            fn[esperada] += 1

    por_clase = {}
    valores_f1 = []
    for clase in clases:
        precision = tp[clase] / (tp[clase] + fp[clase]) if tp[clase] + fp[clase] else 0.0
        recall = tp[clase] / (tp[clase] + fn[clase]) if tp[clase] + fn[clase] else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        por_clase[clase] = {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "soporte": tp[clase] + fn[clase]
        }
        valores_f1.append(f1)

    return {
        "total_casos": total,
        "aciertos": aciertos,
        "fallos": total - aciertos,
        "accuracy": round(accuracy, 4),
        "f1_macro": round(sum(valores_f1) / len(valores_f1), 4) if valores_f1 else 0.0,
        "metricas_por_clase": por_clase
    }


def imprimir_reporte(resultados, metricas):
    print("=" * 100)
    print("EVALUACIÓN DEL AGENTE - DETECCIÓN DE INTENCIÓN")
    print("=" * 100)
    print(f"Total: {metricas['total_casos']} | Aciertos: {metricas['aciertos']} | Fallos: {metricas['fallos']}")
    print(f"Accuracy: {metricas['accuracy']:.4f} ({metricas['accuracy'] * 100:.2f}%)")
    print(f"F1-macro: {metricas['f1_macro']:.4f}")

    print("\nMÉTRICAS POR CLASE")
    print(f"{'Intención':<34}{'Precisión':<12}{'Recall':<12}{'F1':<10}{'Soporte':<8}")
    for clase, m in metricas["metricas_por_clase"].items():
        print(f"{clase:<34}{m['precision']:<12}{m['recall']:<12}{m['f1']:<10}{m['soporte']:<8}")

    print("\nTABLA DE RESULTADOS")
    print(f"{'ID':<4}{'Consulta':<46}{'Esperada':<30}{'Predicha':<30}{'Sim.':<8}{'Estado'}")
    for r in resultados:
        consulta = r["consulta"] if len(r["consulta"]) <= 43 else r["consulta"][:40] + "..."
        estado = "OK" if r["acierto"] else "FALLO"
        print(f"{r['id']:<4}{consulta:<46}{r['intencion_esperada']:<30}{r['intencion_predicha']:<30}{r['similitud_maxima']:<8}{estado}")

    fallos = [r for r in resultados if not r["acierto"]]
    print(f"\nANÁLISIS DE FALLOS ({len(fallos)})")
    if not fallos:
        print("No se registraron fallos en este conjunto de prueba.")
    for r in fallos:
        causa = (
            "La consulta fue enviada a fallback por similitud o tokens insuficientes."
            if r["intencion_predicha"] == "fallback"
            else "Existe solapamiento léxico con una intención distinta."
        )
        print(f"- ID {r['id']}: {r['consulta']}")
        print(f"  Esperada={r['intencion_esperada']} | Predicha={r['intencion_predicha']} | "
              f"Similitud={r['similitud_maxima']} | Tokens={r['tokens_compartidos']}")
        print(f"  Tipo={r['tipo_variacion']} | Análisis={causa}")

    resumen_tipos = Counter(r["tipo_variacion"] for r in fallos)
    if resumen_tipos:
        print("\nFALLOS POR TIPO DE VARIACIÓN")
        for tipo, cantidad in sorted(resumen_tipos.items()):
            print(f"- {tipo}: {cantidad}")


def guardar_csv(resultados, ruta: Path = RUTA_SALIDA_CSV):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    campos = [
        "id", "consulta", "intencion_esperada", "intencion_predicha",
        "tag_candidato", "similitud_maxima", "tokens_compartidos",
        "acierto", "tipo_variacion", "observacion"
    ]
    with open(ruta, "w", encoding="utf-8-sig", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(resultados)


if __name__ == "__main__":
    try:
        modelo = construir_modelo_tfidf()
        datos_intents = cargar_intenciones()
        casos = cargar_casos_prueba()
        resultados = ejecutar_evaluacion(casos, modelo, datos_intents)
        metricas = calcular_metricas(resultados)
        imprimir_reporte(resultados, metricas)
        guardar_csv(resultados)
        print(f"\nResultados guardados en: {RUTA_SALIDA_CSV}")
    except Exception as error:
        print("No fue posible completar la evaluación.")
        print("Detalle:", error)
        raise
