import os
import sys
import numpy as np
import matplotlib.pyplot as plt

def plot_graphic(
        id,
        data_scm, 
        data_les,
        folder = "",
        dpi = 200
    ):
    
    fig_width = 500
    fig_height = 100
    
    plt.figure(figsize=(fig_width/dpi, fig_height/dpi))
    
    plt.plot(data_scm, data_scm)
    
    plt.title(id)
    
    plt.savefig(
        os.path.join(folder, f"setting_{id}.png"),
        dpi = dpi
    )
    plt.close()