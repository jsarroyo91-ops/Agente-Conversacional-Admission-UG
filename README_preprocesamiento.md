# Etapa de preprocesamiento de texto

Este avance corresponde a la etapa asignada a Santiago Arroyo para implementar:

- Normalización de texto.
- Conversión a minúsculas.
- Eliminación de signos y caracteres especiales.
- Eliminación de acentos.
- Tokenización.
- Eliminación de stopwords en español.
- Stemming básico en español.

## Ejecución

Desde la raíz del repositorio:

```bash
python src/preprocessing.py
```

## Instalación de dependencias

```bash
pip install -r requirements.txt
```

Si NLTK no tiene descargadas las stopwords, el código utiliza una lista de respaldo para evitar que el agente se detenga.
