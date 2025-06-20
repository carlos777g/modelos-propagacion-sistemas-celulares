import numpy as np

def model_lognormal(mobiles, Pt_dBm, Gt_dB, Gr_dB, alpha, sigma):
    """
    Calcula pérdidas y potencia recibida según el modelo lognormal.
    """
    dist_m = np.array([m["real_distance"] for m in mobiles])
    dist_km = dist_m / 1000
    n = len(dist_m)

    Ld_log = 10 * alpha * np.log10(dist_km)
    Xsigma = np.random.randn(n) * sigma
    Pr = Pt_dBm + Gt_dB + Gr_dB - Ld_log - Xsigma

    # Devolver lista de dicts
    return [
        {
            "distance": dist_m[i],
            "loss_d": Ld_log[i],
            "shadowing": Xsigma[i],
            "Pr_log": Pr[i]
        }
        for i in range(n)
    ]

from rich.table import Table

def generar_tabla_lognormal(resultados):
    table = Table(title="[bold magenta]Resultados Modelo Lognormal[/bold magenta]")

    table.add_column("Puntos", justify="center")
    table.add_column("Distancia (m)", justify="center")
    table.add_column("Pérdida [dB]", justify="center")
    table.add_column("Ensombrecimiento [dB]", justify="center")
    table.add_column("Potencia recibida [dBm]", justify="center")

    for index, r in enumerate(resultados):
        table.add_row(
            f"{index+1}",
            f"{r['distance']:.2f}",
            f"{r['loss_d']:.2f}",
            f"{r['shadowing']:.2f}",
            f"{r['Pr_log']:.2f}"
        )

    return table

# table = Table(title="[bold magenta]Resultados Modelo lognormal[bold magenta]")
# table.add_column("Distancia", justify="center")
# table.add_column("Pérdida [dB]", justify="center")
# table.add_column("Ensombrecimiento [dB]", justify="center")
# table.add_column("Potencia recibida [dBm]", justify="center")