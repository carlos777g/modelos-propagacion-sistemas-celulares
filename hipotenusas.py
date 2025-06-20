import json
import numpy as np

hipotenusa = []
with open("datos.json", 'r') as f:
        data = json.load(f)

h_bs = data["base_station_height"]

for movil in data["mobiles"]:
        d_rx = movil["distance"]
        d_total = round(np.sqrt(np.power(d_rx, 2) + np.power(h_bs, 2)), 3)
        movil["real_distance"] = d_total
        print(f"Distancia real entre antenas: {d_total}")

# Guarda el archivo actualizado
with open("datos.json", 'w') as f:
    json.dump(data, f, indent=2)