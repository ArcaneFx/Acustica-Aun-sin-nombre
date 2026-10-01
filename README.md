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

### 2. Instalación

```bash
git clone https://github.com/ArcaneFx/Acustica-Aun-sin-nombre.git
cd Acustica-Aun-sin-nombre
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Ejecución

```bash
python src/Analisis_sentimientos.py
```

El script:

1. Carga el modelo de emociones (la primera vez tarda porque lo descarga).
2. Escribe un capítulo de ejemplo en `data/raw/capitulo_prueba.txt`.
3. Lo divide en oraciones y clasifica cada una.
4. Imprime una línea por oración con la emoción principal y la secundaria:

```
[001] (Neutral 99.4% + Sorpresa  0.2%) | Era de noche en la posada Roca de Guía.
```

### 4. Usarlo con otro texto

Desde Python (ejecutando dentro de `src/`), con cualquier archivo `.txt` en UTF-8:

```python
from Analisis_sentimientos import procesar_capitulo

historial = procesar_capitulo("../data/raw/mi_capitulo.txt")
```

Cada elemento de `historial` es un diccionario:

```python
{
    "id": 1,
    "texto": "Era de noche en la posada Roca de Guía.",
    "primaria":   {"emocion": "Neutral", "prob": 0.994},
    "secundaria": {"emocion": "Sorpresa", "prob": 0.002},
    "todas_las_probabilidades": {"others": 0.994, "surprise": 0.002, ...}
}
```

> Nota: importar el archivo ya carga el modelo, así que el `import` tarda unos segundos.

## Cómo divide el texto

- Separa el texto por líneas.
- Las líneas de diálogo (que empiezan con `—`, `-`, `«` o `"`) se tratan como una unidad completa.
- El resto se divide en oraciones al encontrar `.`, `!` o `?` seguidos de un espacio.

## Resultados del prototipo (Fase 1)

Salida real con el capítulo de ejemplo (guardada en [`results/fase1_capitulo_prueba.txt`](results/fase1_capitulo_prueba.txt)):

```
Procesando 8 oraciones del libro...
[001] (Neutral 99.4% + Sorpresa  0.2%) | Era de noche en la posada Roca de Guía.
[002] (Neutral 97.0% + Sorpresa  1.1%) | Un silencio triple envolvía el lugar,
[003] (Neutral 98.4% + Sorpresa  0.6%) | un silencio pesado que nacía de las cosas que no estaban allí.
[004] (Miedo 43.3% + Sorpresa 25.8%)   | De pronto, la puerta se abrió con violencia y un viajero empapado cayó de rodillas, temblando.
[005] (Sorpresa 57.0% + Miedo 14.2%)   | —¡Están en el camino! —gritó con desesperación—. ¡Los he visto con mis propios ojos!
[006] (Neutral 98.5% + Tristeza  1.0%) | El posadero no levantó la vista del vaso que limpiaba.
[007] (Neutral 58.3% + Miedo 27.2%)    | No había miedo en sus ojos, solo una calma fría.
[008] (Neutral 98.7% + Alegría  0.8%)  | Sirvió un trago de vino especiado y lo deslizó sobre la madera con total tranquilidad.
```

Observaciones:

- El modelo capta el giro de la escena: narración neutral → **miedo** (la puerta se abre) → **sorpresa** (el grito del viajero) → vuelta a la calma.
- **Palabras gatillo:** en `[007]` la palabra "miedo" sube Miedo a 27,2% aunque la oración dice que *no* había miedo. El modelo reacciona a la palabra más que al contexto.
- **Saltos de línea:** `[002]` y `[003]` son una sola oración que el salto de línea partió en dos.

**Limitaciones conocidas:**

- Las abreviaturas (`Sr.`, `etc.`) cortan la oración por error.
- Una oración que continúa en la línea siguiente queda partida en dos.
- Palabras emocionales sueltas pesan más que el contexto (negaciones como "no había miedo").
- El modelo fue entrenado con textos de redes sociales, no con literatura.

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

```
Acustica-Aun-sin-nombre/
├── README.md
├── requirements.txt
├── src/
│   └── Analisis_sentimientos.py  # Fase 1: segmentación + clasificación de emociones
├── data/
│   ├── raw/                      # Textos originales (capitulo_prueba.txt)
│   └── processed/                # Líneas temporales y datos etiquetados a mano (próximamente)
├── results/                      # Salidas: fase1_capitulo_prueba.txt; audios de la fase 2
├── notebooks/                    # Exploración y evaluación (próximamente)
├── figures/                      # Gráficos de la línea temporal emocional (próximamente)
└── references/                   # Bibliografía
```

## Referencias

- Pérez, J. M. et al. (2021). *pysentimiento: A Python Toolkit for Opinion Mining and Social NLP tasks.* arXiv:2106.09462.
- Michel, G., Epure, E. V. y Cerisara, C. (2025). *Computational Narrative Understanding for Expressive Text-to-Speech.* arXiv:2509.04072.
- Pratap, V. et al. (2020). *MLS: A Large-Scale Multilingual Dataset for Speech Research.* arXiv:2012.03411.

## Uso de IA

Usamos herramientas de IA generativa (Claude, de Anthropic) como apoyo para organizar el repositorio, documentar
y preparar la presentación. Las decisiones metodológicas, el código y el análisis son del equipo.
