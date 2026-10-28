# Contrato entre frentes (Hito 2)

**Corpus:** tres cuentos de Horacio Quiroga (dominio público, Project Gutenberg 13507) en `data/raw/`:
`quiroga_el_almohadon_de_pluma`, `quiroga_la_gallina_degollada` y `quiroga_a_la_deriva`.
`<cuento>` en los nombres de abajo es el nombre de ese archivo sin `.txt`, para que los ids de
distintos cuentos no se pisen.

Formatos compartidos para que Fase 1 (Benjamin), Fase 2 (Giorgio) y evaluación (Angel) trabajen en paralelo.
No se cambian sin avisar al resto.

## 1. Línea temporal de la Fase 1

JSON: lista de registros, uno por oración, el mismo que devuelve `procesar_capitulo`:

```json
{
  "id": 4,
  "texto": "De pronto, la puerta se abrió con violencia ...",
  "primaria":   {"emocion": "Miedo", "prob": 0.433},
  "secundaria": {"emocion": "Sorpresa", "prob": 0.258},
  "todas_las_probabilidades": {"fear": 0.433, "surprise": 0.258, "...": 0.0}
}
```

- Las etiquetas de `primaria`/`secundaria` van en español: Alegría, Tristeza, Enojo, Miedo, Sorpresa, Disgusto, Neutral.
- Los consumidores deben usar `primaria` y `secundaria`. `todas_las_probabilidades` usa claves en inglés.
- Archivo de prueba: [`data/processed/ejemplo_linea_temporal.json`](../data/processed/ejemplo_linea_temporal.json).
  Se reconstruyó a partir de la salida guardada en `results/fase1_capitulo_prueba.txt`, que solo muestra
  las dos emociones principales: por eso su `todas_las_probabilidades` trae solo esas dos, no las 7.
  La salida real de la Fase 1 sí las trae todas.
- Salida de cada cuento: `data/processed/<cuento>_linea_temporal.json`.

## 2. Etiquetas manuales

CSV `data/processed/etiquetas_manuales.csv`, columnas `texto,emocion_manual,etiquetador`.
`emocion_manual` usa las mismas 7 etiquetas en español. Se une con la Fase 1 por `texto` (no por `id`).
Generar la plantilla: `python src/evaluacion.py --plantilla <linea_temporal.json>`.

## 3. Audios (Fase 2)

`results/audios/<cuento>_<id>_<emocion>.wav` (por ejemplo `quiroga_a_la_deriva_004_miedo.wav`), y, opcionalmente, `<cuento>_<id>_base.wav` (la misma oración sin modulación emocional, para comparar), más
`results/audios/README.md` con la oración de cada audio.
