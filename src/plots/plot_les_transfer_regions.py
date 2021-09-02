import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

def plot_les_transfer_regions(
        data_les,
        folder = "",
        id = "",
        greyscale = False,
        dpi = 200
    ):
    '''
    Plot the cloud base and top, as well as the regions in which the different transfer processes
    are assumed to operate in.
    '''
    
    t = data_les["times"][0]/3600.
    z = data_les["z"][:,0]/1000.
    cloud_base = np.array(data_les["cloud_base"])/1000.
    cloud_top  = np.array(data_les["cloud_top"]) /1000.
    
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,5))
    
    # Plot outlines of cloud base and top
    ax.plot(t, cloud_base, "k")
    ax.plot(t, cloud_top,  "k")
    
    # Plot contours of transfer regions
    kwargs = dict(levels=[0.9, 1.1], alpha=0.8)
    ax.contourf(t, z, data_les["filter_dwdz"],         **kwargs, cmap="Greens")
    ax.contourf(t, z, data_les["filter_instability"],  **kwargs, cmap="Reds")
    ax.contourf(t, z, data_les["filter_mixing"],       **kwargs, cmap="Purples")
    ax.contourf(t, z, data_les["filter_mixing_cloud"], **kwargs, cmap="Blues")
    
    # Add custom elements for the legend
    legend_elements = [
       Line2D([0], [0], color="k", label='Cloud Base/Top'),
       Patch(facecolor=(0.7, 0.4, 0.7, 0.8), label='Mixing BL'),
       Patch(facecolor=(0.5, 0.8,   1, 0.8), label='Mixing Cloud'),
       Patch(facecolor=(  1, 0.5, 0.5, 0.8), label='Instability'),
       Patch(facecolor=(0.5, 0.8, 0.5, 0.8), label='dw/dz')
    ]
    
    ax.set_ylim(0, 4)
    ax.set_xlabel("time (hours)")
    ax.set_ylabel("z (km)")
    ax.legend(handles=legend_elements, loc="upper left")
    
    fig.savefig(
        os.path.join(folder, f"transfer_regions_{id}.png"),
        bbox_inches = "tight",
        dpi = dpi
    )
    plt.close()