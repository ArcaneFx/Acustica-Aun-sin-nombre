# Sección Angel — evaluación, repo y presentación (Hito 2)

> Borrador para completar con resultados reales. No poner cifras hasta tenerlas.

## Qué hice entre hitos
- Contrato de formatos entre los tres frentes ([contrato.md](contrato.md)).
- `src/evaluacion.py`: compara las emociones del modelo con etiquetas manuales (acierto, matriz de confusión, errores).
- Muestra de oraciones etiquetadas a mano: _pendiente_ (n = ?).

## Metodología de evaluación
- Se etiqueta a mano cada oración con una de las 7 emociones del modelo.
- Métricas: acierto de la emoción primaria, acierto primaria-o-secundaria, matriz de confusión, precisión y recall por emoción.
- Limitación: un solo etiquetador (sesgo personal); la etiqueta "Neutral" es la más ambigua.

## Resultados e interpretación
_Pendiente: pegar el informe de `python src/evaluacion.py <cuento>_linea_temporal.json --salida results/evaluacion_fase1.txt` e interpretarlo._
- ¿En qué emociones falla? ¿Cuánto se confunde con Neutral? ¿Qué pasa con negaciones ("no había miedo") y diálogos?

## Decisiones y dificultades
- _Pendiente._

## Qué falta para el Hito 3
- _Pendiente._
