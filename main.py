import json
import matplotlib.pyplot as plt
import math
from archivos_python.determiarLOS import determinar_los
from archivos_python.walfish_ikegami import loss_los, loss_nlos
from archivos_python.logNormal import model_lognormal

# Parámetros globales
FREQ_MHZ = 1935
Pt_dBm = 10 * math.log10(10) + 30  # 10 W
Gt_dB = 9
Gr_dB = 3
alpha = 2.8
sigma = 7


def main():
    # Cargar datos
    with open('datos.json', 'r') as f:
        data = json.load(f)

    h_bs = data['base_station_height']
    h_mvs = data['mobile_height']
    h_prom = data['h_prom_buildings']

    # Obtener LoS/NLoS
    los_list = determinar_los('datos.json')
    # print(los_list)
    # Modelos
    wi_results = []
    print("-"*17 + "Modelo Walfish-Ikegami"+ "-"*17)
    for i, m in enumerate(data['mobiles']):
        d = m['real_distance']
        phi = m['angle_deg']
        w = m['street_weight']
        b = data['prom_distance_buildings']
        if los_list[i]['los']:
            Lb = loss_los(d, FREQ_MHZ)
        else:
            Lb = loss_nlos(d, FREQ_MHZ, h_bs, h_mvs, h_prom, phi, w, b)
        Prx = Pt_dBm + Gt_dB + Gr_dB - Lb

        if(los_list[i]["los"]):
            print(f"Hay LOS; Perdidas: {Lb},  Prx: {Prx}")
        else: 
            print(f"No hay LOS; Perdidas: {Lb},  Prx: {Prx}")
        
        
        wi_results.append({'distance': d, 'Prx': Prx})

    # Lognormal
    ln_results = model_lognormal(data['mobiles'], Pt_dBm, Gt_dB, Gr_dB, alpha, sigma)

    # Graficar
    distances = [r['distance'] for r in wi_results]
    Pr_wi = [r['Prx'] for r in wi_results]
    Pr_ln = [r['Pr_log'] for r in ln_results]

    plt.figure()
    plt.plot(distances, Pr_wi, 'o-', label='Walfish-Ikegami')  # sin especificar color
    plt.plot(distances, Pr_ln, 's--', label='Lognormal')
    plt.xlabel('Distancia (m)')
    plt.ylabel('Potencia recibida (dBm)')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()