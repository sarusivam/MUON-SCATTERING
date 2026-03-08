import numpy as np
import matplotlib.pyplot as plt

materials = {
    "Iron":     {"X0": 1.76,    "density": 7.87,   "Z": 26.0},
    "Copper":   {"X0": 1.43,    "density": 8.96,   "Z": 29.0},
    "Lead":     {"X0": 0.56,    "density": 11.35,  "Z": 82.0},
}



def calculate_muon_scattering(theta, material_info=materials["Lead"], p=4000, v=1.0,L=1.0):
    X0 = material_info['X0']
    ratio = L / X0
    sigma = (13.6 / (v * p)) * np.sqrt(ratio) * (1 + 0.038 * np.log(ratio))
    prob_density = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-theta**2 / (2 * sigma**2))
    
    return prob_density
# for material, info in materials.items():
#     x = np.linspace(-0.015, 0.015, 500)
#     y = calculate_muon_scattering(x, info)
#     plt.plot(x, y, lw=2, label=material)
# plt.title("Muon Scattering Angle Distribution")
# plt.xlabel("Scattering Angle (radians)")
# plt.ylabel("Density")
# plt.legend()
# plt.show()