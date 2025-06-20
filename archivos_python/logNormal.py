import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

# Cargar datos desde JSON
with open("datos.json", 'r') as f:
    data = json.load(f)

# Extraer distancias desde datos.json
dist_m = np.array([movil["real_distance"] for movil in data["mobiles"]])
dist_km = dist_m / 1000
n = len(dist_m)

f = 1935e6  # Hz
Pt_dBm = 10 * np.log10(10) + 30  # Potencia de transmisión en dBm
Gt = 9  # Ganancia transmisor (dB)
Gr = 3  # Ganancia receptor (dB)
alpha = 2.8  # Exponente de pérdida
sigma = 7    # Desviación estándar en dB (lognormal)

# Inicialización de variables
Ld_log = np.zeros(n) #Pérdida por distancia
Xsigma = np.zeros(n) #Pérdida por ensombrecimiento
Pr_Log = np.zeros(n) #Potencia recibida

for i in range(n):
    d_km = dist_km[i]
    Ld_log[i] = 10 * alpha * np.log10(d_km)
    Xsigma[i] = np.random.randn() * sigma
    Pr_Log[i] = Pt_dBm + Gt + Gr - Ld_log[i] - Xsigma[i]

# Crear DataFrame con resultados
df_log = pd.DataFrame({
    'Punto': np.arange(1, n + 1),
    'Distancia_m': dist_m,
    'Pérdida_Distancia_dB': Ld_log,
    'Ensombrecimiento_dB': Xsigma,
    'Potencia_Lognormal_dBm': Pr_Log
})

# Mostrar tabla
print(df_log)

#Grafica
plt.figure(figsize=(10, 6))
plt.plot(dist_m, Pr_Log, 'o-', color='blue', label='Modelo Lognormal')
plt.title("Potencia Recibida - Modelo Lognormal")
plt.xlabel("Distancia desde la estación base (m)")
plt.ylabel("Potencia Recibida (dBm)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
