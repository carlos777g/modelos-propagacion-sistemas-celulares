import json
from archivos_python.determiarLOS import determinar_los
from archivos_python.walfish_ikegami import loss_los, loss_nlos

FREQ_MHZ = 1935  # puedes ajustar

def main():
    with open("datos.json") as f:
        data = json.load(f)

    h_bs = data["base_station_height"]
    h_mvs = data["mobile_height"]
    h_prom_buildings = data["h_prom_buildings"]

    los_resultados = determinar_los("datos.json")

    print("Resultados del modelo COST-231 Walfish-Ikegami:")
    print("-" * 80)

    for i, movil in enumerate(data["mobiles"]):
        real_distance = movil["real_distance"]
        phi = movil["angle_deg"]
        los = los_resultados[i]["los"]
        street_weight = movil["street_weight"]
        if los:
            loss = loss_los(real_distance, FREQ_MHZ)
            tipo = "LoS"
        else:
            loss = loss_nlos(real_distance, FREQ_MHZ, h_bs, h_mvs, h_prom_buildings, phi, street_weight, h_prom_buildings)
            tipo = "NLoS"

        print(f"{tipo:4} | Distancia = {real_distance:7.2f} m | Ángulo = {phi:5.1f}° | Lb = {loss:7.2f} dB")

if __name__ == "__main__":
    main()
