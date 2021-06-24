import os
import sys
import numpy as np
import matplotlib.pyplot as plt

from ..utilities.stitch_images import stitch_transfer_row, stitch_all

def plot_all_transfer_graphics(
        settings_scm,
        data_les_b,
        folder = "",
        title = "",
        greyscale = False,
        dpi = 200
    ):
    '''
    Create multiple graphics for the model settings vs the diagnosed values for various plot ranges.
    '''
    scales = ["default", "wide", "wide_negative", "automatic"]
    # scales = ["automatic"]
    
    for scale in scales:
        print(f"\nCreating graphics for scale: {scale}")
        plot_transfer_graphics(
            settings_scm,
            data_les_b,
            folder = folder,
            title = title,
            scale = scale,
            greyscale = greyscale,
            dpi = dpi
        )
    
def plot_transfer_graphics(
        settings_scm,
        data_les_b,
        folder = "",
        title = "",
        scale = "default",
        greyscale = False,
        dpi = 200
    ):
    '''
    Create multiple graphics for the model settings vs the diagnosed values.
    '''
    if greyscale:
        folder_scale = os.path.join(folder, f"{scale}_greyscale")
    else:
        folder_scale = os.path.join(folder, f"{scale}")
    if not os.path.isdir(folder_scale):
        os.makedirs(folder_scale)
    
    for transfer in settings_scm:
        
        for setting in settings_scm[transfer]:
            id = "{}_{}".format(transfer, settings_scm[transfer][setting]["id"])
            
            plot_transfer_graphic(
                id,
                settings_scm[transfer][setting]["symbol"],
                settings_scm[transfer][setting]["value"], 
                get_corresponding_les_data(transfer, settings_scm[transfer][setting]["id"], data_les_b),
                folder = folder_scale,
                scale = scale,
                greyscale = greyscale,
                color = settings_scm[transfer][setting]["color"],
                dpi = dpi
            )
        
        stitch_transfer_row(folder_scale, transfer, orientation="horizontal", title=settings_scm[transfer][setting]["name"])
        stitch_transfer_row(folder_scale, transfer, orientation="vertical",   title=settings_scm[transfer][setting]["name"])
    
    stitch_all(folder_scale, title=title.replace("_"," ").capitalize())

def plot_transfer_graphic(
        id,
        variable,
        data_scm, 
        data_les,
        folder = "",
        scale = "default",
        greyscale = False,
        color = (1,0,0),
        dpi = 200
    ):
    '''
    Create a graphical representation of the transfer parameters used by the model (SCM)
    and show how this compared with high-resolution data (LES).
    '''
        
    if greyscale:
        color = (0,0,0)
    
    fig_width = 500
    fig_height = 100
    
    fig = plt.figure(figsize=(fig_width/dpi, fig_height/dpi))
    ax = fig.add_subplot(1, 1, 1)
    
    limits = set_limits(ax, scale, data_scm)
    
    # plot_les_range(ax, data_les, limits, color, id)
    plot_les_density(ax, data_les, limits, color, id)
    
    if data_scm >= limits["x_lim"][0] and data_scm <= limits["x_lim"][1]:
        ax.plot([data_scm, data_scm], limits["y_lim"], color="k", linewidth=5., alpha=1., clip_on=False)
    
    ax.set_title(f"{variable} = {data_scm:.2f}")
    
    center_axis(ax)
    turn_off_axis(ax, axis="y")
    
    plt.savefig(
        os.path.join(folder, f"setting_{id}.png"),
        bbox_inches = "tight",
        dpi = dpi
    )
    plt.close()

def set_limits(ax, scale, data_scm):
    '''
    From the user settings, setup the axis limits, labels and formating.
    '''
    limits = {}
    
    # x axis
    if scale == "default":
        x_left = 0
        x_right = 1
        limits["x_ticks"] = np.array([0., 0.5, 1.])
        limits["x_tick_labels"] = ["0","0.5","1"]
        limits["x_ticks_minor"] = [0.25, 0.75]
    elif scale == "wide":
        x_left = 0
        x_right = 2
        limits["x_ticks"] = np.array([0., 1., 2.])
        limits["x_tick_labels"] = ["0","1","2"]
        limits["x_ticks_minor"] = [0.5, 1.5]
    elif scale == "wide_negative":
        x_left = -1
        x_right = 2
        limits["x_ticks"] = np.array([-1., 0., 1., 2.])
        limits["x_tick_labels"] = ["-1","0","1","2"]
        limits["x_ticks_minor"] = [-0.5, 0.5, 1.5]
    else:
        if data_scm < 0.:
            return set_limits(ax, "wide_negative", data_scm)
        elif data_scm > 1.:
            return set_limits(ax, "wide", data_scm)
        else:
            return set_limits(ax, "default", data_scm)
    
    limits["x_lim"] = np.array([x_left, x_right])
    
    # Set axis limits
    ax.set_xlim(limits["x_lim"])
    
    # Set ticks and tick labels
    ax.tick_params(axis='x', which='major', size= 30)
    ax.tick_params(axis='x', which='minor', size= 10)
    ax.set_xticks(limits["x_ticks"])
    ax.set_xticks(limits["x_ticks_minor"], minor = True)
    ax.set_xticklabels(limits["x_tick_labels"])
    
    # y axis
    y_top = 1
    y_center = 0
    y_bottom = -1
    
    limits["y_lim"] = np.array([y_bottom,y_top])
    limits["y_top"] = np.array([y_top,y_top])
    limits["y_center"] = np.array([y_center,y_center])
    limits["y_bottom"] = np.array([y_bottom,y_bottom])
    
    ax.set_ylim(limits["y_lim"])
    
    return limits

def center_axis(ax):
    '''
    By default, Matplotlib shows the axis bar at the edges of the plot.
    This function places the axis at the center of the plot, just like drawing an axis on paper:
                y
                ^
                |
                |
    ------------|-----------> x
                |
    '''
    # Move left y-axis and bottim x-axis to centre, passing through (0,0)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')

    # Eliminate upper and right axes
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # Show ticks in the left and lower axes only
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    
    # Show ticks on the left and lower axes only (and let them protrude in both directions)
    ax.xaxis.set_tick_params(which="both", bottom='on', top=False, direction='inout')
    ax.yaxis.set_tick_params(which="both", left='on', right=False, direction='inout')

def turn_off_axis(ax, axis="y"):
    '''
    Completely remove lines and labels from an axis
    '''
    if axis == "x":
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_color('none')
        
        # RRemove ticks, tick labels and axis labels
        ax.xaxis.set_tick_params(bottom=False, top=False, labelleft=False)
    elif axis == "y":
        # Remove spines
        ax.spines['left'].set_color('none')
        ax.spines['right'].set_color('none')
        
        # Remove ticks, tick labels and axis labels
        ax.yaxis.set_tick_params(left=False, right=False, labelbottom=False)

def get_corresponding_les_data(transfer, id, data_les):
    '''
    Using the ID for the SCM setting, get the relevant data from the LES
    '''
    
    key = ""
    if "entrain" in id:
        key = "b21"
    elif "detrain" in id:
        key = "b12"
    
    variable = ""
    if id[-1] == "w":
        variable = "w"
    elif id[-1] == "t":
        variable = "theta"
    elif id[-1] == "u":
        variable = "u"
    elif id[-1] == "q":
        variable = "qv"
    
    data = {}
    if "plumeEdge" in data_les[transfer]:
        if variable in data_les[transfer]["plumeEdge"]:
            data["plumeEdge"] = data_les[transfer]["plumeEdge"][variable][key]
    if "particles" in data_les[transfer]:
        if variable in data_les[transfer]["particles"]:
            data["particles"] = data_les[transfer]["particles"][variable][key]
    
    return data


def plot_les_range(ax, data_les, limits, color):
    les_range = np.array([np.min(data_les), np.max(data_les)])
    les_min = np.max(data_les)
    
    ax.fill_between(les_range, limits["y_center"], limits["y_top"],    linewidth=1., facecolor=(color[0],color[1],color[2],0.), edgecolor=(color[0],color[1],color[2],0.8))
    ax.fill_between(les_range, limits["y_center"], limits["y_bottom"], linewidth=1., facecolor=(color[0],color[1],color[2],0.), edgecolor=(color[0],color[1],color[2],0.8))


def plot_les_density(ax, data_les, limits, color, id):
    
    if "plumeEdge" in data_les:
        if "particles" in data_les:
            plot_density(ax, data_les["plumeEdge"], 0.5*limits["y_bottom"], limits["y_center"], color)
        else:
            plot_density(ax, data_les["plumeEdge"], 0.5*limits["y_bottom"], 0.5*limits["y_top"], color)
        
        if "bentraint" in id and "mixing_b" in id:
            x = limits["x_lim"][0] + 0.02*(limits["x_lim"][1]-limits["x_lim"][0])
            y = -0.25
            ax.text(x, y, "Plume edge", ha="left", va="center", fontsize=5, weight="bold")
    if "particles" in data_les:
        plot_density(ax, data_les["particles"], limits["y_center"], 0.5*limits["y_top"], color)
        
        if "bentraint" in id and "mixing_b" in id:
            x = limits["x_lim"][0] + 0.02*(limits["x_lim"][1]-limits["x_lim"][0])
            y = 0.25
            ax.text(x, y, "Particles", ha="left", va="center", fontsize=5, weight="bold")
    

def plot_density(ax, data_les, bottom, top, color):
    bins = np.linspace(-1, 2, 61)
    digitized = np.digitize(data_les, bins)
    # bin_means = np.array([data_les[digitized == i].mean() for i in range(1, len(bins))])
    bin_sizes = np.array([len(data_les[digitized == i])   for i in range(1, len(bins))])
    bin_sizes_norm = np.clip(5*bin_sizes/len(data_les), 0., 1.)
    
    for i in range(len(bins)-1):
        alpha = 0.8*bin_sizes_norm[i]
        ax.fill_between(np.array([bins[i],bins[i+1]]), bottom, top, facecolor=(color[0],color[1],color[2],alpha), edgecolor=(color[0],color[1],color[2],0.))
    