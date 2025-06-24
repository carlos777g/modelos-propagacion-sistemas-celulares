import math
from rich.table import Table

def loss_free_space(d, freq_mhz):
    """
    Free-Space Path Loss (FSPL) en dB:
    FSPL = 32.44 + 20·log10(d_km) + 20·log10(freq_mhz)
    """
    d_km = d / 1000.0
    return 32.44 + 20 * math.log10(d_km) + 20 * math.log10(freq_mhz)


def model_free_space(mobiles, freq_mhz, Pt_dBm, Gt_dB, Gr_dB):
    """
    Calcula pérdidas FSPL y potencia recibida para cada móvil.
    Retorna lista de dicts y tabla Rich.
    """
    resultados = []
    table = Table(title="[bold cyan]Resultados Modelo Espacio Libre[/bold cyan]")
    table.add_column("Punto", justify="center")
    table.add_column("Pérdida FSPL [dB]", justify="center")
    table.add_column("Prx FSPL [dBm]", justify="center")

    for i, m in enumerate(mobiles):
        d = m['real_distance']
        Lfs = loss_free_space(d, freq_mhz)
        Prx = Pt_dBm + Gt_dB + Gr_dB - Lfs
        resultados.append({'distance': d, 'loss_fspl': Lfs, 'Prx_fspl': Prx})
        table.add_row(f"{i+1}", f"{Lfs:.2f}", f"{Prx:.2f}")

    return resultados, table
