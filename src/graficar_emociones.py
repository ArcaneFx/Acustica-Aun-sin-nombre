import os
import json
import pandas as pd
import matplotlib.pyplot as plt

def graficar_linea_temporal(ruta_json, ruta_imagen, titulo):
    with open(ruta_json, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    # Convertir a DataFrame
    df = pd.DataFrame([
        {"id": item["id"], "emocion": item["primaria"]["emocion"], "prob": item["primaria"]["prob"]}
        for item in datos
    ])

    # Definir orden y colores
    emociones_orden = ["Alegría", "Sorpresa", "Neutral", "Tristeza", "Miedo", "Disgusto", "Enojo"]
    colores = {"Alegría": "gold", "Sorpresa": "orange", "Neutral": "gray", "Tristeza": "blue", "Miedo": "purple", "Disgusto": "green", "Enojo": "red"}

    df['emocion'] = pd.Categorical(df['emocion'], categories=emociones_orden, ordered=True)

    plt.figure(figsize=(12, 6))
    
    # Graficar puntos con tamaño dependiente de la probabilidad
    for emocion, color in colores.items():
        sub_df = df[df['emocion'] == emocion]
        plt.scatter(sub_df['id'], sub_df['emocion'], c=color, label=emocion, s=sub_df['prob']*100, alpha=0.7)

    # Línea conectora tenue para visualizar la trayectoria narrativa
    plt.plot(df['id'], df['emocion'], color='gray', alpha=0.3, linewidth=1)

    plt.title(f"Línea Temporal Emocional - {titulo}")
    plt.xlabel("ID de Oración")
    plt.ylabel("Emoción Primaria")
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(ruta_imagen)
    plt.close()
    print(f"Gráfico guardado en: {ruta_imagen}")

if __name__ == "__main__":
    os.makedirs("figures", exist_ok=True)
    
    cuentos = {
        "quiroga_el_almohadon_de_pluma": "El Almohadón de Pluma",
        "quiroga_la_gallina_degollada": "La Gallina Degollada",
        "quiroga_a_la_deriva": "A la Deriva"
    }
    
    for archivo, titulo in cuentos.items():
        ruta_in = f"data/processed/{archivo}_linea_temporal.json"
        ruta_out = f"figures/{archivo}_timeline.png"
        
        if os.path.exists(ruta_in):
            graficar_linea_temporal(ruta_in, ruta_out, titulo)
        else:
            print(f"No se encontró el archivo: {ruta_in}")