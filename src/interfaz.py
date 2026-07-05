"""Interfaz local por consola del Agente Conversacional UG."""

from typing import Any, Dict

try:
    from tfidf import construir_modelo_tfidf, cargar_intenciones
    from chatbot import procesar_mensaje, UMBRAL_CONFIANZA
    from entities import extraer_entidades, hay_entidades
except ImportError:
    from src.tfidf import construir_modelo_tfidf, cargar_intenciones
    from src.chatbot import procesar_mensaje, UMBRAL_CONFIANZA
    from src.entities import extraer_entidades, hay_entidades

COMANDOS_SALIDA = {"salir", "exit", "quit"}


def imprimir_encabezado() -> None:
    print("=" * 82)
    print("UNIVERSIDAD DE GUAYAQUIL".center(82))
    print("Ingeniería en Ciencia de Datos e Inteligencia Artificial".center(82))
    print("Trabajo Final de Procesamiento de Lenguaje Natural".center(82))
    print("Realizado por: Arroyo Chuquín Jorge Santiago".center(82))
    print("Espinoza Feijoo Odeth Maylin".center(82))
    print("-" * 82)
    print("AGENTE CONVERSACIONAL PARA ADMISIÓN Y NIVELACIÓN DE LA UG".center(82))
    print("=" * 82)
    print("Escribe una consulta sobre admisión o nivelación.")
    print("Escribe 'salir' para terminar la conversación.")
    print("-" * 82)


def formatear_entidades(entidades: Dict[str, Any]) -> str:
    if not hay_entidades(entidades):
        return "  (no se detectaron entidades específicas en la consulta)"
    partes = [f"{tipo}: {', '.join(valores)}" for tipo, valores in entidades.items() if valores]
    return "  " + " | ".join(partes)


def responder_consulta(
    consulta: str,
    modelo: Dict[str, Any],
    datos_intents: Dict[str, Any],
    modo_depuracion: bool = True
) -> None:
    resultado = procesar_mensaje(consulta, modelo, datos_intents, UMBRAL_CONFIANZA)
    entidades = extraer_entidades(consulta)
    print(f"\nAgente UG: {resultado['respuesta']}")
    if modo_depuracion:
        print("\n[Detalle interno]")
        print(f"  Intención candidata: {resultado['tag_candidato']}")
        print(f"  Similitud coseno máxima: {resultado['similitud_maxima']:.4f}")
        print(f"  Tokens compartidos: {resultado['tokens_compartidos']}")
        print(f"  Umbral de confianza: {resultado['umbral_usado']}")
        print(f"  ¿Fallback aplicado?: {resultado['es_fallback']}")
        print(f"  Intención final: {resultado['tag_final']}")
        print("  Entidades detectadas:")
        print(formatear_entidades(entidades))
    print("-" * 82)


def iniciar_chat() -> None:
    try:
        print("Cargando modelo TF-IDF e intenciones...")
        modelo = construir_modelo_tfidf()
        datos_intents = cargar_intenciones()
    except FileNotFoundError as error:
        print("No se pudo iniciar el agente porque falta un archivo del proyecto.")
        print("Detalle:", error)
        return
    except Exception as error:
        print("No se pudo construir el modelo del agente.")
        print("Detalle:", error)
        return

    print(f"Modelo cargado: {len(modelo['registros'])} patterns, "
          f"{len(modelo['vocabulario'])} términos en el vocabulario.\n")
    imprimir_encabezado()

    while True:
        try:
            consulta = input("\nTú: ").strip()
            if not consulta:
                print("Por favor escribe una consulta.")
                continue
            if consulta.lower() in COMANDOS_SALIDA:
                print("\nAgente UG: Gracias por usar el asistente de Admisión UG. ¡Éxitos en tu proceso!")
                break
            responder_consulta(consulta, modelo, datos_intents)
        except (KeyboardInterrupt, EOFError):
            print("\nConversación finalizada por el usuario.")
            break
        except Exception as error:
            print("\nAgente UG: No fue posible procesar la consulta. Intenta reformularla.")
            print("Detalle técnico:", error)


if __name__ == "__main__":
    iniciar_chat()
