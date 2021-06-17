import os
import sys
import numpy as np
import matplotlib.pyplot as plt

def plot_graphic(
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
    
    if greyscale:
        color = (0,0,0)
    
    fig_width = 500
    fig_height = 100
    
    fig = plt.figure(figsize=(fig_width/dpi, fig_height/dpi))
    ax = fig.add_subplot(1, 1, 1)
    
    limits = set_limits(ax, scale)
    
    ax.plot([data_scm, data_scm], limits["y_lim"], color="k", linewidth=5., alpha=1.)
    ax.fill_between(data_les, limits["y_center"], limits["y_top"],    linewidth=2., facecolor=(color[0],color[1],color[2],0.5), edgecolor=(color[0],color[1],color[2],0.8))
    ax.fill_between(data_les-0.2, limits["y_center"], limits["y_bottom"], linewidth=2., facecolor=(color[0],color[1],color[2],0.5), edgecolor=(color[0],color[1],color[2],0.8))
    
    ax.set_title(f"{variable} = {data_scm:.2f}")
    
    center_axis(ax)
    turn_off_axis(ax, axis="y")
    
    plt.savefig(
        os.path.join(folder, f"setting_{id}.png"),
        bbox_inches = "tight",
        dpi = dpi
    )
    plt.close()

def set_limits(ax, scale):
    limits = {}
    
    # x axis
    if scale == "wide":
        x_left = 0
        x_right = 2
        limits["x_ticks"] = np.array([0., 1., 2.])
        limits["x_tick_labels"] = ["0","1","2"]
        limits["x_ticks_minor"] = [0.5, 1.5]
    elif scale == "wide negative":
        x_left = -1
        x_right = 2
        limits["x_ticks"] = np.array([-1., 0., 1., 2.])
        limits["x_tick_labels"] = ["-1","0","1","2"]
        limits["x_ticks_minor"] = [-0.5, 0.5, 1.5]
    else:
        x_left = 0
        x_right = 1
        limits["x_ticks"] = np.array([0., 0.5, 1.])
        limits["x_tick_labels"] = ["0","0.5","1"]
        limits["x_ticks_minor"] = [0.25, 0.75]
    
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