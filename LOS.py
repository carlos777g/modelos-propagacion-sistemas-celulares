import json

def check_los(h_bs, h_mvs, buildings, d_rx):
    """
    Verifica si hay línea de vista desde la BS al punto a d_rx metros.
    """
    m = (h_mvs - h_bs) / d_rx

    for b in buildings:
        x = b["x"]
        if x < d_rx:  # sólo evaluamos edificios entre BS y móvil
            h_line = h_bs + m * x
            if b["height"] > h_line:
                return False  # Obstrucción
    return True  # No hay obstrucción

def analizar_los_desde_json(ruta_archivo):
    """
    Retorna booleano para decir si hay LOS o no.
    """
    with open(ruta_archivo, 'r') as f:
        data = json.load(f)

    h_bs = data["base_station_height"]
    h_mvs = data["mobile_height"]
    buildings = data["buildings"]
    resultados = []

    for movil in data["mobiles"]:
        d_rx = movil["distance"]
        los = check_los(h_bs, h_mvs, buildings, d_rx)
        resultados.append({
            "distance": d_rx,
            "los": los
        })

    return resultados


if __name__ == "__main__":
    resultados = analizar_los_desde_json("datos.json")
    for r in resultados:
        print(f"Distancia: {r['distance']} m → {'LoS' if r['los'] else 'NLoS'}")
