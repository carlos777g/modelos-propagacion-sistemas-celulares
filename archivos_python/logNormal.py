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