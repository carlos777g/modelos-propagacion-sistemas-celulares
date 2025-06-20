import json
import numpy as np

hipotenusa = []
with open("datos.json", 'r') as f:
        data = json.load(f)
# Sacamos la altura de la estación base menos la altura de la posición del móvil
h_bs = data["base_station_height"] - data["mobile_height"]

for movil in data["mobiles"]:
        d_rx = movil["distance_x"]
        d_total = round(np.sqrt(np.power(d_rx, 2) + np.power(h_bs, 2)), 3)
        movil["real_distance"] = d_total
        print(f'"real_distance": {d_total},')
# En el print anterior obtebemos la distancia entre la BS y cada móvil (hipotenusa de un triangulo escaleno)
