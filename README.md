# Narración emocional

**Generación de audiolibros con análisis de sentimientos**

Proyecto del curso **ACUS220 — Acústica Computacional con Python**, Universidad Austral de Chile (2026).
Integrantes: Giorgio Carlin, Angel Leal, Benjamin Parra.

---

## ¿Qué es?

Las voces sintéticas y muchos audiolibros generados automáticamente leen bien, pero suenan planos:
una frase con miedo suena igual que una con alegría. Este proyecto busca que la narración
**refleje la emoción del texto**.

La idea apunta a audiolibros, educación y entretenimiento (por ejemplo, los audiolibros de novelas,
mangas y libros que se publican en YouTube), mejorando la experiencia de quien escucha.

**Pregunta provisional:** ¿podemos detectar las emociones de un texto narrativo en español y generar
una narración que las exprese?

## Fases del proyecto

| Fase | Qué hace | Estado (Hito 2) |
|------|----------|-----------------|
| **1. Análisis de emociones** | Limpia un cuento, lo divide en oraciones y detecta la emoción de cada una con un modelo de IA. El resultado es una *línea temporal emocional* en JSON y un gráfico. | Funcional sobre 3 cuentos de Quiroga |
| **Evaluación** | Compara las emociones del modelo con etiquetas hechas a mano. | En desarrollo: 1 de 3 cuentos etiquetado |
| **2. Narración emocional** | Usa la línea temporal para generar audio con **Piper** (TTS local), modulando velocidad, tono, volumen y pausa según la emoción. | Prototipo; medido, pero sin prueba de escucha |

```
Texto → Limpieza → Segmentación → Clasificación de emociones → Línea temporal → Mapeo emoción→voz → TTS → Audio
        └────────────────────── Fase 1 ──────────────────────┘                └──────────── Fase 2 ────────────┘
```

## ¿Con qué lo hace?

- **Python 3**
- **[pysentimiento](https://github.com/pysentimiento/pysentimiento)**: toolkit de análisis de opinión y emociones
  en español. Usa un modelo de [Hugging Face Transformers](https://huggingface.co/docs/transformers) sobre
  [PyTorch](https://pytorch.org/) y entrega la probabilidad de 7 emociones:

  | Etiqueta del modelo | En el proyecto |
  |---|---|
  | `joy` | Alegría |
  | `sadness` | Tristeza |
  | `anger` | Enojo |
  | `fear` | Miedo |
  | `surprise` | Sorpresa |
  | `disgust` | Disgusto |
  | `others` | Neutral |

- **[Piper](https://github.com/OHF-voice/piper1-gpl)** (`piper-tts`): TTS neuronal local que corre en CPU, con voces en español.
  Se usan `es_MX-claude-high` (la principal) y `es_ES-davefx-medium`.
- **[ffmpeg](https://ffmpeg.org/)**: aplica tono, volumen y pausas, y une los audios.
- **pandas / matplotlib**: gráficos de la línea temporal emocional.

## Cómo ejecutarlo

### 1. Requisitos

- Python 3.9 o superior (probado con 3.14)
- `ffmpeg` instalado en el sistema (Fase 2)
- Conexión a internet para instalar las dependencias (incluye PyTorch, que pesa bastante) y, la primera vez,
  para descargar el modelo de emociones desde Hugging Face y la voz de Piper (unos 60 MB)

Dependencias (`requirements.txt`):

| Paquete | Para qué |
|---|---|
| `pysentimiento` | Modelo de análisis de emociones en español |
| `torch` | PyTorch, el motor donde corre el modelo |
| `hf_transfer` | Descarga más rápida del modelo desde Hugging Face (opcional; hoy `huggingface_hub` avisa que está obsoleto) |
| `piper-tts` | Síntesis de voz local (Fase 2). Licencia GPL-3.0-or-later |
| `pandas` | Manejo de la línea temporal en DataFrames |
| `matplotlib` | Gráficos de la línea temporal emocional |

### 2. Instalación

Se recomienda un entorno virtual local (`.venv`) para aislar las dependencias:

```bash
git clone https://github.com/ArcaneFx/Acustica-Aun-sin-nombre.git
cd Acustica-Aun-sin-nombre

python -m venv .venv
source .venv/bin/activate             # Linux/macOS (bash/zsh); en fish: source .venv/bin/activate.fish
# .venv\Scripts\activate              # Windows

pip install -r requirements.txt
```

### 3. Flujo completo con un solo comando

```bash
python script.py
```

`script.py` recorre los tres cuentos y **muestra cada paso en la terminal**:

1. **Limpieza** del texto original (quita el título, une las líneas cortadas, normaliza los diálogos).
2. **Fase 1**: emoción primaria y secundaria de cada oración, más la distribución de emociones.
3. **Evaluación** contra las etiquetas manuales, si el cuento las tiene.
4. **Gráfico** de la línea temporal en `figures/`.
5. **Fase 2**: narración con la voz `es_MX-claude-high` en `results/audios/pipeline/<cuento>/` (carpeta ignorada por git).

Opciones útiles:

```bash
python script.py --cuentos quiroga_a_la_deriva   # un solo cuento
python script.py --limite 10                     # narrar solo las primeras 10 oraciones (prueba rápida)
python script.py --reusar-json                   # no vuelve a correr el modelo si el JSON ya existe
python script.py --sin-audio                     # solo pasos 1 a 4
python script.py --base                          # además, cada oración sin modulación para comparar
```

### 4. Pasos por separado

```bash
python src/limpiar_textos.py         # data/raw -> data/processed/<cuento>_limpio.txt
python src/Analisis_sentimientos.py  # texto limpio -> <cuento>_linea_temporal.json
python src/graficar_emociones.py     # JSON -> figures/<cuento>_timeline.png
python src/evaluacion.py data/processed/quiroga_el_almohadon_de_pluma_linea_temporal.json
python src/fase2_narracion.py data/processed/ejemplo_linea_temporal.json --cuento ejemplo --base --unir
```

Las voces de Piper se descargan con `python -m piper.download_voices --download-dir .cache/piper es_MX-claude-high`
(`script.py` lo hace solo si falta).

### 5. Formato de salida

Cada `_linea_temporal.json` es una lista con un registro por oración (el detalle de los formatos compartidos
entre las fases está en [`docs/contrato.md`](docs/contrato.md)):

```json
{
  "id": 1,
  "texto": "Era de noche en la posada Roca de Guía.",
  "primaria":   {"emocion": "Neutral", "prob": 0.994},
  "secundaria": {"emocion": "Sorpresa", "prob": 0.002},
  "todas_las_probabilidades": {"others": 0.994, "surprise": 0.002, "fear": 0.001, "...": 0.0}
}
```

## Preprocesamiento

Los cuentos vienen de Project Gutenberg con tres problemas, que resuelve `src/limpiar_textos.py`:

- La primera línea es el título entre `#` (`#A LA DERIVA#`): se elimina. *(Un error inicial buscaba el texto fijo
  `#TITULO#`, por lo que el título se analizaba como si fuera la oración 1; corregido en este hito.)*
- Las líneas están cortadas a ~70 caracteres: se unen las de cada párrafo.
- Los diálogos usan `--`: se pasan a la raya `—`.

Se mantiene la ortografía antigua (`fué`, `dió`) para no alterar la fuente. Luego `src/Analisis_sentimientos.py`
trata cada línea que empieza con raya como una sola unidad y divide el resto en oraciones tras `.`, `!` o `?`.

## Resultados de la Fase 1

Corpus: tres cuentos de Horacio Quiroga, *Cuentos de amor, de locura y de muerte* (1917), dominio público
([Project Gutenberg 13507](https://www.gutenberg.org/ebooks/13507)).

| Cuento | Oraciones | Neutral | Otras emociones destacadas |
|---|---|---|---|
| *El almohadón de pluma* | 83 | 66 (80 %) | Tristeza 8, Sorpresa 4, Alegría 3 |
| *La gallina degollada* | 153 | 98 (64 %) | Tristeza 26, Enojo 17, Alegría 11 |
| *A la deriva* | 73 | 63 (86 %) | Miedo 3, Alegría 3, Tristeza 2 |

Los gráficos están en [`figures/`](figures/) (`<cuento>_timeline.png`).

**Qué se ve y qué no:**

- Hay un fuerte desbalance hacia "Neutral": el modelo, entrenado con redes sociales, tiene un umbral alto para
  detectar emociones literarias sutiles. Las emociones se concentran en los clímax.
- Que el modelo marque emociones no significa que sean las correctas (ver la evaluación).
- Al tratar cada diálogo como una sola unidad, las intervenciones largas con narrador agrupan varias oraciones en
  una sola predicción, lo que diluye las emociones.

## Evaluación contra etiquetas manuales

Se etiquetaron a mano las 83 oraciones de *El almohadón de pluma* ([`data/processed/etiquetas_manuales.csv`](data/processed/etiquetas_manuales.csv)).
Informe completo y matriz de confusión: [`results/reporte_evaluacion.txt`](results/reporte_evaluacion.txt) y
[`figures/matriz_confusion_almohadon.png`](figures/matriz_confusion_almohadon.png).

| Medida | Valor |
|---|---|
| Acierto con la emoción primaria | 61/83 = 73,5 % |
| Acierto con primaria o secundaria | 72/83 = 86,7 % |
| Referencia: decir siempre "Neutral" | 48/83 = 57,8 % |
| Recall de Miedo / Sorpresa / Tristeza | 17 % / 33 % / 55 % |

**Interpretación:** el 73,5 % supera a la referencia de siempre decir "Neutral", pero la mejora es modesta, y casi
todo el acierto viene de Neutral (recall 98 %). El modelo deja pasar la mayoría de las emociones, sobre todo miedo y
sorpresa. Hay una sola persona etiquetando un solo cuento, así que la cifra es una primera estimación, no un resultado general.

## Fase 2: narración emocional

`src/fase2_narracion.py` lee un JSON de la Fase 1 y genera un WAV por oración. Piper no entiende emociones, por lo
que la emoción primaria se traduce a parámetros acústicos (tabla `PARAMETROS` del script):

| Emoción | Velocidad | Tono | Volumen | Pausa |
|---|---|---|---|---|
| Neutral | normal | 0 | 1,0 | 0,40 s |
| Alegría | más rápida | +1,5 st | 1,1 | 0,35 s |
| Tristeza | más lenta | −2,0 st | 0,8 | 0,80 s |
| Enojo | algo rápida | −1,0 st | 1,4 | 0,30 s |
| Miedo | rápida | +2,5 st | 0,9 | 0,30 s |
| Sorpresa | algo rápida | +3,0 st | 1,15 | 0,45 s |
| Disgusto | algo lenta | −1,5 st | 0,95 | 0,50 s |

(`st` = semitonos.) La pausa final además se ajusta según la puntuación de la oración (una coma pausa menos, `...` más).
**Estos valores son una hipótesis de partida**, no están calibrados con literatura ni con oyentes.

**Qué está medido:** `src/medir_audios.py` sintetiza la misma oración con las 7 emociones y mide duración, tono (F0
aproximado) y nivel. Miedo y Sorpresa salen más agudos y rápidos, Tristeza y Disgusto más graves y lentos, y Enojo más fuerte
(datos en [`results/audios/demo_emociones/`](results/audios/demo_emociones/)).

**Qué NO está probado:** no se hizo todavía una prueba de escucha. Se sabe que los parámetros cambian el audio,
pero no si se percibe la emoción ni si la narración suena más natural. Como la Fase 1 deja ~73 % de las oraciones
como Neutral, la mayor parte de cada narración suena neutral.

Audios para escuchar: [`results/audios/prueba_escucha/`](results/audios/prueba_escucha/README.md) (dos escenas
de *El almohadón de pluma* con dos voces) y [`results/audios/demo_emociones/`](results/audios/demo_emociones/).

### Alternativas de TTS descartadas

| Opción | Por qué no |
|---|---|
| gpt-4o-mini-tts (OpenAI) | De pago; se buscó una opción local y sin costo |
| ElevenLabs v3 | Créditos limitados en el plan gratis |
| Chatterbox | Se recomienda GPU; el equipo trabaja en CPU |
| edge-tts | Gratis pero en línea, y no se confirmó soporte de estilos en español |

Quedan como ideas para el Hito 3: clonación de voz con XTTS-v2 o F5-TTS (necesita GPU, por ejemplo Colab) y
afinar Piper con una voz expresiva (necesita horas de audio y GPU).

## Estado del pipeline

| Etapa | Estado |
|---|---|
| Limpieza de los cuentos | Hecho (título corregido en este hito) |
| Clasificación de emociones y línea temporal (JSON + gráfico) | Hecho para los 3 cuentos |
| Segmentación de diálogos largos con narrador | Pendiente |
| Evaluación con etiquetas manuales | En desarrollo: 1 de 3 cuentos |
| Mapeo emoción → parámetros de voz | Hecho (hipótesis sin calibrar) |
| Narración con Piper | Hecho (prototipo, flujo completo en `script.py`) |
| Prueba de escucha con oyentes | Pendiente |
| Usar la emoción secundaria cuando la primaria es Neutral con baja confianza | Idea sin probar |
| TTS de pago / clonación de voz / afinar Piper | Descartado por ahora |

## Decisiones y documentación por integrante

- [`docs/seccion_benjamin.md`](docs/seccion_benjamin.md): datos, limpieza y Fase 1.
- [`docs/seccion_giorgio.md`](docs/seccion_giorgio.md): Fase 2, elección de Piper y medición de los audios.
- [`docs/seccion_angel.md`](docs/seccion_angel.md): evaluación (borrador).
- [`docs/contrato.md`](docs/contrato.md): formatos compartidos entre las fases.
- [`HITO2_CHECKLIST.md`](HITO2_CHECKLIST.md): checklist del Hito 2 según la pauta.

## Estado del arte

| Proyecto / tecnología | Qué hace |
|---|---|
| [Project Gutenberg + Microsoft + MIT (2023)](https://www.microsoft.com/en/customers/story/1646266241611394912-project-gutenberg-nonprofit-azure-synapse-analytics-azure-ai-services) | ~5.000 audiolibros generados con TTS neuronal, reconocimiento de emoción y clonación de voz |
| [Apple Books — narración digital](https://www.macworld.com/article/1447641/apple-books-ai-narration-audiobooks.html) | Audiolibros narrados por voces de IA para autores y editoriales pequeñas |
| [OpenAI gpt-4o-mini-tts](https://developers.openai.com/api/docs/guides/text-to-speech) | TTS "dirigible": se le indica en texto el tono, la emoción y el ritmo |
| [ElevenLabs Eleven v3](https://elevenlabs.io/blog/eleven-v3) | Etiquetas en línea (`[whispers]`, `[excited]`, `[sighs]`) para controlar emoción; soporta español |
| Anthropic | No ofrece un modelo propio de voz; el modo de voz de Claude [usa tecnología de ElevenLabs](https://the-decoder.com/anthropics-claude-uses-elevenlabs-technology-for-speech-features-rather-than-an-in-house-model/) |
| Modelos abiertos: XTTS-v2, F5-TTS, Chatterbox | TTS multilingüe (incluye español) con transferencia o control de emoción |
| [LibriQuote — Michel et al. (2025)](https://arxiv.org/abs/2509.04072) | 5.300 h de diálogos expresivos de audiolibros; une comprensión narrativa con TTS expresivo |

La diferencia de este proyecto: un pipeline abierto y explicable para **texto literario en español**, donde la emoción
de cada oración se detecta primero y después se usa para dirigir la voz.

## Datos

| Necesidad | Fuente |
|-----------|--------|
| Textos en español (dominio público) | **Usado:** [Project Gutenberg](https://www.gutenberg.org/ebooks/13507), cuentos de Horacio Quiroga. Otras: [Wikisource en español](https://es.wikisource.org/), [Biblioteca Virtual Miguel de Cervantes](https://www.cervantesvirtual.com/) |
| Audiolibros en español alineados con su texto | [Multilingual LibriSpeech — español](https://www.openslr.org/94/) (~918 h de LibriVox) |
| Voz en español etiquetada por emoción | [EmoMatchSpanishDB](https://link.springer.com/article/10.1007/s11042-023-15959-w) (2.005 audios, 7 emociones), [Spanish MEACorpus 2023](https://www.sciencedirect.com/science/article/pii/S0920548924000254) (13 h, 6 emociones) |

## Planificación

| Hito | Fecha aprox. | Meta |
|------|--------------|------|
| Hito 1 | fines de septiembre | Problema, datos, repositorio y prototipo de la Fase 1 |
| Hito 2 | fines de octubre | Fase 1 sobre cuentos completos + Fase 2 concreta conectada a la Fase 1 (primer audio con emoción). **Cumplido a nivel de prototipo** |
| Hito 3 | fines de noviembre | Cierre del proyecto (propuesta, por confirmar con el equipo): ver abajo |

**Propuesta para el Hito 3**, en orden de prioridad:

1. Etiquetar a mano los otros dos cuentos y reevaluar (hoy solo hay un cuento y una persona).
2. Prueba de escucha con oyentes: ¿se distingue la emoción? ¿`_base` contra modulado? ¿qué voz suena mejor?
3. Segmentar mejor los diálogos largos y probar usar la emoción secundaria cuando la primaria es Neutral con baja confianza.
4. Calibrar la tabla emoción → voz con lo que digan los oyentes.
5. Si hay tiempo: probar clonación de voz en Colab. **Probablemente no se alcance.**

## Estructura del repositorio

```text
Acustica-Aun-sin-nombre/
├── README.md
├── script.py                     # Flujo completo: limpieza, Fase 1, evaluación, gráfico y Fase 2
├── requirements.txt
├── HITO2_CHECKLIST.md
├── docs/                         # contrato.md y seccion_<nombre>.md
├── src/
│   ├── limpiar_textos.py         # Limpieza de los cuentos
│   ├── Analisis_sentimientos.py  # Fase 1: emociones y exportación a JSON
│   ├── graficar_emociones.py     # Gráfico de la línea temporal
│   ├── evaluacion.py             # Acierto y matriz de confusión vs etiquetas manuales
│   ├── fase2_narracion.py        # Fase 2: audio con Piper según la emoción
│   └── medir_audios.py           # Duración, tono y nivel de los audios
├── data/
│   ├── raw/                      # Textos originales sin modificar
│   └── processed/                # Textos limpios, líneas temporales (.json) y etiquetas manuales
├── results/                      # Reporte de evaluación y audios (results/audios/)
├── figures/                      # Líneas temporales y matriz de confusión (PNG)
├── notebooks/                    # (vacío por ahora)
└── references/                   # Bibliografía
```

## Presentación Hito 1

https://canva.link/hp4wto71mx5y0zl

## Referencias

- Pérez, J. M. et al. (2021). *pysentimiento: A Python Toolkit for Opinion Mining and Social NLP tasks.* arXiv:2106.09462.
- Michel, G., Epure, E. V. y Cerisara, C. (2025). *Computational Narrative Understanding for Expressive Text-to-Speech.* arXiv:2509.04072.
- Pratap, V. et al. (2020). *MLS: A Large-Scale Multilingual Dataset for Speech Research.* arXiv:2012.03411.
- Quiroga, H. (1917). *Cuentos de amor, de locura y de muerte.* Project Gutenberg, ebook 13507. https://www.gutenberg.org/ebooks/13507
- Piper TTS (Open Home Foundation / Home Assistant). https://github.com/OHF-voice/piper1-gpl — licencia GPL-3.0-or-later; revisar también la licencia de cada voz antes de redistribuir audios.

## Uso de IA

Usamos herramientas de IA generativa como apoyo en este proyecto: Claude (Anthropic) y Gemini (Google) para estructurar el
repositorio, depurar scripts y redactar documentación; y **Claude Code** en la Fase 2 y el flujo completo, donde ayudó a
comparar opciones de TTS, escribir `src/fase2_narracion.py`, `src/medir_audios.py`, `script.py` y parte de la documentación.

Lo que decidió y verificó el equipo: el corpus (cuentos de Quiroga), la elección de un TTS local y gratuito (Piper), la
limpieza de los textos, el etiquetado manual de las oraciones y la interpretación de los resultados. Lo que **no** se ha
verificado todavía: los valores de la tabla emoción → voz (son una hipótesis) y si los audios se perciben emocionales
(no hay prueba de escucha). Cada integrante debe ajustar esta declaración con lo que usó en su parte.
