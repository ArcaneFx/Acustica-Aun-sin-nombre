import os
import json
import re
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

def procesar_texto(ruta_entrada, ruta_salida):
    with open(ruta_entrada, 'r', encoding='utf-8') as f:
        contenido = f.read()

    oraciones = segmentar_en_oraciones(contenido)
    linea_temporal_emociones = []
    distribucion = {v: 0 for v in EMOCIONES.values()}

    print(f"\nProcesando {len(oraciones)} oraciones de {ruta_entrada}...")
    
    for i, oracion in enumerate(oraciones, start=1):
        res = analyzer.predict(oracion)
        probabilidades_ordenadas = sorted(res.probas.items(), key=lambda item: item[1], reverse=True)
        
        emo_1_key, prob_1 = probabilidades_ordenadas[0]
        emo_1 = EMOCIONES.get(emo_1_key, emo_1_key)
        emo_2_key, prob_2 = probabilidades_ordenadas[1]
        emo_2 = EMOCIONES.get(emo_2_key, emo_2_key)

        # Contabilizar para la distribución de emociones
        distribucion[emo_1] += 1

        registro = {
            "id": i,
            "texto": oracion,
            "primaria": {"emocion": emo_1, "prob": round(prob_1, 3)},
            "secundaria": {"emocion": emo_2, "prob": round(prob_2, 3)},
            "todas_las_probabilidades": {k: round(v, 3) for k, v in res.probas.items()}
        }
        linea_temporal_emociones.append(registro)

    # Guardar en formato JSON (Contrato Fase 2)
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        json.dump(linea_temporal_emociones, f, ensure_ascii=False, indent=4)
    
    print(f"Guardado: {ruta_salida}")
    print(f"Distribución de emociones primarias: {distribucion}")

if __name__ == "__main__":
    cuentos = [
        "quiroga_el_almohadon_de_pluma",
        "quiroga_la_gallina_degollada",
        "quiroga_a_la_deriva"
    ]
    
    for cuento in cuentos:
        ruta_in = f"data/processed/{cuento}_limpio.txt"
        ruta_out = f"data/processed/{cuento}_linea_temporal.json"
        
        if os.path.exists(ruta_in):
            procesar_texto(ruta_in, ruta_out)
        else:
            print(f"Archivo limpio no encontrado: {ruta_in}. Ejecuta limpiar_textos.py primero.")