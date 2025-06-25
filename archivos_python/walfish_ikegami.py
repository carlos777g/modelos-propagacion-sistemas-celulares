import math

def loss_los(d, f):
    return 42.6 + 26 * math.log10(d) + 20 * math.log10(f)

import math


def lori(phi: float) -> float:
    """
    Pérdida por orientación de calle (L_ori) según COST-231 Walfish-Ikegami.
    phi: ángulo entre dirección de propagación y orientación de la calle (0°–90°)
    """
    if phi < 0 or phi > 90:
        raise ValueError("phi debe estar entre 0 y 90 grados")
    if phi < 35:
        return -10 + 0.354 * phi
    elif phi < 55:
        return 2.5 + 0.075 * (phi - 35)
    else:
        return 4.0 - 0.114 * (phi - 55)


def loss_nlos(d: float, f: float, h_bs: float, h_m: float, h_prom: float, phi: float, w: float, b: float) -> float:
    """
    Calcula las pérdidas Lb (dB) en condiciones NLoS según COST-231 Walfish-Ikegami.

    Parámetros:
    - d       : distancia real BS→móvil (m)
    - f       : frecuencia (MHz)
    - h_bs    : altura de la estación base (m)
    - h_m     : altura del móvil (m)
    - h_prom  : altura promedio de edificios (m)
    - phi     : ángulo de orientación de calle (°)
    - w       : ancho de la calle (m)
    - b       : separación promedio entre edificios (m)

    Retorna:
    - Lb: pérdidas totales (dB)
    """
    # 1. Pérdida de espacio libre (L_o)
    L_o = 32.44 + 20 * math.log10(f) + 20 * math.log10(d)

    # 2. Pérdida por tejados y orientación (L_rts)
    #    w: ancho de calle
    if w <= 0:
        raise ValueError("Ancho de calle w debe ser > 0")
    delta_h = h_bs - h_prom
    term_hw = 20 * math.log10(delta_h if delta_h > 0 else 0.1)
    L_rts = (
        -16.9
        - 10 * math.log10(w)
        + 10 * math.log10(f)
        + term_hw
        + lori(phi)
    )

    # 3. Pérdida por múltiples pantallas (L_msd)
    # 3.1: L_bsh
    if h_bs > h_prom:
        L_bsh = -18 * math.log10(1 + (h_bs - h_prom))
    else:
        L_bsh = 0

    # 3.2: k_a
    if h_bs > h_prom:
        k_a = 54
    else:
        diff = h_bs - h_prom
        if d >= 500:
            k_a = 54 - 0.8 * diff
        else:
            k_a = 54 - 0.8 * diff * (d / 0.5)

    # 3.3: k_d
    if h_bs > h_prom:
        k_d = 18
    else:
        k_d = 18 - 15 * ((h_bs - h_prom) / h_prom)

    # 3.4: k_f
    k_f = -4 + 1.5 * ((f / 925) - 1)

    # 3.5: L_msd
    if b <= 0:
        raise ValueError("Separación entre edificios b debe ser > 0")
    L_msd = (
        L_bsh
        + k_a
        + k_d * math.log10(d)
        + k_f * math.log10(f)
        - 9 * math.log10(b)
    )

    # 4. Cálculo final Lb
    if (L_rts + L_msd) > 0:
        return L_o + L_rts + L_msd, L_rts, L_msd
    else:
        return L_o
