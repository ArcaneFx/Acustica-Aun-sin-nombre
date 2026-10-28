"""Fase 2: narra una línea temporal emocional con un TTS local (Piper) y modulación acústica.

Piper no entiende emociones, así que la emoción de cada oración (campo `primaria` de la Fase 1) se
traduce a parámetros acústicos: velocidad, variación de la voz, tono, volumen y pausa final.
Los valores de PARAMETROS son una hipótesis de partida, no resultados medidos.

Uso (desde la raíz del repo):
    python src/fase2_narracion.py data/processed/ejemplo_linea_temporal.json --cuento ejemplo --base --unir

Requiere `ffmpeg` y una voz de Piper descargada en .cache/piper:
    python -m piper.download_voices --download-dir .cache/piper es_MX-claude-high
"""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

from piper import PiperVoice, SynthesisConfig

RAIZ = Path(__file__).resolve().parent.parent
DIR_VOCES = RAIZ / ".cache" / "piper"
DIR_AUDIOS = RAIZ / "results" / "audios"

# velocidad: length_scale de Piper (>1 = más lento) | variacion: noise_scale (más alto = entonación más variable)
# ritmo: noise_w_scale (más alto = duraciones de fonemas más irregulares) | tono: semitonos respecto a la voz base
# volumen: factor de ganancia | pausa: segundos de silencio tras una oración que termina en punto
PARAMETROS = {
    "Neutral":  {"velocidad": 1.00, "variacion": 0.667, "ritmo": 0.80, "tono": 0.0,  "volumen": 1.0,  "pausa": 0.40},
    "Alegría":  {"velocidad": 0.90, "variacion": 0.85,  "ritmo": 0.95, "tono": 1.5,  "volumen": 1.1,  "pausa": 0.35},
    "Tristeza": {"velocidad": 1.25, "variacion": 0.50,  "ritmo": 0.60, "tono": -2.0, "volumen": 0.8,  "pausa": 0.80},
    "Enojo":    {"velocidad": 0.95, "variacion": 0.90,  "ritmo": 0.90, "tono": -1.0, "volumen": 1.4,  "pausa": 0.30},
    "Miedo":    {"velocidad": 0.85, "variacion": 0.90,  "ritmo": 1.00, "tono": 2.5,  "volumen": 0.9,  "pausa": 0.30},
    "Sorpresa": {"velocidad": 0.92, "variacion": 0.85,  "ritmo": 0.95, "tono": 3.0,  "volumen": 1.15, "pausa": 0.45},
    "Disgusto": {"velocidad": 1.15, "variacion": 0.60,  "ritmo": 0.70, "tono": -1.5, "volumen": 0.95, "pausa": 0.50},
}

# Multiplica la pausa según cómo termina la oración: una coma deja la frase "abierta", los puntos suspensivos la dejan en el aire.
FACTOR_PAUSA = {".": 1.0, "!": 1.1, "?": 1.1, ":": 0.8, ";": 0.5, ",": 0.4, "…": 1.5}


def cargar_voz(nombre):
    ruta = DIR_VOCES / f"{nombre}.onnx"
    if not ruta.exists():
        raise SystemExit(f"No se encontró la voz {ruta}.\n"
                         f"Descárgala con: python -m piper.download_voices --download-dir {DIR_VOCES} {nombre}")
    return PiperVoice.load(ruta)


def pausa_final(texto, base, modo="contextual"):
    """Segundos de silencio tras la oración: fija, o ajustada por su puntuación final."""
    if modo == "fija":
        return base
    final = texto.rstrip().rstrip("»\"”')—- ")
    if final.endswith("..."):
        return base * FACTOR_PAUSA["…"]
    return base * FACTOR_PAUSA.get(final[-1:], 1.0)


def sintetizar(voz, texto, params):
    """Devuelve (bytes PCM int16 mono, frecuencia de muestreo) sin post-procesar."""
    config = SynthesisConfig(length_scale=params["velocidad"], noise_scale=params["variacion"],
                             noise_w_scale=params["ritmo"])
    trozos = list(voz.synthesize(texto, config))
    return b"".join(t.audio_int16_bytes for t in trozos), trozos[0].sample_rate


def modular(pcm, frecuencia, params, ruta_salida, pausa=None):
    """Aplica tono, volumen y pausa final con ffmpeg y guarda un WAV."""
    pausa = params["pausa"] if pausa is None else pausa
    factor = 2 ** (params["tono"] / 12)
    filtros = []
    if params["tono"]:
        # Cambia el tono sin cambiar la duración: remuestrea y compensa con atempo.
        filtros += [f"asetrate={frecuencia * factor:.0f}", f"aresample={frecuencia}", f"atempo={1 / factor:.5f}"]
    filtros += [f"volume={params['volumen']}", f"apad=pad_dur={pausa:.3f}"]
    comando = ["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", str(frecuencia), "-ac", "1",
               "-i", "-", "-af", ",".join(filtros), str(ruta_salida)]
    subprocess.run(comando, input=pcm, check=True)


def narrar(registros, voz, cuento, carpeta, ids=None, con_base=False, modo_pausas="contextual"):
    """Genera un WAV por oración con su emoción primaria; con `con_base`, también una versión neutral."""
    carpeta.mkdir(parents=True, exist_ok=True)
    generados = []
    for registro in registros:
        if ids and registro["id"] not in ids:
            continue
        emocion = registro["primaria"]["emocion"]
        variantes = [(emocion, f"{cuento}_{registro['id']:03d}_{emocion.lower()}.wav")]
        if con_base and emocion != "Neutral":
            variantes.append(("Neutral", f"{cuento}_{registro['id']:03d}_base.wav"))
        for emocion_usada, nombre in variantes:
            params = PARAMETROS[emocion_usada]
            pcm, frecuencia = sintetizar(voz, registro["texto"], params)
            modular(pcm, frecuencia, params, carpeta / nombre,
                    pausa_final(registro["texto"], params["pausa"], modo_pausas))
            generados.append((nombre, emocion, registro))
            print(f"[{registro['id']:03d}] {nombre:<45} {registro['texto'][:60]}")
    return generados


def unir(generados, ruta_salida):
    """Concatena los audios con emoción (sin los `_base`) en una sola narración continua."""
    nombres = [n for n, _, _ in generados if not n.endswith("_base.wav")]
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as lista:
        for nombre in nombres:
            lista.write(f"file '{(ruta_salida.parent / nombre).resolve()}'\n")
    try:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                        "-i", lista.name, "-c", "copy", str(ruta_salida)], check=True)
    finally:
        Path(lista.name).unlink()
    print(f"Narración continua: {ruta_salida} ({len(nombres)} oraciones)")


def escribir_readme(generados, carpeta, voz_nombre):
    """Tabla de qué oración y emoción tiene cada audio (la pide el contrato)."""
    ruta = carpeta / "README.md"
    nuevas = {f"| `{nombre}` |": f"| `{nombre}` | {emocion} ({registro['primaria']['prob']:.0%}) | {registro['texto']} |"
              for nombre, emocion, registro in generados}
    # Conserva las filas de corridas anteriores (otros cuentos) y reemplaza las de estos archivos.
    previas = []
    if ruta.exists():
        previas = [l for l in ruta.read_text(encoding="utf-8").splitlines()
                   if l.startswith("| `") and not any(l.startswith(clave) for clave in nuevas)]
    lineas = ["# Audios de la Fase 2", "",
              f"Voz: `{voz_nombre}` (Piper, local). Los archivos `*_base.wav` son la misma oración sin modulación emocional.", "",
              "| Archivo | Emoción detectada | Oración |", "|---|---|---|"] + previas + list(nuevas.values())
    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("linea_temporal", type=Path, help="JSON de la Fase 1 (ver docs/contrato.md)")
    parser.add_argument("--cuento", required=True, help="prefijo de los archivos, p. ej. quiroga_a_la_deriva")
    parser.add_argument("--voz", default="es_MX-claude-high")
    parser.add_argument("--ids", type=int, nargs="+", help="solo estas oraciones (por defecto, todas)")
    parser.add_argument("--base", action="store_true", help="también genera la versión neutral para comparar")
    parser.add_argument("--salida", type=Path, default=DIR_AUDIOS)
    parser.add_argument("--pausas", choices=["contextual", "fija"], default="contextual",
                        help="contextual: la pausa depende de la puntuación final de la oración")
    parser.add_argument("--unir", action="store_true", help="también genera <cuento>_narracion.wav con todo seguido")
    args = parser.parse_args()

    with open(args.linea_temporal, encoding="utf-8") as f:
        registros = json.load(f)
    generados = narrar(registros, cargar_voz(args.voz), args.cuento, args.salida, args.ids, args.base, args.pausas)
    escribir_readme(generados, args.salida, args.voz)
    if args.unir:
        sufijo = "" if args.pausas == "contextual" else "_pausa_fija"
        unir(generados, args.salida / f"{args.cuento}_narracion{sufijo}.wav")
