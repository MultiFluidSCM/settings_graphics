import os
import sys
import time
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def make_gif_from_list(images, filename="animation.gif", folder="", duration=1000, loop=0):
    print("Generating gif with {} images".format(len(images)))
    print(images[0])
    image_start = Image.open(images[0])
        
    
    images_append = []
    for i in range(1,len(images)):
        image = Image.open(images[i])
        
        images_append.append(image)
    
    filename = os.path.join(folder, filename)
    if not filename.endswith(".gif"):
        filename += ".gif"
    
    if os.path.isfile(filename):
        os.remove(filename)
    
    if not os.path.isdir(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    
    print("Saving {}".format(filename))
    image_start.save(
        filename, 
        save_all = True, 
        append_images = images_append, 
        duration = duration, 
        loop = loop
    )
    
