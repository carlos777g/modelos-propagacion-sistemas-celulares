import numpy as np
import pandas as pd

# Parámetros generales
f = 1935e6  # Hz
c = 3e8  # m/s
lambda_ = c / f
Pt_dBm = 10 * np.log10(10) + 30
Gt = 9
Gr = 3
ht = 15
hr = 1.5
alpha = 2.8
sigma = 7

# Coordenadas estación base
bs = [19.503668573568277, -99.1279845883227]

# Coordenadas de los puntos
puntos = np.array([
    [19.5037883, -99.1278115],
    [19.5039467, -99.1277085],
    [19.5040868, -99.1276048],
    [19.5042387, -99.1274952],
    [19.5053859, -99.1266844],
    [19.5054628, -99.1266317],
    [19.5055397, -99.1265725],
    [19.5056925, -99.1264652],
    [19.5058470, -99.1263597],
    [19.5059915, -99.1262430],
    [19.5061310, -99.1261597],
    [19.5062961, -99.1260430],
    [19.5064486, -99.1259352],
    [19.5065955, -99.1258314],
    [19.5067395, -99.1257257],
    [19.5068977, -99.1256146],
    [19.5070766, -99.1254859],
    [19.5079421, -99.1248616],
    [19.5081005, -99.1247527],
    [19.5084762, -99.1244849],
    [19.5086251, -99.1243824],
    [19.5089531, -99.1241445]
])

# Distancias desde estación base (m)
dist_m = np.array([
    22.06, 42.66, 61.41, 81.95, 234.79, 244.85, 255.5, 275.8, 295.8, 316.24,
    334.04, 356.1, 376.1, 395.89, 415.33, 436.61, 460.46, 576.31, 597.36,
    647.56, 667.22, 709.94
])
dist_km = dist_m / 1000
n = len(dist_km)

# Parámetros COST231
b = 30
w = 20
h = 15
phi = 45

# Función de pérdida por orientación
def orientation_loss(phi):
    if phi < 35:
        return -10
    elif phi <= 55:
        return -5
    else:
        return 0

# Inicialización de vectores
Pr_EL = np.zeros(n)
Pr_SR = np.zeros(n)
Pr_COST = np.zeros(n)
Pr_Log = np.zeros(n)
Ld_log = np.zeros(n)
Xsigma = np.zeros(n)
Llog = np.zeros(n)

# Cálculos
np.random.seed(1)
for i in range(n):
    d_km = dist_km[i]
    d_m = dist_m[i]

    # Espacio libre
    Lfs = 32.44 + 20 * np.log10(d_km) + 20 * np.log10(f / 1e6)
    Pr_EL[i] = Pt_dBm + Gt + Gr - Lfs

    # Superficie reflejante
1    LSR = 40 * np.log10(d_m) - 20 * np.log10(ht * hr)
    Pr_SR[i] = Pt_dBm + Gt + Gr - LSR

    # COST231
    L0 = 32.4 + 20 * np.log10(d_km) + 20 * np.log10(f / 1e6)
    Lori = orientation_loss(phi)
    Lrts = -16.9 - 10 * np.log10(w) + 10 * np.log10(f / 1e6) + 20 * np.log10(ht - hr) + Lori
    Lbsh = -18 * np.log10(1 + ht - h)
    ka = 54
    kd = 18
    kf = -4 + 0.7 * ((f / 1e6) / 925 - 1)
    Lmsd = Lbsh + ka + kd * np.log10(d_km) + kf * np.log10(f / 1e6) - 9 * np.log10(b)
    Lcost = L0 + Lrts + Lmsd
    Pr_COST[i] = Pt_dBm + Gt + Gr - Lcost

    # Lognormal
    Ld_log[i] = 10 * alpha * np.log10(d_km)
    Xsigma[i] = np.random.randn() * sigma
    Llog[i] = Ld_log[i] + Xsigma[i]
    Pr_Log[i] = Pt_dBm + Gt + Gr - Llog[i]

# Tabla de resultados
T = pd.DataFrame({
    'Punto': np.arange(1, n + 1),
    'Distancia_m': dist_m,
    'Distancia_km': dist_km,
    'Pr_EspacioLibre': Pr_EL,
    'Pr_SuperficieReflejante': Pr_SR,
    'Pr_COST231': Pr_COST,
    'Pr_Lognormal': Pr_Log
})

print(T)

import matplotlib.pyplot as plt

# Crear figura
plt.figure(figsize=(12, 6))

# Graficar cada modelo de potencia recibida vs distancia
plt.plot(dist_m, Pr_EL, label='Espacio Libre', marker='o')
plt.plot(dist_m, Pr_SR, label='Superficie Reflejante', marker='s')
plt.plot(dist_m, Pr_COST, label='COST231', marker='^')
plt.plot(dist_m, Pr_Log, label='Lognormal', marker='d')

# Configuración del gráfico
plt.title('Potencia Recibida según Modelo de Propagación')
plt.xlabel('Distancia desde BS (m)')
plt.ylabel('Potencia Recibida (dBm)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
