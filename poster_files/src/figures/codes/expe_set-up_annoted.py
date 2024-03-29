import glob
import os
import sys

import numpy as np
import PyThemes.quarto as quarto
import svgutils.transform as sg
from matplotlib import pyplot as plt

path_manip = "/media/cyril/IMFTPostDoc/OFB_Colmatage/Data/25072023/release01/images/"

list_image = sorted(glob.glob(os.path.join(path_manip, "*.tif")))
image_ref = np.array([np.array(plt.imread(img)) for img in list_image[:10]]).mean(axis=0)

# %%
figsize = (1.2 * quarto.regular_fig_width, 0.7 * quarto.regular_fig_height)
fig, ax = plt.subplots(1, 1, figsize=figsize)
ax.set_clip_on(False)
pad = 0.01
plt.subplots_adjust(left=pad, right=1 - pad, top=1 - pad, bottom=0.2)

img = np.array(plt.imread(list_image[0]))
ax.imshow(img, cmap="gray", vmin=image_ref.min(), vmax=1.5e4)

ax.set_xticks([])
ax.set_yticks([])

color_sed = "peru"
color_matrix = "yellowgreen"
coor_injection = "skyblue"
color_flow = "tab:blue"

## UDV probes
rect_probe1 = plt.Rectangle(
    xy=(0.6, 0.695),
    width=0.1,
    height=0.14,
    transform=fig.transFigure,
    edgecolor=color_sed,
    facecolor="none",
    clip_on=False,
    zorder=2,
)
ax.add_patch(rect_probe1)

rect_probe2 = plt.Rectangle(
    xy=(0.215, 0.695),
    width=0.06,
    height=0.14,
    transform=fig.transFigure,
    edgecolor=color_sed,
    facecolor="none",
    clip_on=False,
    zorder=2,
)
ax.add_patch(rect_probe2)

ax.text(
    0.435,
    1 - pad,
    "Ultrasound measurements\n" + r"$\phi(z)$, $\vec{u}(z)$",
    ha="center",
    transform=fig.transFigure,
    va="top",
)

xytext = (0.33, 0.925)
ax.annotate(
    "",
    xy=(0.275, 0.835),
    xytext=xytext,
    xycoords=fig.transFigure,
    annotation_clip=False,
    ha="center",
    va="top",
    arrowprops=dict(arrowstyle="->", color=color_sed),
)
xytext = (0.54, 0.925)
ax.annotate(
    "",
    xy=(0.6, 0.835),
    xytext=xytext,
    xycoords=fig.transFigure,
    annotation_clip=False,
    ha="center",
    va="center",
    arrowprops=dict(arrowstyle="->", color=color_sed),
)

## injection
rect_probe1 = plt.Rectangle(
    xy=(0.92, 0.3625),
    width=0.075,
    height=0.465,
    transform=fig.transFigure,
    edgecolor=coor_injection,
    facecolor="none",
    clip_on=False,
)
ax.add_patch(rect_probe1)

xytext = (0.9, 1 - pad)
ax.annotate(
    "Injection set-up\n overflow/spillway",
    xy=(0.96, 0.8275),
    xytext=xytext,
    xycoords=fig.transFigure,
    annotation_clip=False,
    ha="center",
    va="top",
    arrowprops=dict(arrowstyle="->", color=coor_injection),
)

# flow arrows
ax.annotate(
    "",
    xy=(2549, 192),
    xytext=(2549, 356),
    arrowprops=dict(arrowstyle="<-", color=color_flow, shrinkA=0, shrinkB=0),
    annotation_clip=True,
)

ax.annotate(
    "",
    xy=(2398, 135),
    xytext=(2501, 356),
    arrowprops=dict(
        arrowstyle="->", color=color_flow, shrinkA=0, shrinkB=0, connectionstyle="angle, angleA=90,angleB=180"
    ),
    annotation_clip=True,
)

ax.annotate(
    "",
    xy=(1000, 135),
    xytext=(1150, 135),
    arrowprops=dict(arrowstyle="->", color="tab:blue", shrinkA=0, shrinkB=0),
    annotation_clip=True,
)

# %% hydrogel matrix

path_img = "/media/cyril/IMFTPostDoc/OFB_Colmatage/presentations/quick_dirty_pres/talk_files/static/photos_Cyril_manip/PXL_20230725_110311627.jpg"
img = np.array(plt.imread(path_img))

axins = ax.inset_axes([0.08, pad, 0.5, 0.355], xticks=[], yticks=[], transform=fig.transFigure)
rect, lines = ax.indicate_inset(
    bounds=[1300, 140, 300, 295],
    inset_ax=axins,
    edgecolor=color_matrix,
    clip_on=False,
    transform=ax.transData,
    alpha=1,
)
lines[1].set_visible(True)
lines[3].set_visible(False)

for spine in ["top", "bottom", "left", "right"]:
    axins.spines[spine].set_color(color_matrix)

axins.imshow(img)

ax.text(pad, 0.1, "Porous matrix:\n- hygrogel beads\n- optically transparent", ma="left", transform=fig.transFigure)

# %% plate

xytext = (0.762, 0.2)
ax.annotate(
    "Removable porous grid:\nenable/disable hydrogel bead transport",
    xy=(1960, 176),
    xytext=xytext,
    xycoords=ax.transData,
    textcoords=fig.transFigure,
    annotation_clip=False,
    ha="center",
    va="bottom",
    arrowprops=dict(arrowstyle="->", color="k", shrinkB=0),
)

# %% saving figure
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
