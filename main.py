import json
import matplotlib.pyplot as plt
import math
from rich import print
from rich.table import Table
from archivos_python.determiarLOS import determinar_los
from archivos_python.walfish_ikegami import loss_los, loss_nlos
from archivos_python.logNormal import model_lognormal, generar_tabla_lognormal
from archivos_python.espacio_libre import model_free_space
from archivos_python.superficie_reflejante import model_two_ray


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
    table_walfish = Table(title="[bold magenta]Resultados Modelo Walfish-Ikegami[bold magenta]")
    table_walfish.add_column("Puntos", justify="center")
    table_walfish.add_column("LOS", justify="center")
    table_walfish.add_column("Pérdidas [Lb]", justify="center")
    table_walfish.add_column("Potencia recibida [dBm]", justify="center")

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
            table_walfish.add_row(f"{i+1}", "Sí", str(Lb), str(Prx))
        else: 
            table_walfish.add_row(f"{i+1}", "No", str(Lb), str(Prx))
        
        wi_results.append({'distance': d, 'Prx': Prx})

    # Lognormal
    ln_results = model_lognormal(data['mobiles'], Pt_dBm, Gt_dB, Gr_dB, alpha, sigma)
    table_lognormal = generar_tabla_lognormal(ln_results)

    # Espacio libre
    mobiles = data['mobiles']
    resultados_free_space, table_free_space = model_free_space(mobiles, FREQ_MHZ, Pt_dBm, Gt_dB, Gr_dB)
    # Modelo reflejante
    h_m = data['mobile_height']
    resultados_modelo_reflejante, table_reflejante = model_two_ray(mobiles, h_bs, h_m, FREQ_MHZ, Pt_dBm, Gt_dB, Gr_dB)

    # Imprimiendo las tablas en consola
    print(table_walfish)
    print(table_lognormal)
    print(table_free_space)
    print(table_reflejante)
    # Graficar
    distances = [r['distance'] for r in wi_results]
    Pr_wi = [r['Prx'] for r in wi_results]
    Pr_ln = [r['Pr_log'] for r in ln_results]
    Pr_free_space = [r['Prx_fspl'] for r in resultados_free_space]
    Pr_reflejante = [r['Prx_two_ray'] for r in resultados_modelo_reflejante]

    plt.figure()
    plt.plot(distances, Pr_wi, 'o-', label='Walfish-Ikegami')  # sin especificar color
    plt.plot(distances, Pr_ln, 's--', label='Lognormal')
    plt.plot(distances, Pr_free_space, 's-', label='Espacio libre')
    plt.plot(distances, Pr_reflejante, 'o--', label='Modelo reflejante')
    plt.xlabel('Distancia (m)')
    plt.ylabel('Potencia recibida (dBm)')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()