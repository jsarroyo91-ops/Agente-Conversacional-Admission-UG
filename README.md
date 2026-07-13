# Agente Conversacional para Admisión y Nivelación de la UG

Proyecto académico de la asignatura **Procesamiento de Lenguaje Natural** de la carrera de **Ingeniería en Ciencia de Datos e Inteligencia Artificial** de la Universidad de Guayaquil.

El proyecto implementa un agente conversacional basado en técnicas clásicas de PLN para responder consultas frecuentes sobre admisión y nivelación de la Universidad de Guayaquil.

---
🔗 **Aplicación web:** [Abrir Asistente de Admisión y Nivelación UG](https://asistente-admision-ug.streamlit.app)

## Objetivo

Diseñar e implementar un agente conversacional que identifique la intención del usuario y recupere respuestas predefinidas para preguntas frecuentes sobre admisión y nivelación de la Universidad de Guayaquil.

El sistema emplea técnicas de PLN clásico, entre ellas:

- normalización de texto;
- eliminación de signos y acentos;
- corrección tipográfica básica;
- tokenización;
- eliminación de stopwords;
- stemming;
- representación TF-IDF;
- similitud coseno;
- extracción de entidades mediante reglas;
- umbral de confianza;
- respuesta de fallback.

El agente cuenta con dos formas de ejecución:

1. **Interfaz por consola**, para pruebas locales rápidas.
2. **Interfaz web con Streamlit**, para una presentación visual e interactiva.

---

## Autores

- **Arroyo Chuquín Jorge Santiago**
- **Espinoza Feijoo Odeth Maylin**

---

## Estructura del repositorio

```text
Agente_Conversacional_UG/
├── data/
│   └── intents.json
│
├── docs/
│   └── fuentes_consultadas.md
│
├── src/
│   ├── preprocessing.py
│   ├── tfidf.py
│   ├── chatbot.py
│   ├── entities.py
│   ├── interfaz.py
│   ├── streamlit_app.py
│   └── evaluacion.py
│
├── tests/
│   ├── consultas_prueba.csv
│   └── resultados_evaluacion.csv
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Componentes del proyecto

| Archivo | Descripción |
|---|---|
| `data/intents.json` | Contiene 15 intenciones, 20 patterns por tag, respuestas predefinidas y fallback. |
| `docs/fuentes_consultadas.md` | Documenta las fuentes oficiales y complementarias utilizadas para construir la base de conocimiento. |
| `src/preprocessing.py` | Realiza normalización, corrección tipográfica básica, tokenización, eliminación de stopwords y stemming. |
| `src/tfidf.py` | Construye manualmente el modelo TF-IDF y representa las consultas mediante vectores dispersos. |
| `src/chatbot.py` | Detecta la intención usando similitud coseno, aplica umbral de confianza y selecciona la respuesta. |
| `src/entities.py` | Extrae entidades como etapas, documentos, plataformas, carreras, cédulas, fechas, períodos, porcentajes y notas. |
| `src/interfaz.py` | Ejecuta el agente mediante una interfaz local por consola. |
| `src/streamlit_app.py` | Ejecuta el agente mediante una interfaz web responsive desarrollada con Streamlit. |
| `src/evaluacion.py` | Evalúa el agente y calcula accuracy, F1-macro, métricas por clase y análisis de fallos. |
| `tests/consultas_prueba.csv` | Contiene 30 consultas de prueba con variaciones lingüísticas, errores tipográficos, ambigüedad y casos fuera del dominio. |
| `tests/resultados_evaluacion.csv` | Contiene los resultados generados durante la evaluación del agente. |

---

## Requisitos

Para ejecutar el proyecto se requiere:

- Python 3.10 o superior.
- pip.
- Entorno virtual recomendado.
- Navegador web para usar la interfaz Streamlit.

Las dependencias principales son:

```text
nltk>=3.8.1
streamlit>=1.30.0
```

---

## Instalación

Desde la carpeta raíz del proyecto, cree un entorno virtual:

```bash
python -m venv .venv
```

Active el entorno virtual.

En PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

En CMD:

```cmd
.venv\Scripts\activate
```

En Linux o macOS:

```bash
source .venv/bin/activate
```

Instale las dependencias:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## Ejecución por consola

Para ejecutar el agente en modo consola:

```bash
python src/interfaz.py
```

El sistema cargará el modelo TF-IDF y permitirá escribir consultas desde la terminal.

Para finalizar la conversación, escriba:

```text
salir
```

También se aceptan:

```text
exit
quit
```

### Ejemplos de consulta

```text
¿Qué pasos debo seguir para ingresar a la UG?
¿Cómo confirmo el cupo que me asignaron?
¿Qué documentos necesito para nivelación?
¿Dónde ingreso al aula virtual?
¿Cuál es la nota mínima para aprobar nivelación?
```

---

## Ejecución con Streamlit

El proyecto también incluye una interfaz web responsive desarrollada con Streamlit.

Para ejecutar la aplicación web localmente:

```bash
python -m streamlit run src/streamlit_app.py
```

Luego abra en el navegador:

```text
http://localhost:8501
```

La interfaz web permite:

- escribir consultas en una caja de chat;
- usar botones rápidos para preguntas frecuentes;
- visualizar respuestas del agente;
- mostrar u ocultar el detalle técnico;
- revisar la intención detectada, similitud coseno, tokens compartidos, fallback y entidades.

### Ejemplos para probar en la interfaz web

```text
matricula de nivelacion
como acepto mi cupo
que documentos debo subir al siug
cuando inicia el curso de nivelación
quien ganó el partido
```

La última consulta debería activar el fallback, ya que está fuera del dominio de admisión y nivelación.

---

## Ejecución de módulos por separado

Cada módulo puede probarse de forma independiente.

### Preprocesamiento

```bash
python src/preprocessing.py
```

### Representación TF-IDF

```bash
python src/tfidf.py
```

### Motor conversacional

```bash
python src/chatbot.py
```

### Extracción de entidades

```bash
python src/entities.py
```

---

## Evaluación del agente

Para ejecutar la evaluación:

```bash
python src/evaluacion.py
```

La evaluación utiliza:

```text
tests/consultas_prueba.csv
```

y genera:

```text
tests/resultados_evaluacion.csv
```

El proceso de evaluación realiza:

1. carga del conjunto de prueba;
2. ejecución del agente sobre cada consulta;
3. comparación entre intención esperada e intención predicha;
4. cálculo de accuracy;
5. cálculo de F1-macro;
6. cálculo de precisión, recall y F1 por clase;
7. análisis de fallos;
8. generación del archivo de resultados.

---

## Resultados de la versión incluida

| Métrica | Resultado |
|---|---:|
| Casos evaluados | 30 |
| Aciertos | 29 |
| Fallos | 1 |
| Accuracy | 0.9667 |
| Accuracy porcentual | 96.67 % |
| F1-macro | 0.9735 |

El conjunto incluye consultas dentro y fuera del dominio. Un resultado alto debe interpretarse junto con el F1-macro, el comportamiento del fallback y el análisis de fallos. El accuracy por sí solo no basta para afirmar que el agente es completamente robusto.

---

## Intenciones disponibles

El archivo `data/intents.json` incluye las siguientes intenciones:

1. `saludo`
2. `despedida`
3. `canales_oficiales`
4. `etapas_admision`
5. `registro_nacional`
6. `inscripcion_postulacion`
7. `cronograma_evaluaciones`
8. `evaluacion_admision`
9. `asignacion_cupos`
10. `aceptacion_cupo`
11. `oferta_academica`
12. `nivelacion_objetivo`
13. `matricula_documentos_nivelacion`
14. `aprobacion_nivelacion`
15. `plataformas_calendario`

---

## Entidades reconocidas

El agente puede identificar entidades como:

| Entidad | Ejemplo |
|---|---|
| `ETAPA` | matrícula, evaluación, nivelación, aceptación de cupo |
| `DOCUMENTO` | cédula, pasaporte, título de bachiller |
| `PLATAFORMA` | SIUG, Moodle, Campus Virtual |
| `CARRERA` | Medicina, Derecho, Ciencia de Datos |
| `CEDULA` | 0912345678 |
| `FECHA` | 10/07/2026, 10 de julio de 2026 |
| `PERIODO_O_FECHA` | 2026 |
| `PORCENTAJE_O_NOTA` | 70 %, 7/10 |

---

## Fuentes de información

Las respuestas del agente fueron construidas principalmente a partir de fuentes relacionadas con:

- Portal Oficial de Admisión UG.
- Página del Curso de Nivelación de Carrera.
- Oferta Académica UG.
- Calendario Académico de Nivelación.
- Reglamentos institucionales aplicables.

El detalle de las fuentes se encuentra en:

```text
docs/fuentes_consultadas.md
```

---

## Notas importantes

- Las respuestas son predefinidas y no generativas.
- El agente no utiliza modelos de deep learning ni transformers.
- El sistema se basa en PLN clásico: TF-IDF y similitud coseno.
- Las fechas, requisitos y procesos institucionales deben verificarse siempre en canales oficiales.
- El agente está diseñado para ejecutarse localmente o mediante una app Streamlit.
- La carpeta `__pycache__`, los archivos `.pyc` y el entorno `.venv` están excluidos mediante `.gitignore`.

---

## Archivos excluidos del repositorio

El archivo `.gitignore` debe evitar subir archivos generados automáticamente o configuraciones locales:

```gitignore
__pycache__/
*.pyc
.venv/
.vscode/
.idea/
```

---

## Despliegue web

El archivo principal de la aplicación web es:

```text
src/streamlit_app.py
```

Al desplegar el proyecto en Streamlit Community Cloud, se debe seleccionar este archivo como punto de entrada de la aplicación.

Una vez desplegada la app, se puede agregar el enlace público en la parte superior de este README.
