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
        shapes = False,
        dpi = 300
    ):
    '''
    Plot the cloud base and top, as well as the regions in which the different transfer processes
    are assumed to operate in.
    '''
    
    if greyscale:
        shapes = True
    
    t = data_les["times"][0]/3600.
    z = data_les["z"][:,0]/1000.
    cloud_base = np.array(data_les["cloud_base"])/1000.
    cloud_top  = np.array(data_les["cloud_top"]) /1000.
    bl_top     = np.array(data_les["bl_top"])/1000.
    
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6,2.5))
    
    
    
    filter_sigma = 0.5
    
    # Plot contours of transfer regions
    if greyscale:
        kwargs = dict(levels=[0.9, 1.1], alpha=0.9, linewidths=0.3)
        plt.rcParams['hatch.color'] = "grey"
        ax.contourf(t, z, gaussian_filter(1.01*data_les["filter_dwdz"], filter_sigma),         **kwargs, colors="#888888")
        ax.contourf(t, z, gaussian_filter(1.01*data_les["filter_instability"], filter_sigma),  **kwargs, colors="#333333")
        ax.contourf(t, z, gaussian_filter(1.01*data_les["filter_mixing"], filter_sigma),       **kwargs, cmap="seismic", hatches=["OO"])
        ax.contourf(t, z, gaussian_filter(1.01*data_les["filter_mixing_cloud"], filter_sigma), **kwargs, cmap="seismic", hatches=["O.O."])
        ax.contour (t, z, gaussian_filter(1.01*data_les["filter_dwdz"], filter_sigma),         **kwargs, colors="#888888")
        ax.contour (t, z, gaussian_filter(1.01*data_les["filter_instability"], filter_sigma),  **kwargs, colors="#333333")
        ax.contour (t, z, gaussian_filter(1.01*data_les["filter_mixing"], filter_sigma),       **kwargs, colors="grey")
        ax.contour (t, z, gaussian_filter(1.01*data_les["filter_mixing_cloud"], filter_sigma), **kwargs, colors="grey")
    elif shapes:
        kwargs = dict(levels=[0.9, 1.1], alpha=0.9, linewidths=0.5)
        
        ax.contourf(t, z, gaussian_filter(1.01*data_les["filter_dwdz"], filter_sigma),         **kwargs, cmap="Greens")
        plt.rcParams['hatch.color'] = "red"
        ax.contourf(t, z, gaussian_filter(1.01*data_les["filter_instability"], filter_sigma),  **kwargs, cmap="Reds", hatches=["/"])
        plt.rcParams['hatch.color'] = "magenta"
        ax.contourf(t, z, gaussian_filter(1.01*data_les["filter_mixing"], filter_sigma),       **kwargs, cmap="Purples", hatches=["O"])
        plt.rcParams['hatch.color'] = "blue"
        ax.contourf(t, z, gaussian_filter(1.01*data_les["filter_mixing_cloud"], filter_sigma), **kwargs, cmap="Blues", hatches=["O."])
        ax.contour (t, z, gaussian_filter(1.01*data_les["filter_dwdz"], filter_sigma),         **kwargs, colors="green")
        ax.contour (t, z, gaussian_filter(1.01*data_les["filter_instability"], filter_sigma),  **kwargs, colors="red")
        ax.contour (t, z, gaussian_filter(1.01*data_les["filter_mixing"], filter_sigma),       **kwargs, colors="magenta")
        ax.contour (t, z, gaussian_filter(1.01*data_les["filter_mixing_cloud"], filter_sigma), **kwargs, colors="blue")
    else:
        kwargs = dict(levels=[0.9, 1.1], alpha=0.9, linewidths=1)
        ax.contourf(t, z, gaussian_filter(1.01*data_les["filter_dwdz"], filter_sigma),         **kwargs, cmap="Greens")
        ax.contourf(t, z, gaussian_filter(1.01*data_les["filter_instability"], filter_sigma),  **kwargs, cmap="Reds")
        ax.contourf(t, z, gaussian_filter(1.01*data_les["filter_mixing"], filter_sigma),       **kwargs, cmap="Purples")
        ax.contourf(t, z, gaussian_filter(1.01*data_les["filter_mixing_cloud"], filter_sigma), **kwargs, cmap="Blues")
        ax.contour (t, z, gaussian_filter(1.01*data_les["filter_dwdz"], filter_sigma),         **kwargs, colors="green")
        ax.contour (t, z, gaussian_filter(1.01*data_les["filter_instability"], filter_sigma),  **kwargs, colors="red")
        ax.contour (t, z, gaussian_filter(1.01*data_les["filter_mixing"], filter_sigma),       **kwargs, colors="magenta")
        ax.contour (t, z, gaussian_filter(1.01*data_les["filter_mixing_cloud"], filter_sigma), **kwargs, colors="blue")
    
    # Plot outlines of cloud base and top
    ax.plot(t, cloud_base, color="black")
    ax.plot(t, cloud_top,  color="black")
    ax.plot(t, bl_top, color="white")
    ax.plot(t, bl_top, ":", color="black")
    
    # Add custom elements for the legend
    if greyscale:
        legend_elements = [
           Line2D([0], [0], color="k", label='Cloud base/top'),
           Line2D([0], [0], color="k", label='BL top', linestyle=":"),
           Patch(facecolor="#888888", edgecolor="#888888", label='BL/CL top detrainment'),
           Patch(facecolor="white", edgecolor="grey", hatch="O.O.", label='Mid-cloud mixing'),
           Patch(facecolor="white", edgecolor="grey", hatch="OO",  label='Mid-BL mixing'),
           Patch(facecolor="#333333", edgecolor="#333333", label='Surface entrainment'),
        ]
    elif shapes:
        legend_elements = [
           Line2D([0], [0], color="k", label='Cloud base/top'),
           Line2D([0], [0], color="k", label='BL top', linestyle=":"),
           Patch(facecolor=(0.5, 0.8, 0.5, 0.8), edgecolor="green", label='BL/CL top detrainment'),
           Patch(facecolor=(0.5, 0.8,   1, 0.8), edgecolor="blue", hatch="O.O.", label='Mid-cloud mixing'),
           Patch(facecolor=(0.9, 0.4, 0.8, 0.8), edgecolor="magenta", hatch="OO",  label='Mid-BL mixing'),
           Patch(facecolor=(  1, 0.3, 0.3, 0.8), edgecolor="red", hatch="//", label='Surface entrainment'),
        ]
    else:
        legend_elements = [
           Line2D([0], [0], color="k", label='Cloud base/top'),
           Line2D([0], [0], color="k", label='BL top', linestyle=":"),
           Patch(facecolor=(0.5, 0.8, 0.5, 0.8), edgecolor="green",   label='BL/CL top detrainment'),
           Patch(facecolor=(0.5, 0.8,   1, 0.8), edgecolor="blue",    label='Mid-cloud mixing'),
           Patch(facecolor=(0.9, 0.4, 0.8, 0.8), edgecolor="magenta", label='Mid-BL mixing'),
           Patch(facecolor=(  1, 0.3, 0.3, 0.8), edgecolor="red",     label='Surface entrainment'),
        ]
    
    ax.set_xticks(np.arange(0.5, 14.5, 0.5), minor=True)
    ax.set_yticks([0,1,2,3,4])
    ax.set_yticks([0.5, 1.5, 2.5, 3.5], minor=True)
    ax.set_xlim(left=0)
    ax.set_ylim(0, 4)
    ax.set_xlabel("t (hours)")
    ax.set_ylabel("z (km)")
    ax.legend(handles=legend_elements, loc="upper left", prop={'size': 8})
    
    filename = f"transfer_regions_{id}"
    if greyscale:
        filename += "_greyscale"
    if shapes:
        filename += "_shapes"
    fig.savefig(
        os.path.join(folder, f"{filename}.png"),
        bbox_inches = "tight",
        dpi = dpi
    )
    fig.savefig(
        os.path.join(folder, f"{filename}.pdf"),
        bbox_inches = "tight"
    )
    plt.close()