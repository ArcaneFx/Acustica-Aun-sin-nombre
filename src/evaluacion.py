"""Evaluación de la Fase 1: compara las emociones predichas con las etiquetadas a mano.

No carga el modelo: lee el JSON que guarda la Fase 1 y un CSV de etiquetas manuales,
y los une por el texto de la oración (no por id, porque la segmentación puede cambiar).

Uso (desde la raíz del repo):
    python src/evaluacion.py --plantilla data/processed/ejemplo_linea_temporal.json
    python src/evaluacion.py data/processed/ejemplo_linea_temporal.json
"""
import argparse
import csv
import json
import unicodedata
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
RUTA_ETIQUETAS = RAIZ / "data" / "processed" / "etiquetas_manuales.csv"
EMOCIONES = ["Alegría", "Tristeza", "Enojo", "Miedo", "Sorpresa", "Disgusto", "Neutral"]


def normalizar(texto):
    """Clave de unión: sin diferencias de espacios, mayúsculas ni acentos compuestos."""
    texto = unicodedata.normalize("NFC", texto)
    return " ".join(texto.split()).casefold()


def cargar_predicciones(ruta_json):
    with open(ruta_json, encoding="utf-8") as f:
        return json.load(f)


def cargar_etiquetas(ruta_csv):
    """Devuelve {texto_normalizado: [emociones etiquetadas]} ignorando filas sin etiqueta."""
    etiquetas = {}
    with open(ruta_csv, encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f):
            emocion = fila["emocion_manual"].strip()
            if not emocion:
                continue
            if emocion not in EMOCIONES:
                raise ValueError(f"Emoción no válida {emocion!r} en: {fila['texto'][:50]}")
            etiquetas.setdefault(normalizar(fila["texto"]), []).append(emocion)
    return etiquetas


def unir(predicciones, etiquetas):
    """Pares (registro, emocion_manual) para las oraciones que tienen etiqueta."""
    pares = []
    for registro in predicciones:
        manuales = etiquetas.get(normalizar(registro["texto"]))
        if manuales:
            # Si hay varias etiquetas (varios etiquetadores) se usa la más frecuente.
            pares.append((registro, Counter(manuales).most_common(1)[0][0]))
    return pares


def matriz_confusion(pares):
    matriz = {real: Counter() for real in EMOCIONES}
    for registro, real in pares:
        matriz[real][registro["primaria"]["emocion"]] += 1
    return matriz


def informe(pares, total_etiquetadas):
    n = len(pares)
    lineas = [f"Oraciones etiquetadas: {total_etiquetadas} | encontradas en las predicciones: {n}"]
    if n == 0:
        return "\n".join(lineas + ["No hay oraciones para evaluar."])

    aciertos = sum(r["primaria"]["emocion"] == real for r, real in pares)
    aciertos_top2 = sum(real in (r["primaria"]["emocion"], r["secundaria"]["emocion"]) for r, real in pares)
    lineas.append(f"Acierto (emoción primaria):          {aciertos}/{n} = {aciertos / n:.1%}")
    lineas.append(f"Acierto (primaria o secundaria):     {aciertos_top2}/{n} = {aciertos_top2 / n:.1%}")

    matriz = matriz_confusion(pares)
    ancho = 9
    lineas += ["", "Matriz de confusión (filas = etiqueta manual, columnas = predicción del modelo)"]
    lineas.append(" " * ancho + "".join(f"{e[:ancho - 1]:>{ancho}}" for e in EMOCIONES))
    for real in EMOCIONES:
        if sum(matriz[real].values()):
            lineas.append(f"{real[:ancho - 1]:<{ancho}}" + "".join(f"{matriz[real][p]:>{ancho}}" for p in EMOCIONES))

    lineas += ["", f"{'Emoción':<10}{'Etiquetadas':>12}{'Predichas':>11}{'Precisión':>11}{'Recall':>9}"]
    for emocion in EMOCIONES:
        reales = sum(matriz[emocion].values())
        predichas = sum(matriz[r][emocion] for r in EMOCIONES)
        bien = matriz[emocion][emocion]
        precision = f"{bien / predichas:.0%}" if predichas else "-"
        recall = f"{bien / reales:.0%}" if reales else "-"
        if reales or predichas:
            lineas.append(f"{emocion:<10}{reales:>12}{predichas:>11}{precision:>11}{recall:>9}")

    errores = [(r, real) for r, real in pares if r["primaria"]["emocion"] != real]
    if errores:
        lineas += ["", "Errores (para interpretar):"]
        for r, real in errores:
            p = r["primaria"]
            lineas.append(f"- manual={real} | modelo={p['emocion']} {p['prob']:.0%} | {r['texto']}")
    return "\n".join(lineas)


def escribir_plantilla(predicciones, ruta_csv):
    """Crea un CSV listo para etiquetar (no sobrescribe uno existente con etiquetas)."""
    if ruta_csv.exists() and ruta_csv.stat().st_size > len("texto,emocion_manual,etiquetador\n"):
        raise SystemExit(f"{ruta_csv} ya tiene contenido; no se sobrescribe.")
    with open(ruta_csv, "w", encoding="utf-8", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerow(["texto", "emocion_manual", "etiquetador"])
        for registro in predicciones:
            escritor.writerow([registro["texto"], "", ""])
    print(f"Plantilla escrita en {ruta_csv} ({len(predicciones)} oraciones). "
          f"Completa 'emocion_manual' con: {', '.join(EMOCIONES)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("predicciones", help="JSON de la Fase 1 (lista de registros)")
    parser.add_argument("--etiquetas", default=RUTA_ETIQUETAS, type=Path, help="CSV de etiquetas manuales")
    parser.add_argument("--plantilla", action="store_true",
                        help="en vez de evaluar, genera el CSV de etiquetas vacío a partir de las predicciones")
    parser.add_argument("--salida", type=Path, help="guarda el informe en este archivo además de imprimirlo")
    args = parser.parse_args()

    predicciones = cargar_predicciones(args.predicciones)
    if args.plantilla:
        escribir_plantilla(predicciones, args.etiquetas)
    else:
        etiquetas = cargar_etiquetas(args.etiquetas)
        texto_informe = informe(unir(predicciones, etiquetas), len(etiquetas))
        print(texto_informe)
        if args.salida:
            args.salida.write_text(texto_informe + "\n", encoding="utf-8")
