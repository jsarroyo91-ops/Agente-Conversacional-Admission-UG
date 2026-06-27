# Fuentes consultadas

## Proyecto

**Nombre del proyecto:** Agente Conversacional para Admisión y Nivelación de la Universidad de Guayaquil  
**Asignatura:** Procesamiento de Lenguaje Natural  
**Responsable de esta actividad:** ARROYO CHUQUÍN JORGE SANTIAGO  
**Fecha de primera entrega:** 28 de junio de 2026  
**Entregable relacionado:** `data/intents.json`

---

## 1. Propósito del documento

El presente documento registra las fuentes consultadas para la construcción inicial de la base de conocimiento del agente conversacional. La información recopilada se utilizó para definir las intenciones principales, las frases de usuario o *utterances*, las respuestas predefinidas y las entidades relevantes del dominio de admisión y nivelación de la Universidad de Guayaquil.

El objetivo de esta revisión fue garantizar que las respuestas del chatbot se fundamenten en información institucional, verificable y relacionada directamente con los procesos de ingreso, postulación, matrícula, nivelación y oferta académica de la Universidad de Guayaquil.

---

## 2. Criterios de selección de fuentes

Para la construcción de las intenciones se consideraron los siguientes criterios:

1. Priorizar fuentes oficiales de la Universidad de Guayaquil.
2. Usar páginas relacionadas directamente con admisión, nivelación y oferta académica.
3. Evitar información no confirmada o no institucional.
4. Registrar el uso de cada fuente dentro del proyecto.
5. Utilizar la información únicamente para respuestas predefinidas, sin generar información inventada.

---

## 3. Fuentes oficiales consultadas

### 3.1 Portal Oficial de Admisión UG

**Nombre de la fuente:** Portal Oficial de Admisión de la Universidad de Guayaquil  
**URL:** https://admision.ug.edu.ec/admision/  
**Tipo de fuente:** Página institucional oficial  

**Uso dentro del proyecto:**  
Esta fuente fue utilizada para identificar las etapas principales del proceso de admisión de la Universidad de Guayaquil. A partir de esta información se construyeron intenciones relacionadas con el registro nacional, inscripción, postulación, cronograma de evaluación, evaluación, asignación y aceptación de cupo.

**Intenciones relacionadas:**

- `consultar_proceso_admision`
- `consultar_registro_nacional`
- `consultar_inscripcion_postulacion`
- `consultar_cronograma_evaluacion`
- `consultar_evaluacion_admision`
- `aceptar_cupo`
- `consultar_requisitos_admision`

**Justificación de uso:**  
Es una fuente principal del proyecto porque contiene información directamente relacionada con el proceso de admisión de la Universidad de Guayaquil. Permite que el chatbot responda consultas frecuentes de aspirantes sobre las etapas necesarias para ingresar a la institución.

---

### 3.2 Página de Nivelación UG

**Nombre de la fuente:** Curso de Nivelación de Carrera - Universidad de Guayaquil  
**URL:** https://admision.ug.edu.ec/nivelacion/  
**Tipo de fuente:** Página institucional oficial  

**Uso dentro del proyecto:**  
Esta fuente fue utilizada para recopilar información sobre el curso de nivelación, requisitos de matrícula, documentos solicitados, asistencia, calificaciones y criterios generales de aprobación.

**Intenciones relacionadas:**

- `consultar_matricula_nivelacion`
- `consultar_requisitos_nivelacion`
- `consultar_aprobacion_nivelacion`
- `consultar_asistencia_nivelacion`
- `consultar_calificaciones_nivelacion`
- `consultar_documentos_matricula`

**Justificación de uso:**  
La página de nivelación es necesaria porque el chatbot no solo debe responder preguntas sobre admisión, sino también sobre el proceso posterior que deben cumplir los aspirantes que obtienen un cupo. Esta fuente permite construir respuestas sobre matrícula, asistencia y aprobación del curso de nivelación.

---

### 3.3 Oferta Académica UG

**Nombre de la fuente:** Oferta Académica - Admisión Universidad de Guayaquil  
**URL:** https://admision.ug.edu.ec/oferta-ug/  
**Tipo de fuente:** Página institucional oficial  

**Uso dentro del proyecto:**  
Esta fuente fue consultada para identificar la organización general de la oferta académica de la Universidad de Guayaquil, incluyendo carreras, modalidades y bloques de conocimiento.

**Intenciones relacionadas:**

- `consultar_oferta_academica`
- `consultar_carreras_disponibles`
- `consultar_bloques_conocimiento`
- `consultar_modalidad_carrera`

**Justificación de uso:**  
La oferta académica es una de las consultas más comunes de los aspirantes. Esta fuente permite que el chatbot oriente al usuario hacia la revisión de carreras disponibles sin inventar información específica o desactualizada.

---

### 3.4 Calendario Académico de Nivelación UG

**Nombre de la fuente:** Calendario Académico Ciclo I 2026 - 2027  
**URL:** https://admision.ug.edu.ec/calendario/  
**Tipo de fuente:** Página institucional oficial  

**Uso dentro del proyecto:**  
Esta fuente fue utilizada para identificar información relacionada con fechas, actividades académicas, creación de cuentas SIUG, inducción, matrícula y actividades propias del ciclo de nivelación.

**Intenciones relacionadas:**

- `consultar_fechas_nivelacion`
- `consultar_creacion_cuenta_siug`
- `consultar_induccion_nivelacion`
- `consultar_cronograma_nivelacion`

**Justificación de uso:**  
Las fechas suelen cambiar en cada periodo académico, por lo que el chatbot debe responder de forma prudente y recomendar la revisión del calendario oficial. Esta fuente ayuda a construir respuestas que remiten al usuario al cronograma vigente.

---

### 3.5 Reglamento de Admisión de la Universidad de Guayaquil

**Nombre de la fuente:** Reglamento de Admisión de la Universidad de Guayaquil  
**URL:** https://admision.ug.edu.ec/wp-content/uploads/2025/04/REGLAMENTO%20DE%20ADMISI%C3%93N%20DE%20LA%20UNIVERSIDAD%20DE%20GUAYAQUIL%20-%20REFORMADO.pdf  
**Tipo de fuente:** Documento normativo institucional  

**Uso dentro del proyecto:**  
Esta fuente fue considerada como respaldo normativo para comprender las directrices generales del proceso de admisión, los derechos y obligaciones de los aspirantes y la base institucional del proceso de ingreso.

**Intenciones relacionadas:**

- `consultar_normativa_admision`
- `consultar_requisitos_admision`
- `consultar_proceso_admision`

**Justificación de uso:**  
El reglamento permite fundamentar el chatbot en información normativa y no únicamente informativa. Su uso es importante para evitar respuestas ambiguas sobre el proceso de admisión.

---

### 3.6 Reglamento de Matrículas, Aranceles y Derechos de la Universidad de Guayaquil

**Nombre de la fuente:** Reglamento de Matrículas, Aranceles y Derechos de la Universidad de Guayaquil  
**URL:** https://www.ug.edu.ec/wp-content/uploads/SECRETARIA-GENERAL/NORMATIVAS/VIGENTES/Reglamento%20de%20Matriculas%2C%20Aranceles%20y%20Derechos%20de%20la%20Universidad%20de%20Guayaquil%202023%20-%20REFORMADO.pdf  
**Tipo de fuente:** Documento normativo institucional  

**Uso dentro del proyecto:**  
Esta fuente fue revisada como respaldo para las consultas relacionadas con matrícula, responsabilidades del estudiante y procesos administrativos asociados.

**Intenciones relacionadas:**

- `consultar_matricula_nivelacion`
- `consultar_requisitos_nivelacion`
- `consultar_documentos_matricula`

**Justificación de uso:**  
Este documento aporta respaldo normativo para las respuestas relacionadas con matrícula. Es útil para complementar la información publicada en la página de nivelación.

---

## 4. Fuente complementaria autorizada

### 4.1 Blog de orientación académica ALAU

**Nombre de la fuente:** Todo lo que necesitas saber para ingresar a la Universidad de Guayaquil  
**URL:** https://blog.alau.org/todo-lo-que-necesitas-saber-para-ingresar-a-la-universidad-de-guayaquil/  
**Tipo de fuente:** Recurso complementario de orientación  

**Uso dentro del proyecto:**  
Esta fuente se consideró únicamente como apoyo para identificar preguntas frecuentes y formas comunes de consulta de los aspirantes.

**Intenciones relacionadas:**

- `consultar_requisitos_admision`
- `consultar_proceso_admision`
- `consultar_oferta_academica`

**Justificación de uso:**  
Aunque no reemplaza a las fuentes oficiales, puede ayudar a reconocer el lenguaje común usado por los aspirantes. Por esa razón, su uso se limita a la formulación de ejemplos de preguntas o *utterances*, no a la definición de respuestas institucionales.

---

## 5. Relación entre fuentes e intenciones iniciales

| Fuente consultada | Información utilizada | Intenciones asociadas |
|---|---|---|
| Portal Oficial de Admisión UG | Etapas del proceso de admisión, registro, postulación, evaluación y aceptación de cupo | `consultar_proceso_admision`, `consultar_registro_nacional`, `consultar_inscripcion_postulacion`, `consultar_evaluacion_admision`, `aceptar_cupo` |
| Página de Nivelación UG | Matrícula, documentos, asistencia, calificaciones y aprobación del curso de nivelación | `consultar_matricula_nivelacion`, `consultar_requisitos_nivelacion`, `consultar_aprobacion_nivelacion`, `consultar_asistencia_nivelacion` |
| Oferta Académica UG | Carreras, modalidades y bloques de conocimiento | `consultar_oferta_academica`, `consultar_carreras_disponibles`, `consultar_bloques_conocimiento` |
| Calendario Académico UG | Fechas y actividades del ciclo académico de nivelación | `consultar_fechas_nivelacion`, `consultar_cronograma_nivelacion`, `consultar_creacion_cuenta_siug` |
| Reglamento de Admisión UG | Lineamientos institucionales del proceso de admisión | `consultar_normativa_admision`, `consultar_requisitos_admision` |
| Reglamento de Matrículas, Aranceles y Derechos UG | Procesos y responsabilidades asociadas a matrícula | `consultar_matricula_nivelacion`, `consultar_documentos_matricula` |
| Blog ALAU | Preguntas frecuentes y lenguaje común de aspirantes | Apoyo para redactar *utterances* |

---

## 6. Entidades identificadas a partir de las fuentes

A partir de la revisión de fuentes se identificaron entidades relevantes que pueden ser extraídas posteriormente mediante reglas o expresiones regulares.

| Entidad | Descripción | Ejemplo |
|---|---|---|
| `fecha` | Fechas relacionadas con admisión, evaluación, matrícula o nivelación | 10 de mayo, 28 de junio, 2026 |
| `cedula` | Número de documento de identidad del aspirante | 0912345678 |
| `carrera` | Nombre de carrera universitaria consultada por el usuario | Medicina, Software, Derecho |
| `cupo` | Información relacionada con asignación o aceptación de cupo | cupo aceptado, asignación de cupo |
| `nivelacion` | Términos relacionados con el curso de nivelación | curso de nivelación, matrícula de nivelación |
| `siug` | Plataforma institucional usada por estudiantes | cuenta SIUG, matrícula SIUG |
| `documento` | Requisitos documentales para matrícula o inscripción | cédula, título de bachiller, certificado de votación |
| `evaluacion` | Proceso de evaluación de admisión | examen, evaluación, cronograma |
| `bloque_conocimiento` | Área o bloque asociado a carreras y evaluación | Ciencia, Tecnología e Ingeniería |

---

## 7. Uso de las fuentes en el archivo `intents.json`

La información consultada se incorporó al archivo `data/intents.json` mediante la siguiente estructura general:

```json
{
  "tag": "consultar_requisitos_admision",
  "description": "Consulta sobre requisitos generales del proceso de admisión.",
  "utterances": [
    "cuáles son los requisitos para admisión",
    "qué necesito para ingresar a la Universidad de Guayaquil",
    "qué documentos necesito para postular"
  ],
  "responses": [
    "Para participar en el proceso de admisión de la Universidad de Guayaquil debes revisar los requisitos publicados en el portal oficial de admisión. Allí se informa sobre las etapas de registro, inscripción, postulación, evaluación y aceptación de cupo."
  ],
  "entities": [
    "documento",
    "aspirante"
  ],
  "source": "Portal Oficial de Admisión UG"
}
```

Esta estructura permite separar los datos del código fuente del chatbot. De esta manera, las intenciones, frases y respuestas pueden actualizarse sin modificar directamente la lógica del programa.

---

## 8. Observaciones metodológicas

1. Las respuestas del chatbot fueron redactadas como respuestas predefinidas, no como generación abierta de lenguaje natural.
2. Las fuentes oficiales tienen prioridad sobre cualquier recurso complementario.
3. Las fechas específicas deben verificarse en los portales oficiales antes de la entrega final, debido a que pueden cambiar entre periodos académicos.
4. El archivo `intents.json` debe mantenerse separado del código para facilitar su mantenimiento.
5. Las fuentes complementarias solo deben usarse para orientar el lenguaje de las preguntas, no para reemplazar la información oficial.

---

## 9. Referencias en formato APA 7

ALAU. (s. f.). *Todo lo que necesitas saber para ingresar a la Universidad de Guayaquil*. https://blog.alau.org/todo-lo-que-necesitas-saber-para-ingresar-a-la-universidad-de-guayaquil/

Universidad de Guayaquil. (2023). *Reglamento de Matrículas, Aranceles y Derechos de la Universidad de Guayaquil*. https://www.ug.edu.ec/wp-content/uploads/SECRETARIA-GENERAL/NORMATIVAS/VIGENTES/Reglamento%20de%20Matriculas%2C%20Aranceles%20y%20Derechos%20de%20la%20Universidad%20de%20Guayaquil%202023%20-%20REFORMADO.pdf

Universidad de Guayaquil. (2025). *Reglamento de Admisión de la Universidad de Guayaquil - Reformado*. https://admision.ug.edu.ec/wp-content/uploads/2025/04/REGLAMENTO%20DE%20ADMISI%C3%93N%20DE%20LA%20UNIVERSIDAD%20DE%20GUAYAQUIL%20-%20REFORMADO.pdf

Universidad de Guayaquil. (2026). *Calendario Académico Ciclo I 2026 - 2027*. https://admision.ug.edu.ec/calendario/

Universidad de Guayaquil. (2026). *Curso de Nivelación de Carrera*. https://admision.ug.edu.ec/nivelacion/

Universidad de Guayaquil. (2026). *Oferta Académica*. https://admision.ug.edu.ec/oferta-ug/

Universidad de Guayaquil. (2026). *Proceso de Admisión*. https://admision.ug.edu.ec/admision/
