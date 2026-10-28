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

| Fase | Qué hace | Estado |
|------|----------|--------|
| **1. Análisis de emociones** | Divide un capítulo en oraciones y detecta la emoción de cada una con un modelo de IA. El resultado es una *línea temporal emocional* del texto. | Prototipo funcional |
| **2. Narración emocional** | Usa la línea temporal de la fase 1 para generar audio con un motor de texto a voz (TTS), ajustando entonación, ritmo y energía según la emoción. | Por desarrollar |

```
Texto → Segmentación → Clasificación de emociones → Línea temporal → Mapeo emoción→voz → TTS → Audiolibro
        └──────────────────── Fase 1 ────────────────────┘          └──────────── Fase 2 ────────────┘
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

- **Fase 2 (en evaluación):** un TTS con control de emoción, por ejemplo
  [gpt-4o-mini-tts de OpenAI](https://developers.openai.com/api/docs/guides/text-to-speech) (instrucciones de tono),
  [ElevenLabs v3](https://elevenlabs.io/blog/eleven-v3) (etiquetas como `[whispers]`, `[excited]`) o modelos abiertos
  como XTTS-v2 y F5-TTS.

## Cómo ejecutarlo

### 1. Requisitos

- Python 3.9 o superior
- Conexión a internet para instalar las dependencias (incluye PyTorch, que pesa bastante) y, la primera vez, para descargar el modelo desde Hugging Face

Dependencias (`requirements.txt`):

| Paquete | Para qué |
|---|---|
| `pysentimiento` | Modelo de análisis de emociones en español |
| `torch` | PyTorch, el motor donde corre el modelo |
| `hf_transfer` | Descarga más rápida del modelo desde Hugging Face (opcional; se activa con `HF_HUB_ENABLE_HF_TRANSFER=1`) |
| `pandas` | Estructuración y manejo de los datos extraídos en DataFrames |
| `matplotlib` | Generación de gráficos para visualizar la línea temporal emocional |
### 2. Instalación

Es obligatorio utilizar un entorno virtual local (`.venv`) para aislar las dependencias del proyecto y evitar errores o conflictos con las librerías del sistema operativo.

```bash
git clone [https://github.com/ArcaneFx/Acustica-Aun-sin-nombre.git](https://github.com/ArcaneFx/Acustica-Aun-sin-nombre.git)
cd Acustica-Aun-sin-nombre

# 1. Crear el entorno virtual aislado
python -m venv .venv

# 2. Activar el entorno
source .venv/bin/activate             # En Linux/macOS (bash/zsh)
source .venv/bin/activate.fish        # En Linux/macOS (fish)
.venv\Scripts\activate                # En Windows

# 3. Instalar todas las dependencias
pip install -r requirements.txt

### 3. Ejecución

```bash
python src/Analisis_sentimientos.py
```

El script:

1. Carga el modelo de emociones (la primera vez tarda porque lo descarga).
2. Lee los textos previamente limpiados de Horacio Quiroga desde la carpeta `data/processed/`.
3. Clasifica la emoción de cada oración y exporta la línea temporal completa en formato JSON para la Fase 2.
4. Imprime en consola el progreso y la distribución total de emociones encontradas:

```text
Procesando 84 oraciones de data/processed/quiroga_el_almohadon_de_pluma_limpio.txt...
Guardado: data/processed/quiroga_el_almohadon_de_pluma_linea_temporal.json
Distribución de emociones primarias: {'Alegría': 3, 'Tristeza': 8, 'Enojo': 1, 'Miedo': 1, 'Neutral': 67, 'Sorpresa': 4, 'Disgusto': 0}
### 4. Formato de salida y nuevos textos

Para analizar nuevos cuentos, primero debes ubicarlos en formato texto dentro de `data/processed/` (idealmente tras pasar por `src/limpiar_textos.py`) y agregarlos a la lista de ejecución de `src/Analisis_sentimientos.py`. 

El script generará un archivo `_linea_temporal.json` donde cada elemento de la lista tiene esta estructura:

```json
[
  {
    "id": 1,
    "texto": "Era de noche en la posada Roca de Guía.",
    "primaria":   {"emocion": "Neutral", "prob": 0.994},
    "secundaria": {"emocion": "Sorpresa", "prob": 0.002},
    "todas_las_probabilidades": {"others": 0.994, "surprise": 0.002, "fear": 0.001, "joy": 0.001, "sadness": 0.001, "anger": 0.001, "disgust": 0.000}
  }
]

## Cómo divide el texto (Preprocesamiento)

- Se unen las líneas fragmentadas por saltos de línea erróneos del texto original.
- Se estandarizan los distintos tipos de guiones a rayas de diálogo (`—`).
- Las líneas de diálogo se tratan como una unidad narrativa completa.
- El texto restante se divide en oraciones al encontrar `.`, `!` o `?` seguidos de un espacio.

## Resultados de la Fase 1

Los resultados actuales se basan en tres cuentos de Horacio Quiroga (*El almohadón de pluma*, *La gallina degollada*, *A la deriva*). 

- **Datos exportados:** Se generaron tres diccionarios de trayectoria narrativa (`_linea_temporal.json`) en la carpeta `data/processed/`.
- **Visualización:** Se crearon gráficas PNG en la carpeta `figures/` que mapean la evolución emocional de cada historia.

**Observaciones y Limitaciones:**

- Existe un fuerte desbalance hacia la etiqueta "Neutral" (por ejemplo, 99 de 154 oraciones en *La gallina degollada* se clasificaron como neutrales).
- El modelo tiene un umbral muy alto para detectar emociones literarias sutiles, ya que fue entrenado principalmente con textos de redes sociales. Las etiquetas de Tristeza, Enojo y Miedo se restringen casi exclusivamente a los clímax narrativos.
- Al asumir los diálogos como una sola unidad, intervenciones largas del narrador dentro del diálogo agrupan varias oraciones en una sola predicción, diluyendo emociones específicas.


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

| Necesidad | Fuente candidata |
|-----------|------------------|
| Textos en español (dominio público) | [Proyecto Gutenberg](https://www.gutenberg.org/), [Wikisource en español](https://es.wikisource.org/), [Biblioteca Virtual Miguel de Cervantes](https://www.cervantesvirtual.com/) |
| Audiolibros en español alineados con su texto | [Multilingual LibriSpeech — español](https://www.openslr.org/94/) (~918 h de LibriVox) |
| Voz en español etiquetada por emoción | [EmoMatchSpanishDB](https://link.springer.com/article/10.1007/s11042-023-15959-w) (2.005 audios, 7 emociones), [Spanish MEACorpus 2023](https://www.sciencedirect.com/science/article/pii/S0920548924000254) (13 h, 6 emociones) |

**Datos supervisados (planificado):** etiquetar a mano una muestra de oraciones de un capítulo con la emoción
correcta, para medir qué tan bien acierta el modelo automático y tener una base de comparación.

## Planificación

| Hito | Fecha aprox. | Meta |
|------|--------------|------|
| Hito 1 | fines de septiembre | Problema, datos, repositorio y prototipo de la Fase 1 |
| Hito 2 | fines de octubre | Fase 1 sobre un libro completo + Fase 2 concreta conectada a la Fase 1 (primer audio con emoción) |
| Hito 3 | fines de noviembre | Versión pulida: ejemplos, corpus, datos etiquetados y análisis de resultados (¿acierta la emoción? ¿la voz suena a esa emoción?) |

## Estructura del repositorio

```text
Acustica-Aun-sin-nombre/
├── README.md
├── requirements.txt
├── .gitignore                    # Reglas para ignorar el entorno virtual y temporales
├── docs/
│   └── seccion_benjamin.md       # Documentación metodológica de la Fase 1
├── src/
│   ├── limpiar_textos.py         # Preprocesamiento y unión de líneas
│   ├── Analisis_sentimientos.py  # Clasificación de emociones y exportación a JSON
│   └── graficar_emociones.py     # Generación de trayectoria emocional (pandas/matplotlib)
├── data/
│   ├── raw/                      # Textos originales descargados
│   └── processed/                # Textos limpios (_limpio.txt) y líneas temporales (.json)
├── results/                      # Audios generados en la Fase 2
├── notebooks/                    # Exploración y evaluación
├── figures/                      # Gráficos PNG de la trayectoria narrativa
└── references/                   # Bibliografía
## Presentación Hito 1

https://canva.link/hp4wto71mx5y0zl
## Referencias

- Pérez, J. M. et al. (2021). *pysentimiento: A Python Toolkit for Opinion Mining and Social NLP tasks.* arXiv:2106.09462.
- Michel, G., Epure, E. V. y Cerisara, C. (2025). *Computational Narrative Understanding for Expressive Text-to-Speech.* arXiv:2509.04072.
- Pratap, V. et al. (2020). *MLS: A Large-Scale Multilingual Dataset for Speech Research.* arXiv:2012.03411.

## Uso de IA

Usamos herramientas de IA generativa (Claude de Anthropic y Gemini de Google) como apoyo para estructurar el repositorio, depurar los scripts de Python, visualizar los datos y redactar la documentación. Las decisiones metodológicas, la limpieza de los textos originales y el análisis integral de los resultados son de exclusiva autoría del equipo.