# Checklist Hito 2 — ACUS220

Pauta: https://vpobleteacustica.github.io/ACUS220-2026/hito02-pauta/
Entrega: fines de octubre 2026 · Presentación: 10 min + 5 min de preguntas · 7–9 diapositivas.

Marca `[x]` solo lo que ya está hecho **y se puede mostrar**. Estado inicial según lo que hay en el repo al 2026-10-28.

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
- [ ] Correr el pipeline completo con el libro: Fase 1 (Benjamin) → audios de oraciones reales (Giorgio) → evaluación (Angel).
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
- [ ] Al menos 2–3 evidencias concretas del último mes (datos, código, experimentos, evaluación, bibliografía).
- [ ] Texto de un libro completo en `data/raw/` (hoy `data/processed/libro.txt` está **vacío**).
- [ ] Fase 1 corrida sobre el libro completo y salida **guardada** en `data/processed/` (JSON/CSV).
- [ ] Primer intento de Fase 2 (mapeo emoción→voz + audio con TTS) en `src/` y audio de ejemplo en `results/`.
- [ ] Commits que reflejen ese trabajo (mensajes informativos; sin commits artificiales).

### 3. Comprensión de datos y desarrollo metodológico (15%)
- [ ] Descripción del corpus: fuente, tamaño (nº oraciones), licencia/dominio público.
- [ ] Distribución de emociones predichas (¿desbalance hacia Neutral?).
- [ ] Problemas de calidad documentados: saltos de línea que parten oraciones, abreviaturas, diálogos largos, palabras gatillo ("no había miedo").
- [ ] Decidir y justificar mejoras de preprocesamiento/segmentación (o dejarlas como limitación explícita).
- [ ] Justificar el modelo (pysentimiento, entrenado en redes sociales, no literatura) y la alternativa de TTS elegida.
- [ ] Supuestos explícitos (p. ej. emoción por oración = unidad de narración).

### 4. Resultados o evidencias intermedias e interpretación (20%)
- [ ] Figura de la **línea temporal emocional** del libro/capítulo (en `figures/`).
- [ ] Cada figura/tabla con una frase de interpretación ("qué vemos y qué NO podemos concluir").
- [ ] Muestra de oraciones etiquetadas a mano (aunque sean ~50–100) y primera medida de acierto del modelo.
- [ ] Al menos 2–3 audios con distintas emociones y una evaluación cualitativa honesta ("¿suena a esa emoción?").
- [ ] Un resultado sorprendente o fallido, contado como aprendizaje.

### 5. Decisiones, dificultades, reformulaciones y plan al Hito 3 (10%)
- [ ] Lista de decisiones con la evidencia que las respalda (qué se eligió, qué se descartó, por qué).
- [ ] Dificultades reales y cómo se enfrentaron.
- [ ] Pipeline actualizado con estados: hecho · en desarrollo · modificado · descartado · pendiente.
- [ ] Plan al Hito 3: prioridades, pendientes, qué probablemente **no** se alcanzará, cierre realista.

### 6. Repositorio, documentación y reproducibilidad (10%)
- [ ] Repo = el mismo del Hito 1 (confirmar cuál es el oficial: el README clona `ArcaneFx/Acustica-Aun-sin-nombre`).
- [ ] Repo **compartido con Víctor Poblete y Carlos Duarte** (verificar en Settings → Collaborators).
- [ ] README actualizado: estado de las fases, resultados, estructura, planificación.
- [ ] Instrucciones de reproducción probadas desde cero (venv + `pip install -r requirements.txt` + comando).
- [ ] `requirements.txt` incluye lo nuevo (TTS, matplotlib/pandas, etc.).
- [ ] Datos originales (`data/raw`) separados de derivados (`data/processed`, `results`).
- [ ] Decisiones documentadas (sección en README o `docs/decisiones.md`).
- [ ] Carpetas vacías (`notebooks/`, `figures/`) con contenido o eliminadas de la estructura.

### 7. Comunicación profesional y manejo del tiempo (10%)
- [ ] 7–9 diapositivas, ensayo cronometrado ≤ 10 min.
- [ ] Reparto de quién habla en cada diapositiva (los 3 integrantes).
- [ ] Diapositivas legibles: poco texto, figuras grandes, escudo UACh.
- [ ] Demo/audios probados con anticipación (con respaldo si falla el audio o internet).

### 8. Referencias y declaración de IA (5%)
- [ ] Citar todas las fuentes que influyeron en decisiones (pysentimiento, LibriQuote, MLS + las nuevas: TTS elegido, corpus, etc.) en README, `references/` y diapositiva final.
- [ ] Declaración de IA **de esta etapa**: qué herramientas, para qué, y qué verificó/decidió el equipo (la del README es genérica del Hito 1).

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
- [ ] B1. Descargar el libro elegido a `data/raw/`.
- [ ] B2. Hacer que `procesar_capitulo` **guarde** el resultado (JSON en `data/processed/`) y que el `__main__` no dependa de regenerar el capítulo de ejemplo.
- [ ] B3. Correr la Fase 1 sobre el libro completo; calcular la distribución de emociones.
- [ ] B4. Gráfico de línea temporal emocional (`figures/`), con interpretación.
- [ ] B5. Mejorar la segmentación (oraciones partidas por saltos de línea, abreviaturas) o documentarlo como limitación con ejemplos.
- [ ] B6. Separar el script en funciones reutilizables (el modelo se carga al importar).
- [ ] B7. Escribir `docs/seccion_benjamin.md` (datos, metodología, decisiones, dificultades).

### Giorgio — Fase 2
- [x] F1. Elegir un TTS y justificar la elección: **Piper (local, gratis, CPU)** con modulación acústica; descartados gpt-4o-mini-tts (de pago), ElevenLabs (cuenta/créditos), Chatterbox (pide GPU). Falta la justificación escrita en `docs/seccion_giorgio.md`.
- [x] F2. Tabla emoción → instrucción/parámetros de voz.
- [x] F3. `src/fase2_narracion.py`: lee cualquier JSON del contrato y genera un audio por oración.
- [ ] F4. _(parcial: hay audios del ejemplo y una demo de 7 emociones; faltan los de la Fase 1 real)_ Generar 5–10 audios con distintas emociones a partir de `ejemplo_linea_temporal.json`; guardarlos en `results/audios/` con su README.
- [ ] F5. Evaluación cualitativa honesta ("¿suena a esa emoción?"), incluyendo lo que falló.
- [ ] F6. Agregar las dependencias del TTS a `requirements.txt` _(hecho: `piper-tts`; falta documentar `ffmpeg` y la descarga de voces, y probar desde cero)_.
- [ ] F7. Escribir `docs/seccion_giorgio.md` (decisiones, dificultades, resultados interpretados).

### Angel — Evaluación, repo y presentación
- [ ] E1. Commitear el contrato y crear las ramas **(lo hace Giorgio: el repo es suyo y los archivos ya están en su máquina)**. _(archivos listos: `docs/contrato.md`, `ejemplo_linea_temporal.json`, `etiquetas_manuales.csv`; falta commit, ramas y acordar el libro con el equipo)_
- [ ] E2. Etiquetar a mano una muestra de oraciones del libro (≥ 50–100) en `etiquetas_manuales.csv`.
- [x] E3. `src/evaluacion.py`: une etiquetas y predicciones por `texto`, calcula acierto y matriz de confusión (probado con etiquetas de prueba descartables; falta correrlo con etiquetas reales).
- [ ] E4. Interpretar la evaluación (¿en qué emociones falla? ¿se confunde con Neutral?).
- [ ] E5. Confirmar cuál es el repo oficial y que esté compartido con Víctor Poblete y Carlos Duarte **(solo el dueño puede agregar colaboradores: lo ejecuta Giorgio, Angel verifica)**.
- [ ] E6. README, `references/`, `data/README.md`, `results/README.md` y declaración de IA de esta etapa (ensamblando las secciones de los otros).
- [ ] E7. Esqueleto de diapositivas y respuestas a preguntas probables; ensamblar al final.
- [ ] E8. Probar la reproducción desde un clon limpio.

Todos: commits atómicos con mensajes claros durante todo el proceso, cada uno en sus archivos.

---

## D. Vísperas de la entrega
- [ ] Repo compartido y último push hecho.
- [ ] Diapositivas exportadas a PDF como respaldo.
- [ ] Audios/demo abiertos y con volumen probado.
- [ ] Ensayo final cronometrado.
