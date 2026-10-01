import re
from pathlib import Path
from pysentimiento import create_analyzer

print("Cargando modelo de emociones...")
analyzer = create_analyzer(task="emotion", lang="es")

EMOCIONES = {
    "joy": "Alegría",
    "sadness": "Tristeza",
    "anger": "Enojo",
    "fear": "Miedo",
    "others": "Neutral",
    "surprise": "Sorpresa",
    "disgust": "Disgusto"
}

def segmentar_en_oraciones(texto):
    lineas = texto.strip().split("\n")
    oraciones_finales = []

    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
        
        if linea.startswith("—") or linea.startswith("-") or linea.startswith("«") or linea.startswith('"'):
            oraciones_finales.append(linea)
        else:
            partes = re.split(r'(?<=[.!?])\s+', linea)
            for p in partes:
                p_limpia = p.strip()
                if len(p_limpia) > 2:
                    oraciones_finales.append(p_limpia)

    return oraciones_finales

def procesar_capitulo(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()

    oraciones = segmentar_en_oraciones(contenido)
    linea_temporal_emociones = []

    print(f"\nProcesando {len(oraciones)} oraciones del libro...")
    print("=" * 80)

    for i, oracion in enumerate(oraciones, start=1):
        res = analyzer.predict(oracion)
        
        # Ordenar todas las probabilidades de mayor a menor
        probabilidades_ordenadas = sorted(
            res.probas.items(), 
            key=lambda item: item[1], 
            reverse=True
        )
        
        # 1ra emoción dominante
        emo_1_key, prob_1 = probabilidades_ordenadas[0]
        emo_1 = EMOCIONES.get(emo_1_key, emo_1_key)
        
        # 2da emoción dominante
        emo_2_key, prob_2 = probabilidades_ordenadas[1]
        emo_2 = EMOCIONES.get(emo_2_key, emo_2_key)

        registro = {
            "id": i,
            "texto": oracion,
            "primaria": {"emocion": emo_1, "prob": round(prob_1, 3)},
            "secundaria": {"emocion": emo_2, "prob": round(prob_2, 3)},
            "todas_las_probabilidades": {k: round(v, 3) for k, v in res.probas.items()}
        }
        linea_temporal_emociones.append(registro)

        # Formato: [ID] Primaria (X%) + Secundaria (Y%) | Texto
        etiqueta_dual = f"{emo_1} {prob_1*100:4.1f}% + {emo_2} {prob_2*100:4.1f}%"
        print(f"[{i:03d}] ({etiqueta_dual:<32}) | {oracion}")

    return linea_temporal_emociones

if __name__ == "__main__":
    capitulo_ejemplo = """
    Era de noche en la posada Roca de Guía. Un silencio triple envolvía el lugar, 
    un silencio pesado que nacía de las cosas que no estaban allí.
    De pronto, la puerta se abrió con violencia y un viajero empapado cayó de rodillas, temblando.
    —¡Están en el camino! —gritó con desesperación—. ¡Los he visto con mis propios ojos!
    El posadero no levantó la vista del vaso que limpiaba. No había miedo en sus ojos, solo una calma fría.
    Sirvió un trago de vino especiado y lo deslizó sobre la madera con total tranquilidad.
    """
    
    # El capítulo de ejemplo se guarda en data/raw/ (relativo a la raíz del repo)
    ruta_capitulo = Path(__file__).resolve().parent.parent / "data" / "raw" / "capitulo_prueba.txt"
    ruta_capitulo.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta_capitulo, "w", encoding="utf-8") as f:
        f.write(capitulo_ejemplo)

    historial = procesar_capitulo(ruta_capitulo)