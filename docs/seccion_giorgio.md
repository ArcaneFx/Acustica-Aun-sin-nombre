# Sección Giorgio — Fase 2: narración emocional (Hito 2)

> Borrador. La evaluación perceptiva (¿suena a esa emoción?) está pendiente: hay que escuchar los audios.

## Qué hice entre hitos
- Comparé opciones de TTS y elegí **Piper** (local, gratis, corre en CPU) con voces `es_MX-claude-high` y `es_ES-davefx-medium`.
- `src/fase2_narracion.py`: lee la línea temporal de la Fase 1 (contrato) y genera un WAV por oración, con parámetros acústicos según su emoción primaria.
- `src/medir_audios.py`: mide duración, tono y nivel de los audios para comprobar que la modulación tiene efecto.
- Audios de ejemplo en `results/audios/` y una demo de la misma oración con las 7 emociones en `results/audios/demo_emociones/`.

## Decisión: por qué Piper
| Opción | Motivo para descartarla |
|---|---|
| gpt-4o-mini-tts (OpenAI) | De pago; el equipo prefirió una opción sin costo |
| ElevenLabs v3 | Plan gratis con créditos limitados y sin derechos comerciales |
| Chatterbox | Se recomienda GPU; esta máquina solo tiene CPU |
| edge-tts | Gratis pero en línea (no local), y no se confirmó soporte de estilos en español |

Piper no entiende emociones: la emoción se simula con parámetros acústicos. Es una limitación de fondo y debe decirse en la presentación.

## Tabla emoción → parámetros acústicos (hipótesis de partida)
Ver `PARAMETROS` en `src/fase2_narracion.py`. Criterio general: miedo, sorpresa y alegría más rápidos y agudos; tristeza y disgusto más lentos y graves; enojo más fuerte. Los valores son una hipótesis mía, **no** están calibrados con literatura ni con oyentes.

## Resultado medido (misma oración, 7 emociones; `results/audios/demo_emociones/medicion.txt`)
La modulación cambia lo que debía en la dirección prevista:
- Duración: Tristeza y Disgusto > Neutral > Alegría, Enojo, Miedo, Sorpresa.
- Tono (F0 aprox.): Miedo y Sorpresa ≈ 220 Hz, Alegría ≈ 208, Neutral ≈ 190, Tristeza y Disgusto ≈ 170.
- Nivel: Enojo ≈ 4 dB sobre Neutral; Tristeza ≈ 1 dB bajo.

Salvedades: el F0 es una estimación por autocorrelación (no un extractor profesional) y Piper es estocástico, así que los valores varían un poco entre corridas. **Esto prueba que los parámetros cambian, no que se perciba la emoción.**

## Mejoras para que suene menos robótico (sin entrenar)
Piper sintetiza cada oración por separado y su entonación es bastante plana. Se probaron ajustes baratos antes de pensar en entrenar o clonar voces:
1. **Pausas según la puntuación final** (`--pausas contextual`, por defecto): tras una coma la pausa es 0,4× la base, tras `!`/`?` 1,1×, tras `...` 1,5×. Con `--pausas fija` se recupera el comportamiento anterior. Las pausas base subieron (0,3 a 0,8 s según la emoción) para que la lectura continua respire.
2. **Variación de ritmo por emoción** (`ritmo` = `noise_w_scale` de Piper): más alto en miedo/alegría/sorpresa, más bajo en tristeza/disgusto.
3. **Narración continua** (`--unir`): une las oraciones en un solo audio, que es como se escucha un audiolibro. Archivos: `ejemplo_narracion.wav` (voz `es_MX-claude-high`) y `ejemplo_narracion_davefx.wav` (voz `es_ES-davefx-medium`) para comparar voces de oído.

Salvedades: no hay prueba de escucha todavía, así que **no sé si suena mejor**; solo sé que los parámetros cambian. En el ejemplo casi todas las oraciones terminan en punto, por lo que las pausas contextuales casi no se notan; se verán en los cuentos reales (donde hay comas por los saltos de línea). Piper es estocástico: la duración total varía unos 0,4 s entre corridas, más que el efecto de las pausas en este ejemplo.

Opciones que NO se hicieron (más costosas): afinar Piper con una voz expresiva (requiere horas de audio y GPU), modelos por emoción, y clonación de voz con XTTS/F5-TTS/Chatterbox en Colab. Quedan como trabajo posible del Hito 3.

## Por hacer
- Escuchar y describir honestamente cada audio; probar con otros oyentes si hay tiempo.
- Generar audios con la salida real de la Fase 1 sobre los cuentos de Quiroga cuando Benjamin la entregue.
- Prueba de escucha: comparar `_base` vs con emoción, y las dos voces, con otras personas.
- Probar la reproducción desde cero (`ffmpeg` es dependencia del sistema; las voces se bajan con `python -m piper.download_voices`).
