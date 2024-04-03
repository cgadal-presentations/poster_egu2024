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
ws = 0.053  # [cm/s]

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
t_plot = np.logspace(1.3, 2.6, 100)
colors = plt.cm.viridis((xrefs - gen_pars.x_ref) / (xrefs.min() - xrefs.max()))
labels = [rf"$x_{{{xrefs.size - i}}}$" for i in range(xrefs.size)]

figsize = np.array([quarto.regular_fig_width, 0.75 * quarto.regular_fig_width])
fig, axmain = plt.subplots(1, 1, layout="constrained", figsize=figsize / 1.25)
ax_inset = axmain.inset_axes([0.1, 0.1, 0.4, 0.4])

for ax in [ax_inset, axmain]:
    lines = []
    for timing, color, label in zip(timings[:, xrefs[1:]].T[::-1], colors[1:][::-1], labels[1:][::-1]):
        lines.append(ax.plot(timing, y, color=color, label=label)[0])

    (l1,) = ax.plot(t_plot, b_m * t_plot**a_m, label=rf"$d = {b_m:.2f} t^{{{a_m:.1f}}}$", color="tab:orange")
    (l2,) = ax.plot(t_plot, ws * t_plot, color="tab:orange", ls="--", label=r"$d = w_{\rm s} t$")

leg1 = axmain.legend(handles=lines, ncols=3, title="positions", loc="upper right", fontsize=10)
leg2 = axmain.legend(handles=[l1, l2], loc="lower right", fontsize=10, bbox_to_anchor=[1, 0.53])
axmain.add_artist(leg1)

ax_inset.set_ylim(1, 26)
ax_inset.set_xlim(20, 275)
ax_inset.set_xscale("log")
ax_inset.set_yscale("log")
# ax_inset.set_xlabel("$t$ [s]", labelpad=0, loc="left")
# ax_inset.set_ylabel("$d$ [cm]", labelpad=0)
axmain.text(76, 25.25, "$t$ [s]")
axmain.text(28, 17.85, "$d$ [cm]", rotation=90)


axmain.set_ylim(0, 26)
axmain.set_xlim(20, 275)
axmain.set_xlabel("Time, $t$ [s]")
axmain.set_ylabel("Front depth, $d$ [cm]")

for ax in [ax_inset, axmain]:
    ax.invert_yaxis()

figname = "../{}.svg".format(sys.argv[0].split(os.sep)[-1].replace(".py", ""))
fig.savefig(figname, dpi=400)

fig = sg.fromfile(figname)
newsize = ["{}pt".format(quarto.scaling_factor * float(i.replace("pt", ""))) for i in fig.get_size()]

fig.set_size(newsize)
fig.save(figname)
