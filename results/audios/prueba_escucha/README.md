# Prueba de escucha de la Fase 2 (El almohadón de pluma)

Audios generados con la salida **real** de la Fase 1 sobre *El almohadón de pluma* (Quiroga), para que el equipo los escuche.

| Carpeta | Voz Piper |
|---|---|
| `mx/` | `es_MX-claude-high` |
| `davefx/` | `es_ES-davefx-medium` |

En cada carpeta:
- `almohadon_llanto_narracion.wav`: escena del llanto (oraciones 15 a 21), narración continua.
- `almohadon_horror_narracion.wav`: escena de la alucinación y el horror (oraciones 39 a 46), narración continua.
- `*_<emocion>.wav`: cada oración con su modulación emocional; `*_base.wav`: la misma oración sin modular.
- `README.md`: oración y emoción detectada de cada audio.

## Qué escuchar
1. Narración continua: ¿las pausas entre oraciones se sienten naturales?
2. `*_base.wav` contra la versión con emoción: ¿se nota la diferencia, y en la dirección esperada?
3. Una voz contra la otra.

## Ojo con las etiquetas
Los audios siguen lo que dijo la Fase 1, y esa salida tiene errores. Ejemplos (sin verificar contra etiquetas manuales):
- `015`: "…una tarde pudo salir al jardín…" sale Alegría 98%.
- `041`: "—¡Soy yo, Alicia, soy yo!" sale Alegría 98,5% en plena escena de horror.
- `045`: "Los médicos volvieron inútilmente." sale Enojo 90,5%.
- `076` (el clímax del cuento) sale solo Sorpresa 35%.
De 83 oraciones, 66 salen Neutral. Si una oración suena "alegre" donde no toca, el error está en el análisis, no en la voz.

## `fuente/`
Entrada y salida de esta prueba, hechas con una limpieza **improvisada** (unir líneas de cada párrafo y cambiar `--` por `—`). No es el archivo oficial: la limpieza y la Fase 1 sobre los cuentos las entrega Benjamin en `data/processed/`.
- `almohadon_limpio.txt`: texto preparado.
- `almohadon_linea_temporal.json`: salida de la Fase 1 sobre ese texto (formato de `docs/contrato.md`).
