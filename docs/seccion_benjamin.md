# Fase 1: Análisis de emociones - Benjamín Parra

## 1. Datos y Preprocesamiento
Se utilizaron tres cuentos de Horacio Quiroga (*El almohadón de pluma*, *La gallina degollada*, *A la deriva*) extraídos del Project Gutenberg (ID 13507) en formato texto plano UTF-8. 

**Decisiones de limpieza (`src/limpiar_textos.py`):**
* Se eliminó la etiqueta `#TITULO#` inicial.
* Se unieron las líneas fragmentadas por saltos de línea para evitar que el segmentador partiera oraciones por la mitad.
* Se estandarizaron los guiones dobles (`--`) a rayas de diálogo (`—`) sin alterar los espacios originales.
* Se mantuvo la ortografía antigua original (ej. *fué*, *dió*) para no alterar la fuente.

## 2. Metodología
Se utilizó el modelo `pysentimiento` ejecutado en CPU local para predecir la emoción de cada oración. Se reestructuró `src/Analisis_sentimientos.py` para procesar los textos limpios y exportar la línea temporal emocional en formato JSON, proveyendo la entrada exacta requerida por la Fase 2. También se creó `src/graficar_emociones.py` usando `pandas` y `matplotlib` para visualizar el flujo narrativo.

**Dificultades y Limitaciones:**
La segmentación asume como unidad narrativa a toda línea iniciada con raya de diálogo (`—`). En los diálogos largos con intervención del narrador, esto agrupa varias oraciones en una sola predicción emocional.

## 3. Resultados e Interpretación
Las gráficas de trayectoria en `figures/` y el conteo en consola revelan un fuerte desbalance hacia la etiqueta "Neutral" (ej. 99 de 154 oraciones en *La gallina degollada*, 67 de 84 en *El almohadón de pluma*). Esto sugiere que el modelo (entrenado en redes sociales) tiene un umbral alto para detectar emociones literarias sutiles, restringiendo las etiquetas de Tristeza, Enojo y Miedo casi exclusivamente a los clímax narrativos.