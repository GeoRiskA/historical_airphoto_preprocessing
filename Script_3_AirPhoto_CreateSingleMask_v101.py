#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------------------
PYTHON SCRIPT TO CREATE ONE MASK ASSOCIATED WITH
A SERIES OF IDENTICAL AERIAL PHOTOGRAPHS
------------------------------------------------------------------------------

Version: 1.0.1 (18/05/2021)
Authors: Benoît SMETS
        (Royal Museum for Central Africa  /  Vrije Universiteit Brussel)

Citation:
    Smets, B., 2021
    Historical Aerial Photo Pre-Processing
    [Script_3_AirPhoto_CreateSingleMask_v101.py].
    Version 1.0
    https://github.com/GeoRiskA/historical_airphoto_preprocessing
    DOI: N/A
    
Associated article (to be cited too):
    Smets, B., Dewitte, O., Michellier, C., Muganga, G., Dille, A., Kervyn, F.,
    SUBMITTED
    Insights into the SfM photogrammetric processing of historical
    panchromatic aerial photographs without camera calibration
    information.
    ISPRS International Journal of Geo-Information.
    DOI: N/A

Notes:
    
    - For the required Python libraries, we recommend the use of Anaconda
      or Miniconda.
      
    - Specific Python modules needed for this script:
        > Glob
        > Numpy
        > Pillow
    
    - To use this script, simply adapt the directory paths and required values
      in the setup section of the script.

"""

import glob
from PIL import Image
from PIL import ImageDraw
import numpy as np
from time import sleep

################################    SETUP     ################################

##### DIRECTORY PATHS #####
input_image_folder = r"/Users/benoitsmets/GoogleDrive/PHOTOGRAMMETRY/Test_CanvasSizing/"
output_mask_folder = r"/Users/benoitsmets/GoogleDrive/PHOTOGRAMMETRY/Test_CanvasSizing/"

##### SPECIFY THE FILE FORMAT OF YOUR INPUT IMAGE DATASET #####
    # (e.g., '*.tif', '*.jpg', '*.png')
image_format = '*.tif'

##### SIZE OF CORNER MASKS #####
    # This script will mask the corners of images, using rectangles
    # The size of these rectangles is a percentage of the image width and height
percent_mask_size_X = 12 #percent
percent_mask_size_Y = 12 #percent

#### NAME OF DATASET #####
    # Provide the name you want to give to the single mask
dataset_name = 'TestSingleMask'

################################ END OF SETUP ################################

print(' ')
print('=====================================================================')
print('=            PYTHON SCRIPT TO CREATE A SINGLE IMAGE MASK            =')
print('=         Version 1.0.1 (May 2021)  |  B. Smets (RMCA/VUB)          =')
print('=====================================================================')
print(' ')

### Define the list of images and count the number of files to process ###
images_list = glob.glob(input_image_folder + image_format)
print('Number of images in dataset: ' + str(len(images_list)))
print(' ')

### Detect the max width and height in the dataset ###
Image.MAX_IMAGE_PIXELS = None
sizes = [Image.open(f, 'r').size for f in images_list]
sizes_array = np.asarray(sizes)
widths = sizes_array[:, 0]
heights = sizes_array[:, 1]
width_max = max(widths)
height_max = max(heights)
width_min = min(widths)
height_min = min(heights)

print('Width found = ' + str(width_max) + ' pixels')
print('Height found = ' + str(height_max) + ' pixels')
print(' ')
print('Double check --> minimum width = ' + str(width_min) + ' pixels (must be similar)')
print('Double check --> minimum height = ' + str(height_min) + ' pixels (must be similar)')
print(' ')

### Define the size of corner masks (by default = 12% of the size)
dimX = width_max
dimY = height_max
marginX = round((percent_mask_size_X/100)*dimX)
marginY = round((percent_mask_size_Y/100)*dimY)

### create the single mask ###
ROI1_x0 = 0
ROI1_x1 = marginX
ROI1_y0 = 0
ROI1_y1 = marginY
ROI2_x0 = dimX-marginX
ROI2_x1 = dimX
ROI2_y0 = 0
ROI2_y1 = marginY
ROI3_x0 = dimX-marginX
ROI3_x1 = dimX
ROI3_y0 = dimY-marginY
ROI3_y1 = dimY
ROI4_x0 = 0
ROI4_x1 = marginX
ROI4_y0 = dimY-marginY
ROI4_y1 = dimY

mask = Image.new('L', size=[dimX, dimY], color=255)
draw = ImageDraw.Draw(mask)
draw.rectangle([(ROI1_x0, ROI1_y0), (ROI1_x1, ROI1_y1)],fill=0)
draw.rectangle([(ROI2_x0, ROI2_y0), (ROI2_x1, ROI2_y1)],fill=0)
draw.rectangle([(ROI3_x0, ROI3_y0), (ROI3_x1, ROI3_y1)],fill=0)
draw.rectangle([(ROI4_x0, ROI4_y0), (ROI4_x1, ROI4_y1)],fill=0)
mask.save(output_mask_folder + dataset_name + '_mask.png')

##### END PROCESSING #####

sleep(1)
print(' ')
print('======================')
print(' PROCESSING COMPLETED ')
print('======================')