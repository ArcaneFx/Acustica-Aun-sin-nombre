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

## Por hacer
- Escuchar y describir honestamente cada audio; probar con otros oyentes si hay tiempo.
- Generar audios con la salida real de la Fase 1 sobre los cuentos de Quiroga cuando Benjamin la entregue.
- Comparar con la versión `_base` (sin modulación).
- Probar la reproducción desde cero (`ffmpeg` es dependencia del sistema; las voces se bajan con `python -m piper.download_voices`).
