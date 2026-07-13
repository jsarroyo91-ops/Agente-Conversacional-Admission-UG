"""
Interfaz web responsive con Streamlit para el Agente Conversacional UG.

Diseño adaptable para ordenador y celulares.
Reutiliza los módulos:
- preprocessing.py
- tfidf.py
- chatbot.py
- entities.py
"""

from pathlib import Path
import sys
import html

import streamlit as st


# ============================================================
# CONFIGURACIÓN BASE
# ============================================================

st.set_page_config(
    page_title="Asistente de Admisión y Nivelación UG",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = Path(__file__).resolve().parents[1]

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


from src.tfidf import construir_modelo_tfidf, cargar_intenciones
from src.chatbot import procesar_mensaje, UMBRAL_CONFIANZA
from src.entities import extraer_entidades, hay_entidades


# ============================================================
# ESTILOS RESPONSIVE
# ============================================================

def aplicar_estilos() -> None:
    """
    Aplica estilos visuales personalizados y responsive.
    """
    st.markdown(
        """
        <style>
        :root {
            --azul-ug: #003b71;
            --azul-ug-2: #005ea8;
            --dorado-ug: #d6a21f;
            --fondo: #f4f7fb;
            --texto: #1f2937;
            --muted: #64748b;
            --card: #ffffff;
            --borde: #d8e2ef;
            --sombra: 0 14px 34px rgba(15, 23, 42, 0.10);
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(0, 94, 168, 0.10), transparent 28rem),
                radial-gradient(circle at bottom right, rgba(214, 162, 31, 0.13), transparent 30rem),
                var(--fondo);
            color: var(--texto);
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        #MainMenu, footer {
            visibility: hidden;
        }

        .welcome-card {
            background: rgba(255,255,255,0.92);
            border: 1px solid var(--borde);
            border-radius: 24px;
            padding: 26px;
            box-shadow: var(--sombra);
            position: relative;
            overflow: hidden;
            margin-bottom: 90px;
        }

        /* HERO */
        .hero {
            margin-left: calc(-50vw + 50%);
            margin-right: calc(-50vw + 50%);
            padding: 34px 20px 42px 20px;
            background:
                linear-gradient(135deg, rgba(0, 59, 113, 0.98), rgba(0, 94, 168, 0.92)),
                radial-gradient(circle at 20% 20%, rgba(255,255,255,0.18), transparent 22rem);
            color: white;
            border-bottom: 5px solid var(--dorado-ug);
            box-shadow: 0 10px 30px rgba(0, 39, 84, 0.22);
        }

        .hero-inner {
            max-width: 1100px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1.3fr 0.7fr;
            gap: 26px;
            align-items: center;
        }

        .eyebrow {
            font-size: 12px;
            letter-spacing: 2.2px;
            font-weight: 800;
            text-transform: uppercase;
            opacity: 0.9;
            margin-bottom: 12px;
        }

        .hero-title {
            font-size: clamp(32px, 5vw, 58px);
            line-height: 1.05;
            margin: 0;
            font-weight: 900;
        }

        .hero-subtitle {
            font-size: clamp(15px, 2vw, 19px);
            opacity: 0.96;
            margin-top: 14px;
            max-width: 720px;
        }

        .hero-meta {
            margin-top: 18px;
            font-size: 13px;
            line-height: 1.6;
            opacity: 0.93;
        }

        .hero-badge {
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.22);
            border-radius: 24px;
            padding: 22px;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.18);
            backdrop-filter: blur(10px);
            text-align: center;
        }

        .hero-badge-icon {
            font-size: 58px;
            margin-bottom: 8px;
        }

        .hero-badge-title {
            font-weight: 900;
            font-size: 22px;
            margin-bottom: 6px;
        }

        .hero-badge-text {
            font-size: 14px;
            opacity: 0.92;
        }

        /* SECCIONES */
        .section {
            margin-top: 26px;
        }

        .quick-title {
            font-size: 15px;
            color: var(--muted);
            font-weight: 700;
            margin-bottom: 10px;
        }

        /* TARJETAS */
        .welcome-card {
            background: rgba(255,255,255,0.92);
            border: 1px solid var(--borde);
            border-radius: 24px;
            padding: 26px;
            box-shadow: var(--sombra);
            position: relative;
            overflow: hidden;
        }

        .welcome-card::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            width: 7px;
            height: 100%;
            background: linear-gradient(180deg, var(--dorado-ug), #f2c94c);
        }

        .welcome-title {
            font-size: 24px;
            font-weight: 900;
            color: var(--azul-ug);
            margin-bottom: 8px;
            padding-left: 8px;
        }

        .welcome-text {
            font-size: 16px;
            line-height: 1.65;
            color: #334155;
            padding-left: 8px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 14px;
            margin-top: 18px;
        }

        .stat-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 18px;
            padding: 16px;
            text-align: center;
        }

        .stat-number {
            color: var(--azul-ug);
            font-size: 24px;
            font-weight: 900;
        }

        .stat-label {
            color: var(--muted);
            font-size: 12px;
            font-weight: 700;
            margin-top: 4px;
        }

        /* BOTONES STREAMLIT */
        div.stButton > button {
            width: 100%;
            border-radius: 18px;
            border: 1px solid #d8e2ef;
            background: rgba(255,255,255,0.95);
            color: var(--azul-ug);
            font-weight: 800;
            min-height: 48px;
            box-shadow: 0 8px 18px rgba(15, 23, 42, 0.08);
            transition: all 0.18s ease-in-out;
        }

        div.stButton > button:hover {
            background: var(--azul-ug);
            color: white;
            border-color: var(--azul-ug);
            transform: translateY(-2px);
            box-shadow: 0 12px 22px rgba(0, 59, 113, 0.22);
        }

        /* CHAT */
        .chat-area {
            margin-top: 24px;
        }

        .chat-message {
            padding: 16px 18px;
            border-radius: 20px;
            margin: 14px 0;
            max-width: 78%;
            line-height: 1.58;
            font-size: 15px;
            box-shadow: 0 8px 22px rgba(15, 23, 42, 0.08);
            word-wrap: break-word;
        }

        .user-message {
            background: linear-gradient(135deg, var(--azul-ug), var(--azul-ug-2));
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 6px;
        }

        .bot-message {
            background: white;
            color: #263445;
            margin-right: auto;
            border-left: 5px solid var(--dorado-ug);
            border-bottom-left-radius: 6px;
            border: 1px solid #e4edf7;
        }

        .message-label {
            font-size: 11px;
            font-weight: 900;
            opacity: 0.72;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 7px;
        }

        .bot-message .message-label {
            color: var(--azul-ug);
        }

        .detail-box {
            background: #f8fafc;
            border: 1px solid #d8e2ef;
            border-radius: 16px;
            padding: 14px;
            font-size: 13px;
            line-height: 1.6;
        }

        div[data-testid="stExpander"] {
            border: 1px solid #d8e2ef;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
        }

        div[data-testid="stChatInput"] {
            max-width: 900px;
            margin: 0 auto;
        }

        div[data-testid="stChatInput"] textarea {
            border-radius: 18px;
            border: 1px solid #cbd5e1;
        }

        /* SIDEBAR */
        section[data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #e2e8f0;
        }

        /* MOBILE */
        @media (max-width: 820px) {
            .hero {
                padding: 28px 18px 32px 18px;

                div[data-testid="stChatInput"] {
                    max-width: 94%;
                }

                .hero-title {
                    font-size: 30px;
                }

                .stats-grid {
                    grid-template-columns: 1fr;
                }
            }

            .hero-inner {
                grid-template-columns: 1fr;
                text-align: center;
            }

            .hero-subtitle {
                margin-left: auto;
                margin-right: auto;
            }

            .hero-meta {
                font-size: 12px;
            }

            .hero-badge {
                display: none;
            }

            .chat-message {
                max-width: 94%;
                font-size: 14px;
            }

            .welcome-card {
                padding: 22px 18px;
            }

            .welcome-title {
                font-size: 21px;
            }

            .welcome-text {
                font-size: 14px;
            }

            .stats-grid {
                grid-template-columns: 1fr;
            }

            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CARGA DEL MODELO
# ============================================================

@st.cache_resource
def cargar_agente():
    """
    Carga el modelo TF-IDF y las intenciones una sola vez.
    """
    modelo = construir_modelo_tfidf()
    datos_intents = cargar_intenciones()
    return modelo, datos_intents


# ============================================================
# FUNCIONES DE APOYO
# ============================================================

def limpiar_html(texto: str) -> str:
    """
    Escapa texto para evitar que una consulta del usuario inserte HTML.
    """
    return html.escape(str(texto)).replace("\n", "<br>")


def inicializar_estado() -> None:
    """
    Inicializa el historial de conversación.
    """
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []


def formatear_entidades(entidades) -> str:
    """
    Formatea entidades detectadas.
    """
    if not hay_entidades(entidades):
        return "No se detectaron entidades específicas."

    partes = []

    for tipo, valores in entidades.items():
        if valores:
            valores_limpios = ", ".join(limpiar_html(v) for v in valores)
            partes.append(f"<b>{limpiar_html(tipo)}:</b> {valores_limpios}")

    return " | ".join(partes)


def mostrar_hero() -> None:
    """
    Muestra el encabezado principal de la aplicación.
    """
    st.markdown(
        """
<div class="hero">
    <div class="hero-inner">
        <div>
            <div class="eyebrow">Universidad de Guayaquil · Ingeniería en Ciencia de Datos e Inteligencia Artificial</div>
            <h1 class="hero-title">Asistente de Admisión y Nivelación UG</h1>
            <div class="hero-subtitle">
                Agente conversacional para orientar consultas sobre admisión,
                cupos, matrícula, carreras y nivelación.
            </div>
            <div class="hero-meta">
                <b>Trabajo Final de Procesamiento de Lenguaje Natural</b><br>
                Realizado por: Arroyo Chuquín Jorge Santiago · Espinoza Feijoo Odeth Maylin
            </div>
        </div>
        <div class="hero-badge">
            <div class="hero-badge-icon">🎓</div>
            <div class="hero-badge-title">Asistente UG</div>
            <div class="hero-badge-text">
                PLN clásico · TF-IDF · Similitud coseno · Fallback
            </div>
        </div>
    </div>
</div>
        """,
        unsafe_allow_html=True
    )


def mostrar_bienvenida(modelo) -> None:
    """
    Muestra la tarjeta inicial de bienvenida.
    """
    total_patterns = len(modelo["registros"])
    total_vocabulario = len(modelo["vocabulario"])

    st.markdown(
        f"""
<div class="welcome-card">
    <div class="welcome-title">
        Hola, soy tu asistente virtual de admisión y nivelación
    </div>
    <div class="welcome-text">
        Puedes preguntarme sobre requisitos, registro nacional, creación de cuenta,
        postulación, evaluación, asignación de cupos, aceptación de cupo,
        matrícula de nivelación, documentos, carreras y plataformas oficiales.
    </div>
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-number">15</div>
            <div class="stat-label">Intenciones</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{total_patterns}</div>
            <div class="stat-label">Patterns</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{total_vocabulario}</div>
            <div class="stat-label">Términos TF-IDF</div>
        </div>
    </div>
</div>
        """,
        unsafe_allow_html=True
    )


def mostrar_mensaje_usuario(texto: str) -> None:
    """
    Muestra mensaje del usuario.
    """
    st.markdown(
        f"""
        <div class="chat-message user-message">
            <div class="message-label">Tú</div>
            {limpiar_html(texto)}
        </div>
        """,
        unsafe_allow_html=True
    )


def mostrar_mensaje_agente(texto: str, detalle=None, mostrar_detalle=True) -> None:
    """
    Muestra mensaje del agente.
    """
    st.markdown(
        f"""
        <div class="chat-message bot-message">
            <div class="message-label">Agente UG</div>
            {limpiar_html(texto)}
        </div>
        """,
        unsafe_allow_html=True
    )

    if detalle and mostrar_detalle:
        with st.expander("Detalle técnico de la respuesta"):
            st.markdown(
                f"""
                <div class="detail-box">
                    <b>Intención candidata:</b> {limpiar_html(detalle["tag_candidato"])}<br>
                    <b>Similitud coseno máxima:</b> {detalle["similitud_maxima"]:.4f}<br>
                    <b>Tokens compartidos:</b> {detalle["tokens_compartidos"]}<br>
                    <b>Umbral de confianza:</b> {detalle["umbral_usado"]}<br>
                    <b>¿Fallback aplicado?:</b> {detalle["es_fallback"]}<br>
                    <b>Intención final:</b> {limpiar_html(detalle["tag_final"])}<br>
                    <b>Entidades detectadas:</b> {detalle["entidades_formateadas"]}
                </div>
                """,
                unsafe_allow_html=True
            )


def procesar_consulta_usuario(consulta: str, modelo, datos_intents) -> None:
    """
    Procesa la consulta del usuario y agrega la respuesta al historial.
    """
    if not consulta or consulta.strip() == "":
        return

    consulta = consulta.strip()

    st.session_state.mensajes.append(
        {
            "rol": "user",
            "contenido": consulta
        }
    )

    try:
        resultado = procesar_mensaje(
            consulta,
            modelo,
            datos_intents,
            UMBRAL_CONFIANZA
        )

        entidades = extraer_entidades(consulta)

        detalle = {
            "tag_candidato": resultado["tag_candidato"],
            "similitud_maxima": resultado["similitud_maxima"],
            "tokens_compartidos": resultado["tokens_compartidos"],
            "umbral_usado": resultado["umbral_usado"],
            "es_fallback": resultado["es_fallback"],
            "tag_final": resultado["tag_final"],
            "entidades_formateadas": formatear_entidades(entidades)
        }

        st.session_state.mensajes.append(
            {
                "rol": "assistant",
                "contenido": resultado["respuesta"],
                "detalle": detalle
            }
        )

    except Exception as error:
        st.session_state.mensajes.append(
            {
                "rol": "assistant",
                "contenido": (
                    "No fue posible procesar la consulta. "
                    "Intenta reformularla."
                ),
                "detalle": {
                    "tag_candidato": "error",
                    "similitud_maxima": 0.0,
                    "tokens_compartidos": 0,
                    "umbral_usado": UMBRAL_CONFIANZA,
                    "es_fallback": True,
                    "tag_final": "fallback",
                    "entidades_formateadas": limpiar_html(error)
                }
            }
        )


def mostrar_botones_rapidos(modelo, datos_intents) -> None:
    """
    Muestra accesos rápidos a consultas comunes.
    """
    st.markdown(
        '<div class="quick-title">Consultas rápidas</div>',
        unsafe_allow_html=True
    )

    consultas = [
        ("📌 Requisitos", "cuáles son los requisitos de admisión"),
        ("📅 Fechas", "cuando inicia el curso de nivelación"),
        ("👤 Crear cuenta", "cómo creo mi cuenta para admisión"),
        ("✅ Aceptar cupo", "cómo acepto mi cupo"),
        ("📄 Documentos", "qué documentos debo subir al SIUG"),
        ("🎓 Carreras", "dónde veo la oferta académica")
    ]

    cols = st.columns(3)

    for index, (etiqueta, consulta) in enumerate(consultas):
        with cols[index % 3]:
            if st.button(etiqueta, key=f"quick_{index}", use_container_width=True):
                procesar_consulta_usuario(
                    consulta,
                    modelo,
                    datos_intents
                )
                st.rerun()


def mostrar_historial(mostrar_detalle: bool) -> None:
    """
    Muestra el historial de conversación.
    """
    st.markdown('<div class="chat-area">', unsafe_allow_html=True)

    for mensaje in st.session_state.mensajes:
        if mensaje["rol"] == "user":
            mostrar_mensaje_usuario(mensaje["contenido"])

        elif mensaje["rol"] == "assistant":
            mostrar_mensaje_agente(
                mensaje["contenido"],
                detalle=mensaje.get("detalle"),
                mostrar_detalle=mostrar_detalle
            )

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# APP PRINCIPAL
# ============================================================

def main() -> None:
    aplicar_estilos()
    inicializar_estado()
    mostrar_hero()

    try:
        modelo, datos_intents = cargar_agente()

    except FileNotFoundError as error:
        st.error("Falta un archivo necesario para iniciar el agente.")
        st.exception(error)
        st.stop()

    except Exception as error:
        st.error("No se pudo construir el modelo del agente.")
        st.exception(error)
        st.stop()

    with st.sidebar:
        st.title("Panel del agente")

        mostrar_detalle = st.checkbox(
            "Mostrar detalle técnico",
            value=False
        )

        st.info(
            f"Modelo cargado con {len(modelo['registros'])} patterns "
            f"y {len(modelo['vocabulario'])} términos."
        )

        if st.button("Limpiar conversación", use_container_width=True):
            st.session_state.mensajes = []
            st.rerun()

        st.markdown("---")
        st.markdown("### Sobre el agente")
        st.write(
            "Este asistente usa PLN clásico: preprocesamiento, TF-IDF, "
            "similitud coseno y fallback."
        )

    mostrar_botones_rapidos(modelo, datos_intents)

    if len(st.session_state.mensajes) == 0:
        st.markdown('<div class="section">', unsafe_allow_html=True)
        mostrar_bienvenida(modelo)
        st.markdown('</div>', unsafe_allow_html=True)

    mostrar_historial(mostrar_detalle)

    consulta = st.chat_input("Escribe tu consulta sobre admisión o nivelación...")

    if consulta:
        procesar_consulta_usuario(
            consulta,
            modelo,
            datos_intents
        )
        st.rerun()


if __name__ == "__main__":
    main()