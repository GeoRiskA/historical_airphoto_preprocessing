#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------------------
PYTHON SCRIPT FOR THE STANDARDIZING OF AERIAL PHOTO ARCHIVE CANVAS SIZE
------------------------------------------------------------------------------

Version: 1.0.1 (18/05/2021)
Author: Benoît SMETS
        (Royal Museum for Central Africa  /  Vrije Universiteit Brussel)

Citation:
    Smets, B., 2021
    Historical Aerial Photo Pre-Processing
    [Script_1_AirPhoto_CanvasSizing_v101.py].
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
        > Joblib
        > OpenCV
        > Pillow
    
    - To use this script, simply adapt the directory paths and required values
      in the setup section of the script.


"""

import os
import glob
from PIL import Image
import numpy as np
import cv2
from joblib import Parallel, delayed
import multiprocessing
from time import sleep

################################    SETUP     ################################

##### DIRECTORY PATHS #####
input_image_folder = r"G:\Lubefu-Fizi_Kasongo-selection\0_RAW"
output_image_folder = r"G:\Lubefu-Fizi_Kasongo-selection\1_CanvasSized"

##### SPECIFY THE FILE FORMAT OF YOUR INPUT IMAGE DATASET #####
    # (e.g., '*.tif', '*.jpg', '*.png')
image_format = '*.tif'

#### PARALLEL PROCESSING #####
    # (Choose the number of CPU cores you want to use)
    # (minimum = 1; suggested value = (number of cores) - 1)
    # (if you don't know how many cores you have, write: 'multiprocessing.cpu_count()')
num_cores = multiprocessing.cpu_count() - 1

################################ END OF SETUP ################################

print(' ')
print('=====================================================================')
print('=           PYTHON SCRIPT FOR IMAGE CANVAS STANDARDIZING            =')
print('=         Version 1.0.1 (May 2021)  |  B. Smets (RMCA/VUB)          =')
print('=====================================================================')
print(' ')

### Define the list of images and count the number of files to process ###
images_list = glob.glob(input_image_folder + image_format)
print('Number of images to process: ' + str(len(images_list)))
print(' ')

### Detect the max width and height in the dataset ###
sizes = [Image.open(f, 'r').size for f in images_list]
sizes_array = np.asarray(sizes)
widths = sizes_array[:, 0]
heights = sizes_array[:, 1]
width_max = max(widths)
height_max = max(heights)

print('maximum width found = ' + str(width_max) + ' pixels')
print('maximum height found = ' + str(height_max) + ' pixels')
print(' ')

### Standardize the the canvas size of each image ###
def standardize_canvas(image):
        # Read the images, keep the original pixel depth (-1) and read its dimensions
        file = os.path.join(input_image_folder, os.path.splitext(os.path.basename(image))[0] + '.tif')
        img = cv2.imread(file, -1)
        rows, cols = img.shape
        # Add columns and rows to change the canvas size to maximum width and height
        rows_added = height_max - rows
        cols_added = width_max - cols
        imready = cv2.copyMakeBorder(img, top=0, bottom=rows_added, left=0, right=cols_added, borderType=cv2.BORDER_CONSTANT, value=0)
        # Save the new image with the standardized size of canvas
        img_name=os.path.splitext(os.path.basename(image))[0]   # Find the name of the input image, without its file extension, in order to use it into the output image name 
        cv2.imwrite(os.path.join(output_image_folder, img_name + '_CanvasSized.tif'), imready)

##### PARALLEL PROCESSING #####

Parallel(n_jobs=num_cores, verbose=30)(delayed(standardize_canvas)(image) for image in images_list)

##### END PROCESSING #####

sleep(3)
print(' ')
print('======================')
print(' PROCESSING COMPLETED ')
print('======================')