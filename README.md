# Agente Conversacional para Admisión y Nivelación de la UG

Proyecto académico de la asignatura **Procesamiento de Lenguaje Natural** de la carrera de Ingeniería en Ciencia de Datos e Inteligencia Artificial.

## Objetivo

Diseñar e implementar un agente conversacional local que identifique la intención del usuario y recupere respuestas predefinidas para preguntas frecuentes sobre admisión y nivelación de la Universidad de Guayaquil. El proyecto emplea PLN clásico: normalización, stopwords, stemming, TF-IDF, similitud coseno, reglas de entidades y respuesta de fallback.

## Autores

- Arroyo Chuquín Jorge Santiago
- Espinoza Feijoo Odeth Maylin

## Estructura del repositorio

```text
Agente_Conversacional_UG/
├── data/
│   └── intents.json
├── docs/
│   └── fuentes_consultadas.md
├── src/
│   ├── preprocessing.py
│   ├── tfidf.py
│   ├── chatbot.py
│   ├── entities.py
│   ├── interfaz.py
│   └── evaluacion.py
├── tests/
│   ├── consultas_prueba.csv
│   └── resultados_evaluacion.csv
├── .gitignore
├── requirements.txt
└── README.md
```

## Componentes

- `data/intents.json`: 15 intenciones, 20 patterns por tag, respuestas y fallback.
- `src/preprocessing.py`: normalización, corrección tipográfica básica, tokenización, stopwords y stemming.
- `src/tfidf.py`: construcción manual de TF-IDF y vectores dispersos.
- `src/chatbot.py`: similitud coseno, umbral de confianza y selección de respuesta.
- `src/entities.py`: detección de etapas, documentos, plataformas, carreras, cédulas, fechas, períodos, porcentajes y notas.
- `src/interfaz.py`: interfaz local por consola.
- `src/evaluacion.py`: cálculo de accuracy, F1-macro y análisis de fallos.
- `tests/consultas_prueba.csv`: 30 consultas nuevas, con variaciones, errores tipográficos, ambigüedad y casos fuera del dominio.

## Requisitos

- Python 3.10 o superior.
- `pip`.

## Instalación

Desde la carpeta raíz:

```bash
python -m venv .venv
```

En PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale las dependencias:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Ejecutar el agente

```bash
python src/interfaz.py
```

Escriba una consulta y use `salir`, `exit` o `quit` para finalizar.

Ejemplos:

```text
¿Qué pasos debo seguir para ingresar a la UG?
¿Cómo confirmo el cupo que me asignaron?
¿Qué documentos necesito para nivelación?
¿Dónde ingreso al aula virtual?
```

## Ejecutar módulos por separado

```bash
python src/preprocessing.py
python src/tfidf.py
python src/chatbot.py
python src/entities.py
```

## Evaluación

```bash
python src/evaluacion.py
```

La evaluación usa `tests/consultas_prueba.csv` y genera `tests/resultados_evaluacion.csv`.

### Resultados de la versión incluida

| Métrica | Resultado |
|---|---:|
| Casos evaluados | 30 |
| Aciertos | 29 |
| Fallos | 1 |
| Accuracy | 0.9667 |
| Accuracy porcentual | 96.67 % |
| F1-macro | 0.9735 |

El conjunto incluye consultas dentro y fuera del dominio. Un resultado alto debe interpretarse junto con F1-macro, comportamiento del fallback y análisis de los fallos; no basta por sí solo para afirmar que el agente es robusto.

## Notas

- Las respuestas son predefinidas y no generativas.
- Las fechas y requisitos deben comprobarse en canales oficiales.
- La carpeta `__pycache__`, los archivos `.pyc` y el entorno `.venv` están excluidos mediante `.gitignore`.
