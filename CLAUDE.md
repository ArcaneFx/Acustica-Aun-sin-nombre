# CLAUDE.md

Contexto del proyecto para Claude Code (y para cualquier persona que llegue al repo).

## Qué es

"Acústica (aún sin nombre)": proyecto en etapa temprana. Hoy el único código es
`src/Analisis_sentimientos.py`, que analiza las **emociones de un texto literario en español,
oración por oración**, y construye una "línea temporal emocional" del capítulo.

El nombre del repo sugiere que esa línea temporal alimentará después algo sonoro
(música o ambientación según la emoción de cada pasaje), pero esa parte todavía no existe
en el código; no la asumas como implementada.

## Estado del repo

- `src/Analisis_sentimientos.py`: script único (≈95 líneas), sin paquete ni módulos.
- Estructura: `data/raw`, `data/processed`, `results`, `notebooks`, `figures`, `references` (ver README).
- `README.md`: documentación completa del proyecto.
- `requirements.txt` (solo `pysentimiento`); no hay tests ni CI.
- Idioma del código, comentarios y salida: **español**.

## Cómo funciona `src/Analisis_sentimientos.py`

1. Al importar, carga el modelo de emociones de
   [pysentimiento](https://github.com/pysentimiento/pysentimiento):
   `create_analyzer(task="emotion", lang="es")` (descarga un modelo de Hugging Face la
   primera vez; es lento y requiere `torch`/`transformers`).
2. `EMOCIONES` traduce las etiquetas del modelo al español
   (`joy`→Alegría, `sadness`→Tristeza, `anger`→Enojo, `fear`→Miedo, `surprise`→Sorpresa,
   `disgust`→Disgusto, `others`→Neutral).
3. `segmentar_en_oraciones(texto)`:
   - Divide por saltos de línea.
   - Las líneas que empiezan con `—`, `-`, `«` o `"` (diálogo) se conservan enteras.
   - El resto se parte en oraciones con la regex `(?<=[.!?])\s+`, descartando fragmentos
     de 2 caracteres o menos.
4. `procesar_capitulo(ruta_archivo)`: lee un `.txt` (UTF-8), predice la emoción de cada
   oración y devuelve una lista de registros:
   ```python
   {
       "id": 1,
       "texto": "...",
       "primaria":   {"emocion": "Miedo", "prob": 0.812},
       "secundaria": {"emocion": "Neutral", "prob": 0.103},
       "todas_las_probabilidades": {"joy": 0.01, ...}  # claves en inglés
   }
   ```
   Además imprime una línea por oración: `[001] (Miedo 81.2% + Neutral 10.3%) | texto`.
5. `__main__`: escribe un capítulo de ejemplo en `data/raw/capitulo_prueba.txt` (ruta relativa
   al archivo, no al directorio actual) y lo procesa. El resultado (`historial`) no se guarda en ningún lado todavía.

## Ejecutar

```bash
pip install -r requirements.txt
```

```bash
python src/Analisis_sentimientos.py
```

## Detalles a tener en cuenta

- El modelo se carga a nivel de módulo: importar el archivo ya dispara la descarga/carga.
- La segmentación no maneja abreviaturas ("Sr.", "etc.") ni `…`/`¿¡` de forma especial,
  y un diálogo largo con varias oraciones cuenta como una sola unidad.
- Las oraciones que cruzan un salto de línea (como en el texto de ejemplo) quedan partidas
  en dos.
- `todas_las_probabilidades` usa las claves originales del modelo (inglés), mientras que
  `primaria`/`secundaria` usan las etiquetas traducidas.
- `data/raw/capitulo_prueba.txt` lo regenera el script con el mismo contenido; está versionado como dato de ejemplo.

## Autores

Repo de Giorno (giorgiocarlin2004) con aportes de Benjamin Parra (ArcaneFx), que subió el
script de análisis.
