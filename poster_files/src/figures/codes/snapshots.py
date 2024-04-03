import glob
import os
import sys

import matplotlib.transforms as mtransforms
import numpy as np
import PyThemes.quarto as quarto
import svgutils.transform as sg
from matplotlib import pyplot as plt

sys.path.append("/media/cyril/IMFTPostDoc/OFB_Colmatage/processing")
import parameters_general as gen_pars

path_manip = "/media/cyril/IMFTPostDoc/OFB_Colmatage/Data/25072023/release01/images/"
path_contour = "/media/cyril/IMFTPostDoc/OFB_Colmatage/processing/images/spatial_analysis/specific_contours/"

list_image = sorted(glob.glob(os.path.join(path_manip, "*.tif")))
image_ref = np.array([np.array(plt.imread(img)) for img in list_image[:30]]).mean(axis=0)

indexes = [385, 885, 1501, 2226, 2806, 3500]
dt = 1 / 10
xrefs = np.array([50, 308, 567, 826, 1084, 1343, 1602, 1860, 2119, 2378])
colors = plt.cm.viridis((xrefs - gen_pars.x_ref) / (xrefs.min() - xrefs.max()))
labels = [rf"$x_{{{xrefs.size - i}}}$" for i in range(xrefs.size)]

figsize = np.array([quarto.regular_fig_width, 0.4 * quarto.regular_fig_height])
fig, axarr = plt.subplots(3, 2, figsize=1.2 * figsize, layout="compressed")

for i, ax in zip(indexes, axarr.T.flatten()):
    img = np.array(plt.imread(list_image[i]))
    #
    ax.imshow(img, cmap="gray", vmin=2 * image_ref.min(), vmax=0.5e4)
    ax.axhline(y=89 if i > 400 else 93, color="k", lw=0.15)
    ax.set_xticks([])
    ax.set_yticks([])
    #
    trans = mtransforms.ScaledTranslation(3 / 72, 3 / 72, fig.dpi_scale_trans)
    ax.text(
        0.0,
        0,
        rf"$t = {(i - 200) * dt:.0f}$ s",
        transform=ax.transAxes + trans,
        fontsize=8,
        bbox=dict(facecolor="w", edgecolor="none", pad=0.5, alpha=0.35),
    )
    if i == 1501:
        LINES = np.load(os.path.join(path_contour, f"{i}.npy"), allow_pickle=True).item()
        ax.plot(LINES[0.75][0][:, 0], LINES[0.75][0][:, 1], color="tab:orange", lw=1)
        ax.text(1700, 300, r"$d(x, t)$", color="tab:orange", fontsize=10)
        ax.set_xticks(xrefs[1:], labels[1:], fontsize=10)
        #
        for c, label in zip(colors[1:], ax.get_xticklabels()):
            label.set_color(c)

fig.get_layout_engine().set(w_pad=0, h_pad=0, hspace=0.1, wspace=0.02)


ax.patch.set_alpha(0.2)
fig.patch.set_alpha(0)

figname = "../{}.svg".format(
    sys.argv[0].split(os.sep)[-1].replace(".py", ""),
)
fig.savefig(figname, dpi=1200, facecolor=fig.get_facecolor(), edgecolor="none")

fig = sg.fromfile(figname)
newsize = ["{}pt".format(quarto.scaling_factor * float(i.replace("pt", ""))) for i in fig.get_size()]

fig.set_size(newsize)
fig.save(figname)
