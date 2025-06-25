import math
from rich.table import Table

# velocidad de la luz en m/s
c = 3e8

def pr_two_ray(d, h_bs, h_m, freq_mhz, Pt_dBm, Gt_dB, Gr_dB):
    """
    Modelo Two-Ray Ground Reflection.
    Calcula Pr en dBm usando la fórmula:
    Pr_lin = Pt_lin * Gt_lin * Gr_lin * (h_bs * h_m / (d**2 * lambda_))**2
    """
    # convertir a sistema lineal
    Pt_lin = 10**((Pt_dBm - 30) / 10)
    Gt_lin = 10**(Gt_dB / 10)
    Gr_lin = 10**(Gr_dB / 10)
    lam = c / (freq_mhz * 1e6)

    Pr_lin = Pt_lin * Gt_lin * Gr_lin * (h_bs * h_m / (d**2 * lam))**2
    return 10 * math.log10(Pr_lin) + 30


def model_two_ray(mobiles, h_bs, h_m, freq_mhz, Pt_dBm, Gt_dB, Gr_dB):
    """
    Aplica el modelo Two-Ray a cada móvil.
    Retorna lista de dicts y tabla Rich.
    """
    resultados = []
    table = Table(title="[bold cyan]Resultados Superficie reflejante[/bold cyan]")
    table.add_column("Punto", justify="center")
    table.add_column("Prx [dBm]", justify="center")

    for i, m in enumerate(mobiles):
        d = m['real_distance']
        Prx = pr_two_ray(d, h_bs, h_m, freq_mhz, Pt_dBm, Gt_dB, Gr_dB)
        resultados.append({'distance': d, 'Prx_two_ray': Prx})
        table.add_row(f"{i+1}", f"{Prx:.2f}")

    return resultados, table