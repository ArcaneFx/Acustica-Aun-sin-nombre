# Checklist Hito 2 — ACUS220

Pauta: https://vpobleteacustica.github.io/ACUS220-2026/hito02-pauta/
Entrega: fines de octubre 2026 · Presentación: 10 min + 5 min de preguntas · 7–9 diapositivas.

Marca `[x]` solo lo que ya está hecho **y se puede mostrar**. Estado inicial al 2026-10-28; **actualizado el 2026-10-29** según lo que hay en `main`/rama `giorgio/pipeline`.

---

## Reparto del equipo (tres frentes independientes)

Objetivo: que nadie espere a otra persona. Cada uno tiene su propia carpeta/archivos (sin conflictos en git), su propia
entrada de prueba y su propia salida. Lo único compartido es un **contrato** de formatos que se acuerda hoy y no se cambia
sin avisar.

### Contrato (acordarlo hoy, 30 min, lo commitea Giorgio)
- [x] **Corpus elegido**: los tres cuentos de Quiroga en `data/raw/` (`quiroga_el_almohadon_de_pluma`, `quiroga_la_gallina_degollada`, `quiroga_a_la_deriva`); el equipo dio libertad de elección.
- [x] **Registro de la Fase 1** (ya existe en el script): `{"id", "texto", "primaria": {"emocion", "prob"}, "secundaria": {...}, "todas_las_probabilidades": {...}}`, guardado como lista JSON.
- [x] **Archivo de ejemplo** `data/processed/ejemplo_linea_temporal.json` con las 8 oraciones de `results/fase1_capitulo_prueba.txt` en ese formato. Es la entrada de prueba de Giorgio y Angel, así no dependen de Benjamin.
- [x] **Etiquetas manuales**: CSV `data/processed/etiquetas_manuales.csv` con columnas `texto,emocion_manual,etiquetador`. Se une con la Fase 1 por `texto`, no por `id` (la segmentación puede cambiar los ids).
- [x] **Audios**: `results/audios/<cuento>_<id>_<emocion>.wav` + `results/audios/README.md` con la oración de cada uno.

### Frentes

| Persona | Frente | Archivos propios | Entrada de prueba | Salida |
|---|---|---|---|---|
| **Benjamin** | Fase 1: libro completo, segmentación, línea temporal | `src/Analisis_sentimientos.py`, `data/raw/`, `figures/` | El libro | `data/processed/<cuento>_linea_temporal.json`, gráfico con interpretación |
| **Giorgio** | Fase 2: emoción → voz → audio | `src/fase2_narracion.py` (nuevo), `results/audios/` | `ejemplo_linea_temporal.json` (no necesita a Benjamin) | 5–10 audios + tabla emoción→voz + evaluación cualitativa |
| **Angel** | Evaluación, repo y presentación | `src/evaluacion.py` (nuevo), `data/processed/etiquetas_manuales.csv`, `README.md`, `references/`, `docs/` | El libro + `ejemplo_linea_temporal.json` | Acierto del modelo y matriz de confusión, README, diapositivas |

Reglas para mantenerlo independiente:
- Cada uno edita **solo sus archivos**; si necesita algo de otro, lo pide por el contrato, no tocando su código.
- Cada uno trabaja en su rama (`benjamin/fase1`, `giorgio/fase2`, `angel/evaluacion`) y hace merge a `main` al terminar.
- `requirements.txt`: cada uno agrega sus líneas al final (Giorgio el TTS, Benjamin pandas/matplotlib, Angel lo que use para evaluar).
- README y diapositivas: cada uno escribe **su sección** en un archivo propio (`docs/seccion_benjamin.md`, `docs/seccion_angel.md`, `docs/seccion_giorgio.md`) con decisiones, dificultades e interpretación de sus resultados. Angel solo ensambla.
- Angel etiqueta solo (frente suyo). Opcional y al final: Benjamin y Giorgio etiquetan 15 oraciones cada uno para medir acuerdo entre personas.

### Único momento de integración (día previo a la entrega)
- [x] Correr el pipeline completo con el libro: `python script.py` (limpieza → Fase 1 → evaluación → gráfico → Fase 2). Probado con los 3 cuentos; el audio completo solo con *A la deriva*.
- [ ] Cada uno confirma que su parte funciona con la salida real y no solo con el ejemplo.
- [ ] Ensayo general juntos, cronometrado.
- [ ] Reparto de diapositivas: Angel 1, 2, 7, 8 · Benjamin 3, 4, 5 · Giorgio 5 (audios), 6.

---

## A. Pauta (por criterio, con ponderación)

### 1. Continuidad y evolución desde el Hito 1 (10%)
- [ ] Resumen del Hito 1 en **una sola diapositiva** (pregunta, datos, prototipo Fase 1).
- [ ] Tabla/lista "qué cambió desde el Hito 1": pregunta, datos, alcance, pipeline.
- [ ] Si algo NO cambió, decir por qué (no se premia mantener la idea ni cambiarla por cambiar).

### 2. Evidencia de trabajo entre hitos (20%) — el criterio más pesado
- [x] Al menos 2–3 evidencias concretas del último mes (datos, código, experimentos, evaluación, bibliografía).
- [x] Texto completo en `data/raw/`: 3 cuentos de Quiroga (`data/processed/libro.txt` sigue vacío y se puede borrar).
- [x] Fase 1 corrida sobre los 3 cuentos y salida **guardada** en `data/processed/` (JSON).
- [x] Primer intento de Fase 2 (mapeo emoción→voz + audio con Piper) en `src/` y audios en `results/audios/`.
- [x] Commits que reflejen ese trabajo (mensajes informativos; sin commits artificiales).

### 3. Comprensión de datos y desarrollo metodológico (15%)
- [x] Descripción del corpus: fuente (Gutenberg 13507), nº de oraciones por cuento y dominio público (README).
- [x] Distribución de emociones predichas (¿desbalance hacia Neutral?): 64 a 86 % Neutral según el cuento (README).
- [x] Problemas de calidad documentados: líneas cortadas, título, diálogos largos, palabras gatillo y etiquetas dudosas (README, `docs/`).
- [x] Mejoras de preprocesamiento justificadas (`docs/seccion_benjamin.md`); la segmentación de diálogos largos queda como limitación explícita.
- [x] Justificar el modelo (pysentimiento, entrenado en redes sociales, no literatura) y la alternativa de TTS elegida (README, `docs/seccion_giorgio.md`).
- [ ] Supuestos explícitos (p. ej. emoción por oración = unidad de narración).

### 4. Resultados o evidencias intermedias e interpretación (20%)
- [x] Figura de la **línea temporal emocional** de cada cuento (en `figures/`).
- [ ] Cada figura/tabla con una frase de interpretación («qué vemos y qué NO podemos concluir»). _(parcial: el README interpreta el conjunto, falta una frase por figura en la presentación)_
- [x] Muestra etiquetada a mano (83 oraciones de *El almohadón de pluma*) y primera medida de acierto: 73,5 % (57,8 % si siempre se dijera Neutral).
- [ ] Al menos 2–3 audios con distintas emociones **y** una evaluación cualitativa honesta («¿suena a esa emoción?»). _(audios hechos; falta la prueba de escucha)_
- [x] Un resultado sorprendente o fallido, contado como aprendizaje: el modelo marca Alegría 98 % en «¡Soy yo, Alicia!» y casi todo sale Neutral; el título quedaba como oración 1 (corregido).

### 5. Decisiones, dificultades, reformulaciones y plan al Hito 3 (10%)
- [x] Lista de decisiones con la evidencia que las respalda (README, `docs/seccion_*.md`).
- [x] Dificultades reales y cómo se enfrentaron (README, `docs/seccion_*.md`).
- [x] Pipeline actualizado con estados: hecho · en desarrollo · descartado · pendiente (README).
- [x] Plan al Hito 3 (README y diapositiva 8): prioridades, pendientes y qué no se alcanzará (una app pulida de producción).

### 6. Repositorio, documentación y reproducibilidad (10%)
- [ ] Repo = el mismo del Hito 1 (confirmar con el equipo; el dueño es `ArcaneFx/Acustica-Aun-sin-nombre`, y es el que usa el README).
- [x] Repo compartido: en GitHub figuran como colaboradores `vpobleteacustica` y `CarlosD1234` (confirmar que este último es Carlos Duarte). El repo es público.
- [x] README actualizado: estado de las fases, resultados, estructura, planificación.
- [ ] Instrucciones de reproducción probadas desde cero (venv + `pip install -r requirements.txt` + comando).
- [x] `requirements.txt` incluye lo nuevo (`piper-tts`, `pandas`, `matplotlib`). `ffmpeg` está documentado como dependencia del sistema.
- [x] Datos originales (`data/raw`) separados de derivados (`data/processed`, `results`).
- [x] Decisiones documentadas (README y `docs/seccion_*.md`).
- [ ] Carpetas vacías (`notebooks/`, `figures/`) con contenido o eliminadas de la estructura.

### 7. Comunicación profesional y manejo del tiempo (10%)
- [ ] 7–9 diapositivas, ensayo cronometrado ≤ 10 min.
- [ ] Reparto de quién habla en cada diapositiva (los 3 integrantes).
- [ ] Diapositivas legibles: poco texto, figuras grandes, escudo UACh.
- [ ] Demo/audios probados con anticipación (con respaldo si falla el audio o internet).

### 8. Referencias y declaración de IA (5%)
- [x] Fuentes citadas en README y `references/` (pysentimiento, LibriQuote, MLS, Quiroga/Gutenberg, Piper). Falta la diapositiva final.
- [ ] Declaración de IA **de esta etapa**. _(hay un borrador en el README; cada integrante debe ajustarlo con lo que usó)_

---

## B. Presentación (estructura sugerida por la pauta)

| # | Diapositiva | Listo |
|---|---|---|
| 1 | Portada: título, integrantes, ACUS220 (Acústica Computacional con Python), UACh, fecha, escudo | [ ] |
| 2 | Punto de partida: Hito 1 resumido + qué cambió | [ ] |
| 3 | Trabajo realizado entre hitos (evidencia concreta) | [ ] |
| 4 | Comprensión de datos y metodología | [ ] |
| 5 | Resultados intermedios + interpretación | [ ] |
| 6 | Decisiones tomadas y su justificación | [ ] |
| 7 | Pipeline actualizado (hecho / en desarrollo / descartado / pendiente) | [ ] |
| 8 | Plan hacia el Hito 3 (prioridades, riesgos, alcance que se recorta) | [ ] |
| 9 | (opcional) Referencias y uso de IA | [ ] |

Preparar respuestas para las preguntas probables (5 min):
- [ ] ¿Qué cambió desde el Hito 1?
- [ ] ¿Cuál fue el avance más importante?
- [ ] ¿Qué evidencia respalda su decisión principal?
- [ ] ¿Qué aprendieron de los datos? ¿Qué resultado los sorprendió?
- [ ] ¿Qué estrategia falló?
- [ ] ¿Qué conclusiones se pueden y cuáles no se pueden sacar?
- [ ] Si reducen el alcance, ¿qué dejan fuera? ¿Qué debe estar listo antes del Hito 3?

---

## C. Desarrollo (trabajo técnico, por frente)

### Benjamin — Fase 1
- [x] B1. Cuentos de Quiroga descargados a `data/raw/` (hecho por Giorgio).
- [x] B2. `procesar_texto` guarda el resultado (JSON en `data/processed/`).
- [x] B3. Fase 1 corrida sobre los 3 cuentos, con la distribución de emociones.
- [x] B4. Gráfico de línea temporal por cuento (`figures/`); interpretación en el README.
- [ ] B5. Mejorar la segmentación. _(limpieza hecha, con el título corregido; falta partir los diálogos largos con narrador y las abreviaturas, o dejarlo como limitación con ejemplos)_
- [ ] B6. Separar el script en funciones reutilizables (el modelo se carga al importar).
- [x] B7. `docs/seccion_benjamin.md` (datos, metodología, decisiones, dificultades).

### Giorgio — Fase 2
- [x] F1. TTS elegido: **Piper (local, gratis, CPU)** con modulación acústica; descartados gpt-4o-mini-tts (de pago), ElevenLabs (créditos), Chatterbox (pide GPU) y edge-tts (en línea). Justificación en `docs/seccion_giorgio.md` y README.
- [x] F2. Tabla emoción → instrucción/parámetros de voz.
- [x] F3. `src/fase2_narracion.py`: lee cualquier JSON del contrato y genera un audio por oración.
- [x] F4. Audios con distintas emociones: demo de las 7 emociones, prueba de escucha de *El almohadón de pluma* con dos voces y flujo completo con `script.py`.
- [ ] F5. Evaluación cualitativa honesta ("¿suena a esa emoción?"), incluyendo lo que falló.
- [x] F6. `piper-tts` en `requirements.txt`; `ffmpeg` y la descarga de voces documentados en el README. _(falta probar desde un clon limpio)_
- [ ] F7. Escribir `docs/seccion_giorgio.md` (decisiones, dificultades, resultados interpretados).

### Angel — Evaluación, repo y presentación
- [x] E1. Contrato commiteado en `main` (`docs/contrato.md`, `ejemplo_linea_temporal.json`, `etiquetas_manuales.csv`).
- [x] E2. 83 oraciones etiquetadas a mano en `etiquetas_manuales.csv`. _(solo *El almohadón de pluma*; faltan los otros dos cuentos)_
- [x] E3. `src/evaluacion.py` corrido con etiquetas reales: 73,5 % de acierto (`results/reporte_evaluacion.txt`).
- [ ] E4. Interpretar la evaluación (¿en qué emociones falla? ¿se confunde con Neutral?).
- [ ] E5. Confirmar cuál es el repo oficial. _(el repo ya está compartido con el profesor; ver criterio 6)_
- [x] E6. README, `references/`, `data/README.md` y `results/README.md` actualizados. _(la declaración de IA es un borrador que cada integrante debe ajustar)_
- [ ] E7. Esqueleto de diapositivas y respuestas a preguntas probables; ensamblar al final.
- [ ] E8. Probar la reproducción desde un clon limpio.

Todos: commits atómicos con mensajes claros durante todo el proceso, cada uno en sus archivos.

---

## D. Vísperas de la entrega
- [ ] Repo compartido y último push hecho.
- [ ] Diapositivas exportadas a PDF como respaldo.
- [ ] Audios/demo abiertos y con volumen probado.
- [ ] Ensayo final cronometrado.
