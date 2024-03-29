import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import PyThemes.quarto as quarto
import svgutils.transform as sg
from lmfit import Model

sys.path.append("/media/cyril/IMFTPostDoc/OFB_Colmatage/processing")
import parameters_general as gen_pars


def lin_func(x, a, b):
    return a * x + b


# %%% load data
path_data = "/media/cyril/IMFTPostDoc/OFB_Colmatage/processing/images/front_propagation"
data = np.load(os.path.join(path_data, "data.npy"), allow_pickle=True).item()


# %% fit front
def affine(x, a, b):
    return a * x + b


def fitfunc(log_t):
    mask = log_t < np.log(1e2)
    weights = np.ones_like(log_z)
    weights[mask] = 0
    return gmodel_aff.fit(log_z, params, x=log_t, nan_policy="omit", weights=weights)


y, timings = data["front_infiltration"]["z"], data["front_infiltration"]["t"]
xrefs = data["xrefs"]
x = data["x"]

gmodel_aff = Model(affine)
params = gmodel_aff.make_params(a=2, b=1.2)

log_t = np.log(timings)
log_z = np.log(y)
log_t[np.abs(log_t) == np.inf] = np.nan
mask_enough_points = (np.isfinite(log_t * log_z[:, None])).sum(axis=0) > 10

fitresults = np.apply_along_axis(fitfunc, 0, log_t[:, mask_enough_points])
a, b = np.array([[fitresult.params["a"], fitresult.params["b"]] for fitresult in fitresults]).T

a_m, a_std = np.nanmean(a), np.nanstd(a)
b_m, b_std = np.exp(np.nanmean(b)), np.exp(np.nanstd(b))

# %%
t_plot = np.logspace(1.3, 2.4, 100)
colors = plt.cm.viridis((xrefs - gen_pars.x_ref) / (xrefs.min() - xrefs.max()))

figsize = np.array([quarto.regular_fig_width, 0.75*quarto.regular_fig_width])
fig, ax = plt.subplots(1, 1, layout="constrained", figsize=figsize/1.25)

for timing, color, xref in zip(timings[:, xrefs].T, colors, xrefs):
    ax.plot(
        timing,
        y,
        color=color,
        # label='{:.0f}'.format(x[xref])
    )

ax.plot(t_plot, b_m * t_plot**a_m, label=rf"$d = {b_m:.2f} t^{{{a_m:.1f}}}$", color="tab:orange")

ax.legend()
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Time [s]")
ax.set_xlim(left=9)
ax.set_ylabel("Front position [cm]")
ax.invert_yaxis()

figname = "../{}.svg".format(sys.argv[0].split(os.sep)[-1].replace(".py", ""))
fig.savefig(figname, dpi=400)

fig = sg.fromfile(figname)
newsize = ["{}pt".format(quarto.scaling_factor * float(i.replace("pt", ""))) for i in fig.get_size()]

fig.set_size(newsize)
fig.save(figname)
