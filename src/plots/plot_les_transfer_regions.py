import os
import sys
import scipy.ndimage
from scipy.ndimage.filters import gaussian_filter
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
    bl_top     = np.array(data_les["bl_top"])/1000.
    
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6,2.5))
    
    # Plot outlines of cloud base and top
    ax.plot(t, cloud_base, color="black")
    ax.plot(t, cloud_top,  color="black")
    ax.plot(t, bl_top, color="white")
    ax.plot(t, bl_top, "--", color="black")
    
    filter_sigma = 0.5
    
    # Plot contours of transfer regions
    kwargs = dict(levels=[0.9, 1.1], alpha=0.9, linewidths=1)
    ax.contourf(t, z, gaussian_filter(1.01*data_les["filter_dwdz"], filter_sigma),         **kwargs, cmap="Greens")
    ax.contourf(t, z, gaussian_filter(1.01*data_les["filter_instability"], filter_sigma),  **kwargs, cmap="Reds")
    ax.contourf(t, z, gaussian_filter(1.01*data_les["filter_mixing"], filter_sigma),       **kwargs, cmap="Purples")
    ax.contourf(t, z, gaussian_filter(1.01*data_les["filter_mixing_cloud"], filter_sigma), **kwargs, cmap="Blues")
    ax.contour (t, z, gaussian_filter(1.01*data_les["filter_dwdz"], filter_sigma),         **kwargs, colors="green")
    ax.contour (t, z, gaussian_filter(1.01*data_les["filter_instability"], filter_sigma),  **kwargs, colors="red")
    ax.contour (t, z, gaussian_filter(1.01*data_les["filter_mixing"], filter_sigma),       **kwargs, colors="magenta")
    ax.contour (t, z, gaussian_filter(1.01*data_les["filter_mixing_cloud"], filter_sigma), **kwargs, colors="blue")
    
    # Add custom elements for the legend
    legend_elements = [
       Line2D([0], [0], color="k", label='Cloud Base/Top'),
       Patch(facecolor=(0.7, 0.4, 0.7, 0.8), label='Mixing BL'),
       Patch(facecolor=(0.5, 0.8,   1, 0.8), label='Mixing Cloud'),
       Patch(facecolor=(  1, 0.5, 0.5, 0.8), label='Instability'),
       Patch(facecolor=(0.5, 0.8, 0.5, 0.8), label='dw/dz')
    ]
    legend_elements = [
       Line2D([0], [0], color="k", label='Cloud base/top'),
       Line2D([0], [0], color="k", label='BL top', linestyle="--"),
       Patch(facecolor=(0.5, 0.8, 0.5, 0.8), edgecolor="green",   label='BL/CL top detrainment'),
       Patch(facecolor=(0.5, 0.8,   1, 0.8), edgecolor="blue",    label='Mid-cloud mixing'),
       Patch(facecolor=(0.9, 0.4, 0.8, 0.8), edgecolor="magenta", label='Mid-BL mixing'),
       Patch(facecolor=(  1, 0.3, 0.3, 0.8), edgecolor="red",     label='Surface entrainment'),
    ]
    
    ax.set_yticks([0,1,2,3,4])
    ax.set_ylim(0, 4)
    ax.set_xlabel("t (hours)")
    ax.set_ylabel("z (km)")
    ax.legend(handles=legend_elements, loc="upper left", prop={'size': 7})
    
    fig.savefig(
        os.path.join(folder, f"transfer_regions_{id}.png"),
        bbox_inches = "tight",
        dpi = dpi
    )
    plt.close()