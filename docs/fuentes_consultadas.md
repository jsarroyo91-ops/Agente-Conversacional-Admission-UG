# Fuentes consultadas

## Proyecto

**Nombre:** Agente Conversacional para Admisión y Nivelación de la Universidad de Guayaquil  
**Asignatura:** Procesamiento de Lenguaje Natural  
**Autores:** Arroyo Chuquín Jorge Santiago y Espinoza Feijoo Odeth Maylin  
**Archivo relacionado:** `data/intents.json`

## Propósito

Este documento registra las fuentes utilizadas para definir los `patterns`, respuestas predefinidas e información del dominio. Las respuestas del agente se basan principalmente en fuentes institucionales; los recursos complementarios se emplean únicamente para identificar formas comunes de consulta.

## Fuentes oficiales

### Portal Oficial de Admisión UG

- **URL:** https://admision.ug.edu.ec/admision/
- **Uso:** etapas de admisión, registro, inscripción, postulación, evaluación, asignación y aceptación de cupos.
- **Tags relacionados:** `canales_oficiales`, `etapas_admision`, `registro_nacional`, `inscripcion_postulacion`, `cronograma_evaluaciones`, `evaluacion_admision`, `asignacion_cupos`, `aceptacion_cupo`.

### Curso de Nivelación de Carrera UG

- **URL:** https://admision.ug.edu.ec/nivelacion/
- **Uso:** objetivo del curso, matrícula, documentos, asistencia, calificaciones y aprobación.
- **Tags relacionados:** `nivelacion_objetivo`, `matricula_documentos_nivelacion`, `aprobacion_nivelacion`, `plataformas_calendario`.

### Oferta Académica UG

- **URL:** https://admision.ug.edu.ec/oferta-ug/
- **Uso:** carreras, modalidades y bloques de conocimiento.
- **Tag relacionado:** `oferta_academica`.

### Calendario Académico de Nivelación UG

- **URL:** https://admision.ug.edu.ec/calendario/
- **Uso:** fechas de matrícula, inicio de clases, evaluaciones y actividades académicas.
- **Tag relacionado:** `plataformas_calendario`.

### Reglamento de Admisión de la Universidad de Guayaquil

- **URL:** https://admision.ug.edu.ec/wp-content/uploads/2025/04/REGLAMENTO%20DE%20ADMISI%C3%93N%20DE%20LA%20UNIVERSIDAD%20DE%20GUAYAQUIL%20-%20REFORMADO.pdf
- **Uso:** respaldo normativo de las etapas, obligaciones y derechos asociados al proceso de ingreso.

### Reglamento de Matrículas, Aranceles y Derechos

- **URL:** https://www.ug.edu.ec/wp-content/uploads/SECRETARIA-GENERAL/NORMATIVAS/VIGENTES/Reglamento%20de%20Matriculas%2C%20Aranceles%20y%20Derechos%20de%20la%20Universidad%20de%20Guayaquil%202023%20-%20REFORMADO.pdf
- **Uso:** respaldo para consultas relacionadas con matrícula y procesos administrativos.

## Fuente complementaria

### Blog ALAU

- **URL:** https://blog.alau.org/todo-lo-que-necesitas-saber-para-ingresar-a-la-universidad-de-guayaquil/
- **Uso permitido:** identificar preguntas frecuentes y vocabulario habitual de aspirantes.
- **Limitación:** no sustituye a las fuentes oficiales para redactar respuestas institucionales.

## Relación entre fuentes y tags

| Fuente | Tags principales |
|---|---|
| Admisión UG | `canales_oficiales`, `etapas_admision`, `registro_nacional`, `inscripcion_postulacion`, `cronograma_evaluaciones`, `evaluacion_admision`, `asignacion_cupos`, `aceptacion_cupo` |
| Nivelación UG | `nivelacion_objetivo`, `matricula_documentos_nivelacion`, `aprobacion_nivelacion`, `plataformas_calendario` |
| Oferta Académica UG | `oferta_academica` |
| Calendario UG | `plataformas_calendario` |

## Estructura usada en `intents.json`

```json
{
  "tag": "matricula_documentos_nivelacion",
  "description": "Explica la matrícula de nivelación y los documentos solicitados.",
  "patterns": [
    "como me matriculo en nivelacion",
    "que documentos necesito para nivelacion"
  ],
  "responses": [
    "La matrícula se realiza mediante el SIUG, según las fechas oficiales."
  ],
  "sources": ["nivelacion_curso"]
}
```

## Criterios metodológicos

1. Las respuestas predefinidas se separan del código fuente.
2. Los cambios de fechas deben verificarse en los portales oficiales.
3. Las fuentes complementarias se usan para redactar patrones, no para reemplazar información institucional.
4. Los tags documentados aquí coinciden con los definidos en `data/intents.json`.
