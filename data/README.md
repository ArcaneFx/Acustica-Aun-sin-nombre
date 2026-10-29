# data/

- `raw/`: textos originales, sin modificar (capítulos `.txt` en UTF-8).
  - `capitulo_prueba.txt`: capítulo de ejemplo que genera `src/Analisis_sentimientos.py`.
  - `quiroga_el_almohadon_de_pluma.txt`, `quiroga_la_gallina_degollada.txt`, `quiroga_a_la_deriva.txt`:
    tres cuentos de Horacio Quiroga, *Cuentos de amor, de locura y de muerte* (1917), dominio público.
    Fuente: [Project Gutenberg, ebook 13507](https://www.gutenberg.org/ebooks/13507). Son el recorte exacto de cada
    cuento (solo se pasó de CRLF a LF y se quitaron las líneas en blanco finales). Se conservan tal cual:
    - La primera línea es el título entre `#`.
    - Las líneas están cortadas a ~70 caracteres, así que el segmentador parte oraciones por la mitad.
    - Los diálogos usan `--` en vez de `—`.

    Hay que limpiar esto antes de analizar (derivados van en `processed/`, no aquí).
- `processed/`: salidas intermedias y datos derivados (formatos en [`docs/contrato.md`](../docs/contrato.md)).
  - `quiroga_<cuento>_limpio.txt` y `quiroga_<cuento>_linea_temporal.json`: texto limpio (sin título, líneas unidas, diálogos con `—`) y salida de la Fase 1 de cada cuento (los genera `script.py`).
  - `ejemplo_linea_temporal.json`: línea temporal del capítulo de ejemplo, reconstruida desde `results/fase1_capitulo_prueba.txt` (solo trae las 2 emociones principales por oración).
  - `etiquetas_manuales.csv`: oraciones etiquetadas a mano (datos supervisados); hoy tiene las 83 oraciones de *El almohadón de pluma*. Plantilla vacía: `src/evaluacion.py --plantilla`.
  - `libro.txt`: archivo vacío heredado del Hito 1; se puede borrar.

Fuentes candidatas de textos y audios: ver la sección **Datos** del README principal.
