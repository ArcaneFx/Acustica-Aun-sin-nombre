import os

def limpiar_cuento(ruta_entrada, ruta_salida):
    with open(ruta_entrada, 'r', encoding='utf-8') as f:
        texto_completo = f.read()

    # 1. Quitar el título: primera línea con el formato #TITULO DEL CUENTO# (el título real, no un texto fijo)
    lineas = texto_completo.split('\n')
    primera = lineas[0].strip() if lineas else ""
    if len(primera) > 1 and primera.startswith('#') and primera.endswith('#'):
        lineas = lineas[1:]
    
    texto_sin_titulo = "\n".join(lineas)
    
    # 2. Unir párrafos cortados (separados por doble salto de línea)
    parrafos = texto_sin_titulo.split('\n\n')
    parrafos_limpios = []
    
    for p in parrafos:
        p_limpio = p.strip()
        if not p_limpio:
            continue
            
        # Unir líneas del mismo párrafo con un espacio
        p_unido = " ".join(p_limpio.split())
        
        # 3. Pasar -- a — (sin añadir espacios extra)
        p_unido = p_unido.replace('--', '—')
        
        parrafos_limpios.append(p_unido)
        
    # Guardar el texto limpio
    texto_final = "\n\n".join(parrafos_limpios)
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(texto_final)
    
    print(f"Procesado: {ruta_salida}")

if __name__ == "__main__":
    cuentos = [
        "quiroga_el_almohadon_de_pluma",
        "quiroga_la_gallina_degollada",
        "quiroga_a_la_deriva"
    ]
    
    for cuento in cuentos:
        entrada = f"data/raw/{cuento}.txt"
        salida = f"data/processed/{cuento}_limpio.txt"
        
        if os.path.exists(entrada):
            limpiar_cuento(entrada, salida)
        else:
            print(f"Falta el archivo: {entrada}")