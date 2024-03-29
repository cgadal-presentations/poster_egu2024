import os
import sys

import numpy as np
import PyThemes.quarto as quarto
import svgutils.transform as sg
from matplotlib import pyplot as plt
from uncertainties import correlated_values
from uncertainties import unumpy as unp


def law_wall(z, u_star, z0, Kappa=0.4):
    return (u_star / Kappa) * unp.log(z / z0)


sys.path.append("/media/cyril/IMFTPostDoc/OFB_Colmatage/processing/UDV")

path_data = "/media/cyril/IMFTPostDoc/OFB_Colmatage/processing/UDV/release01"

data = np.load(os.path.join(path_data, "data.npy"), allow_pickle=True).item()

z_interp = data["z_interp"] * 1e-2  # [m]
u, v = data["U_av"]  # [m/s]

probe = 13
z, phi = data[probe]["z"] * 1e-2, data[probe]["phi_inferred"][1]  # [m], [-]

C0 = "C0"
C1 = "C1"

## fit law of the wall
Kappa = 0.4  # Von karma constant
nu = 9.9e-7  # water viscosity for T = 12deg in [m2/s]

mask = (z_interp * 1e2 - 0.73 > 0.75) & (z_interp * 1e2 - 0.73 <= 4.5)  # value in cm
p, pcov = np.polyfit(np.log(z_interp[mask] - 0.73 * 1e-2), -u[mask], 1, cov=True)
ubeta = correlated_values(p, pcov)


u_star = Kappa * ubeta[0]
z0 = unp.exp(-ubeta[-1] / ubeta[0])[()]
zth = np.logspace(-2, 1, 300) * 1e-2  # [m]
theory = law_wall(zth, u_star, z0)
m, s = unp.nominal_values(theory), unp.std_devs(theory)


figsize = np.array([quarto.regular_fig_width, 0.75*quarto.regular_fig_width])
fig, ax = plt.subplots(1, 1, layout="constrained", figsize=figsize/1.25)


ax.plot(-u * 1e2, z_interp * 1e2 - 0.73, color=C0)
ax.set_xlabel(r"Velocity [cm/s]", color=C0)
ax.tick_params(axis="x", labelcolor=C0)
ax.set_xlim(3, 5.5)
ax.set(ylabel=r"Height [cm]", ylim=(0, 6))

ax0_bis = ax.twiny()
ax0_bis.plot(phi, z * 1e2 - 0.73, color=C1, ls="--")
ax0_bis.set_xlabel(r"$\phi~[\%]$", color=C1)
ax0_bis.set_xlim(0, 0.2)
ax0_bis.tick_params(axis="x", labelcolor=C1)

# %% saving figure
figname = "../{}.svg".format(sys.argv[0].split(os.sep)[-1].replace(".py", ""))
fig.savefig(figname, dpi=1200)

fig = sg.fromfile(figname)
newsize = ["{}pt".format(quarto.scaling_factor * float(i.replace("pt", ""))) for i in fig.get_size()]

fig.set_size(newsize)
fig.save(figname)
