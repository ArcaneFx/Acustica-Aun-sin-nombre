"""Flujo completo del proyecto, de punta a punta, mostrando cada paso en la terminal.

    cuento crudo -> 1. limpieza -> 2. Fase 1 (emociones) -> 3. evaluación -> 4. gráfico -> 5. Fase 2 (audio)

Uso (desde la raíz del repo, con el entorno activado):
    python script.py                                   # los 3 cuentos completos
    python script.py --cuentos quiroga_a_la_deriva     # un solo cuento
    python script.py --limite 10                       # narrar solo las primeras 10 oraciones (prueba rápida)
    python script.py --reusar-json                     # no vuelve a correr el modelo si el JSON ya existe

Requiere `ffmpeg` y la voz de Piper es_MX-claude-high (se descarga sola si falta).
"""
import argparse
import shutil
import subprocess
import sys
import time
import wave
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "src"))

CUENTOS = {
    "quiroga_el_almohadon_de_pluma": "El Almohadón de Pluma",
    "quiroga_la_gallina_degollada": "La Gallina Degollada",
    "quiroga_a_la_deriva": "A la Deriva",
}
VOZ_POR_DEFECTO = "es_MX-claude-high"
DIR_VOCES = RAIZ / ".cache" / "piper"
ANCHO = 78


def banner(texto, nivel=1):
    """Imprime un encabezado bien visible para seguir el flujo en la terminal."""
    if nivel == 1:
        print("\n" + "#" * ANCHO)
        print(f"# {texto}")
        print("#" * ANCHO, flush=True)
    else:
        print("\n" + "=" * ANCHO)
        print(f"== {texto}")
        print("=" * ANCHO, flush=True)


def paso(numero, total, texto):
    print(f"\n--- Paso {numero}/{total}: {texto} " + "-" * max(3, ANCHO - 16 - len(texto)), flush=True)


def duracion_wav(ruta):
    with wave.open(str(ruta)) as w:
        return w.getnframes() / w.getframerate()


def barra(cantidad, total, ancho=30):
    llenos = round(ancho * cantidad / total) if total else 0
    return "█" * llenos + "·" * (ancho - llenos)


def revisar_entorno(voz, sin_audio):
    banner("Paso 0: revisando el entorno", 2)
    print(f"Python {sys.version.split()[0]} | repo: {RAIZ}")
    if sin_audio:
        print("--sin-audio: no se revisa ffmpeg ni la voz.")
        return
    if shutil.which("ffmpeg") is None:
        raise SystemExit("Falta ffmpeg (dependencia del sistema). Instálalo y vuelve a correr el script.")
    print("ffmpeg: OK")
    if not (DIR_VOCES / f"{voz}.onnx").exists():
        print(f"La voz {voz} no está en {DIR_VOCES}; descargándola (unos 60 MB)...", flush=True)
        subprocess.run([sys.executable, "-m", "piper.download_voices", "--download-dir", str(DIR_VOCES), voz], check=True)
    print(f"Voz de Piper: {voz} OK")


def paso_limpieza(cuento):
    from limpiar_textos import limpiar_cuento
    crudo = RAIZ / "data" / "raw" / f"{cuento}.txt"
    limpio = RAIZ / "data" / "processed" / f"{cuento}_limpio.txt"
    if not crudo.exists():
        raise SystemExit(f"Falta el texto original: {crudo}")
    limpiar_cuento(crudo, limpio)
    texto = limpio.read_text(encoding="utf-8")
    parrafos = [p for p in texto.split("\n\n") if p.strip()]
    print(f"Texto original: {len(crudo.read_text(encoding='utf-8').splitlines())} líneas -> "
          f"limpio: {len(parrafos)} párrafos, {len(texto.split())} palabras")
    print(f"Empieza así: {parrafos[0][:90]}...")
    return limpio


def paso_fase1(cuento, limpio, reusar):
    import json
    ruta_json = RAIZ / "data" / "processed" / f"{cuento}_linea_temporal.json"
    if reusar and ruta_json.exists():
        print(f"--reusar-json: se usa {ruta_json.name} sin volver a correr el modelo.")
    else:
        print("Importando pysentimiento y cargando el modelo (la primera vez tarda)...", flush=True)
        from Analisis_sentimientos import procesar_texto
        procesar_texto(limpio, ruta_json)
    registros = json.loads(ruta_json.read_text(encoding="utf-8"))

    print(f"\nOración por oración (emoción primaria + secundaria):")
    for r in registros:
        p, s = r["primaria"], r["secundaria"]
        etiqueta = f"{p['emocion']} {p['prob'] * 100:4.1f}% + {s['emocion']} {s['prob'] * 100:4.1f}%"
        print(f"[{r['id']:03d}] ({etiqueta:<34}) | {r['texto'][:90]}")

    cuenta = Counter(r["primaria"]["emocion"] for r in registros)
    print(f"\nDistribución de emociones primarias ({len(registros)} oraciones):")
    for emocion, n in cuenta.most_common():
        print(f"  {emocion:<9}{barra(n, len(registros))} {n:>4}  ({n / len(registros):.0%})")
    return ruta_json, registros, cuenta


def paso_evaluacion(registros):
    from evaluacion import cargar_etiquetas, informe, unir, RUTA_ETIQUETAS
    etiquetas = cargar_etiquetas(RUTA_ETIQUETAS)
    pares = unir(registros, etiquetas)
    if not pares:
        print("No hay etiquetas manuales para este cuento: se omite la evaluación.")
        return
    lineas = informe(pares, len(etiquetas)).splitlines()
    print("\n".join(lineas[:3]))
    mas_comun = Counter(real for _, real in pares).most_common(1)[0]
    print(f"Referencia: decir siempre '{mas_comun[0]}' acertaría {mas_comun[1]}/{len(pares)} = {mas_comun[1] / len(pares):.1%}")
    print("(informe completo, matriz de confusión y errores: python src/evaluacion.py <json>)")


def paso_grafico(cuento, ruta_json):
    from graficar_emociones import graficar_linea_temporal
    (RAIZ / "figures").mkdir(exist_ok=True)
    graficar_linea_temporal(ruta_json, RAIZ / "figures" / f"{cuento}_timeline.png", CUENTOS.get(cuento, cuento))


def paso_fase2(cuento, registros, voz_nombre, carpeta, limite, con_base):
    from fase2_narracion import PARAMETROS, cargar_voz, escribir_readme, narrar, unir
    if limite:
        registros = registros[:limite]
    emociones = Counter(r["primaria"]["emocion"] for r in registros)
    print(f"Se narran {len(registros)} oraciones con la voz {voz_nombre} (Piper, local, CPU).")
    print("Cada emoción se traduce a parámetros acústicos (velocidad, tono, volumen, pausa):")
    for emocion in emociones:
        p = PARAMETROS[emocion]
        print(f"  {emocion:<9} x{emociones[emocion]:<3} velocidad={p['velocidad']:.2f} tono={p['tono']:+.1f} st "
              f"volumen={p['volumen']:.2f} pausa={p['pausa']:.2f}s")
    print("\nSintetizando:", flush=True)
    voz = cargar_voz(voz_nombre)
    generados = narrar(registros, voz, cuento, carpeta, None, con_base, "contextual")
    escribir_readme(generados, carpeta, voz_nombre)
    final = carpeta / f"{cuento}_narracion.wav"
    unir(generados, final)
    print(f"Archivos: {len(generados)} WAV + README.md en {carpeta.relative_to(RAIZ)}")
    return final


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--cuentos", nargs="+", default=list(CUENTOS), help="nombres de archivo en data/raw sin .txt")
    parser.add_argument("--limite", type=int, help="narrar solo las primeras N oraciones de cada cuento")
    parser.add_argument("--voz", default=VOZ_POR_DEFECTO)
    parser.add_argument("--salida", type=Path, default=RAIZ / "results" / "audios" / "pipeline")
    parser.add_argument("--base", action="store_true", help="también genera la versión sin modulación de cada oración")
    parser.add_argument("--sin-audio", action="store_true", help="solo limpieza, Fase 1, evaluación y gráfico")
    parser.add_argument("--reusar-json", action="store_true", help="usar el JSON existente en vez de correr el modelo")
    args = parser.parse_args()

    inicio = time.perf_counter()
    banner("ACÚSTICA: de texto a narración emocional")
    print(f"Cuentos: {', '.join(args.cuentos)}")
    revisar_entorno(args.voz, args.sin_audio)

    total = 4 if args.sin_audio else 5
    resumen = []
    for numero, cuento in enumerate(args.cuentos, start=1):
        t0 = time.perf_counter()
        banner(f"Cuento {numero}/{len(args.cuentos)}: {CUENTOS.get(cuento, cuento)}  [{cuento}]", 2)
        paso(1, total, "Limpieza del texto (quitar título, unir líneas, normalizar diálogos)")
        limpio = paso_limpieza(cuento)
        paso(2, total, "Fase 1: emoción de cada oración con pysentimiento")
        ruta_json, registros, cuenta = paso_fase1(cuento, limpio, args.reusar_json)
        paso(3, total, "Evaluación contra las etiquetas manuales (si existen)")
        paso_evaluacion(registros)
        paso(4, total, "Gráfico de la línea temporal emocional")
        paso_grafico(cuento, ruta_json)
        audio = None
        if not args.sin_audio:
            paso(5, total, "Fase 2: narración con Piper y modulación por emoción")
            audio = paso_fase2(cuento, registros, args.voz, args.salida / cuento, args.limite, args.base)
        resumen.append((cuento, len(registros), cuenta["Neutral"], audio, time.perf_counter() - t0))

    banner("RESUMEN")
    for cuento, n, neutral, audio, segundos in resumen:
        extra = f" | audio {duracion_wav(audio):.0f} s -> {audio.relative_to(RAIZ)}" if audio else ""
        print(f"{cuento:<32}{n:>4} oraciones | {neutral / n:.0%} Neutral{extra} | {segundos:.0f} s")
    print(f"\nTiempo total: {time.perf_counter() - inicio:.0f} s")


if __name__ == "__main__":
    main()
