import glob
import os
import sys

import numpy as np
import PyThemes.quarto as quarto
import svgutils.transform as sg
from matplotlib import pyplot as plt
from skimage import exposure

path_manip = "/media/cyril/IMFTPostDoc/OFB_Colmatage/Data/25072023/release01/images/"

list_image = sorted(glob.glob(os.path.join(path_manip, "*.tif")))
image_ref = np.array([np.array(plt.imread(img)) for img in list_image[:10]]).mean(axis=0)


indexes = [385, 885, 1501, 2226, 2806, 3500]

figsize = (quarto.regular_fig_width, 0.3 * quarto.regular_fig_height)
fig, axarr = plt.subplots(2, 3, figsize=figsize, layout='compressed')

for  i, ax in zip(indexes, axarr.flatten()):
    img = np.array(plt.imread(list_image[i]))
    #
    ax.imshow(img, cmap="gray", vmin=2*image_ref.min(), vmax=0.5e4)
    ax.set_xticks([])
    ax.set_yticks([])

fig.get_layout_engine().set(w_pad=0, h_pad=0, hspace=0.06, wspace=0.025)


ax.patch.set_alpha(0.2)
fig.patch.set_alpha(0)

figname = "../{}.svg".format(
    sys.argv[0].split(os.sep)[-1].replace(".py", ""),
)
fig.savefig(figname, dpi=1200, facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches='tight')

fig = sg.fromfile(figname)
newsize = ["{}pt".format(quarto.scaling_factor * float(i.replace("pt", ""))) for i in fig.get_size()]

fig.set_size(newsize)
fig.save(figname)