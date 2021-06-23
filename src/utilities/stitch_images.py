import os
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from .check_folder import get_files_in_folder

def stitch_images(files, file_output, orientation="horizontal", padding=0, color=(255,255,255)):
    '''
    Merge two images into one, displayed side by side
    :param files: list of paths to image files
    :return: the merged Image object
    '''
    n = len(files)
    images = []
    widths = []
    heights = []
    for file in files:
        image = Image.open(file)
        (width, height) = image.size
        
        images.append(image)
        widths.append(width)
        heights.append(height)
    
    widths = np.array(widths, dtype=int)
    heights = np.array(heights, dtype=int)
    
    if orientation == "horizontal":
        result_width = np.sum(widths) + (n+1)*padding
        result_height = np.max(heights) + 2*padding

        result = Image.new('RGB', (result_width, result_height), color=color)
        for i in range(n):
            result.paste(im=images[i], box=(np.sum(widths[:i]) + (i+1)*padding, padding))
    else:
        result_width = np.max(widths) + 2*padding
        result_height = np.sum(heights) + (n+1)*padding

        result = Image.new('RGB', (result_width, result_height), color=color)
        for i in range(n):
            result.paste(im=images[i], box=(padding, np.sum(heights[:i]) + (i+1)*padding))
    
    result.save(file_output)

def add_title(file, title, file_output="", font_size=50, font_color=(0,0,0), background_color=(255,255,255)):
    '''
    Add a title text to the top of an image
    '''
    filename_font = "/mnt/c/Windows/Fonts/Arial.ttf"
    
    if os.path.isfile(filename_font):
        image = Image.open(file)

        (width, height) = image.size
        
        # Create a new image with extra space at the top for the title text
        result_width = width
        result_height = height + 2*font_size

        result = Image.new('RGB', (result_width, result_height), color=background_color)
        result.paste(im=image, box=(0, 2*font_size))
        
        # Prepare image to draw text
        draw = ImageDraw.Draw(result)
        
        # Define font style and size
        font = ImageFont.truetype(filename_font, font_size)
        
        # Calculate size of text before drawing so text can be centered
        text_width, text_height = draw.textsize(title, font=font)
        
        # Draw the text
        # The stroke arguments make the title bold
        draw.text(((result_width-text_width)/2, font_size/2), title, font_color, font=font, stroke_width=1, stroke_fill=font_color)
        
        if file_output == "":
            file_output = file
        result.save(file_output)

def stitch_transfer_row(folder, transfer, orientation="horizontal", title=""):
    '''
    Stitch multiple transfer graphics together
    '''
    images = get_files_in_folder(folder, extension=".png")
    
    file_bentrainw = os.path.join(folder, f"setting_{transfer}_bentrainw.png")
    if file_bentrainw in images:
        files = [
            os.path.join(folder, f"setting_{transfer}_bentrainw.png"),
            os.path.join(folder, f"setting_{transfer}_bentraint.png"),
            os.path.join(folder, f"setting_{transfer}_bentrainq.png")
        ]
        
        file_output = os.path.join(folder, f"settings_{orientation}_{transfer}_bentrain.png")
        stitch_images(files, file_output, orientation=orientation, padding=20)
        
        if title != "":
            add_title(file_output, title.replace("detrain","entrain"), font_size=40)
    
    file_bdetrainw = os.path.join(folder, f"setting_{transfer}_bdetrainw.png")
    if file_bdetrainw in images:
        files = [
            os.path.join(folder, f"setting_{transfer}_bdetrainw.png"),
            os.path.join(folder, f"setting_{transfer}_bdetraint.png"),
            os.path.join(folder, f"setting_{transfer}_bdetrainq.png")
        ]
        file_output = os.path.join(folder, f"settings_{orientation}_{transfer}_bdetrain.png")
        stitch_images(files, file_output, orientation=orientation, padding=20)
        
        if title != "":
            add_title(file_output, title.replace("entrain","detrain"), font_size=40)
    

def stitch_all(folder, title=""):
    image_list = [
        "settings_horizontal_mixing_bentrain.png",
        "settings_horizontal_mixing_bdetrain.png",
        "settings_horizontal_mixing_cloud_bentrain.png",
        "settings_horizontal_mixing_cloud_bdetrain.png",
        "settings_horizontal_instability_bentrain.png",
        "settings_horizontal_dwdz_bdetrain.png"
    ]
    
    files = []
    for image in image_list:
        file = os.path.join(folder, image)
        
        if os.path.isfile(file):
            files.append(file)
    
    if len(files) > 1:
        file_output = os.path.join(folder, f"settings_horizontal.png")
        stitch_images(files, file_output, orientation="vertical", padding=0)
        
        if title != "":
            file_title = os.path.join(folder, f"settings_horizontal_title.png")
            add_title(file_output, title, file_output=file_title, font_size=70)
    
    
    image_list = [
        "settings_vertical_mixing_bentrain.png",
        "settings_vertical_mixing_bdetrain.png",
        "settings_vertical_mixing_cloud_bentrain.png",
        "settings_vertical_mixing_cloud_bdetrain.png",
        "settings_vertical_instability_bentrain.png",
        "settings_vertical_dwdz_bdetrain.png"
    ]
    
    files = []
    for image in image_list:
        file = os.path.join(folder, image)
        
        if os.path.isfile(file):
            files.append(file)
    
    if len(files) > 1:
        file_output = os.path.join(folder, f"settings_vertical.png")
        stitch_images(files, file_output, orientation="horizontal", padding=0)
        
        if title != "":
            file_title = os.path.join(folder, f"settings_vertical_title.png")
            add_title(file_output, title, file_output=file_title, font_size=70)