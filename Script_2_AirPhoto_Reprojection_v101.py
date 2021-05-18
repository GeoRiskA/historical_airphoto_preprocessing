#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------------------
PYTHON SCRIPT FOR AERIAL PHOTO ARCHIVE REPROJECTION INTO A STANDARD FORMAT
BEFORE PHOTOGRAMMETRIC PROCESSING USING AGISOFT METASHAPE PRO
------------------------------------------------------------------------------

Version: 1.0.1 (18/05/2021)
Authors: Benoît SMETS
        (Royal Museum for Central Africa  /  Vrije Universiteit Brussel)
        &
        Antoine DILLE for the beta version 0.1
        (Royal Museum for Central Africa)

Citation:
    Smets, B., 2021
    Historical Aerial Photo Pre-Processing
    [Script_2_AirPhoto_Reprojection_v101.py].
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
        > Numpy
        > OpenCV
        > Pandas
    
    - To use this script, simply adapt the directory paths and required values
      in the setup section of the script.

"""

import numpy as np
import os, pandas as pd
import glob
import cv2
from joblib import Parallel, delayed
import multiprocessing
from time import sleep

################################    SETUP     ################################

##### DIRECTORY PATHS ##### (for Windows paths, please use "//" between directories ; for Mac, simply use "/" between directories)

input_image_folder = r"I://2_SfM_READY_photo_collection//Burundi_1981-82//1_CanvasSized_FidMark//"

fiducialmarks_file = r"I://2_SfM_READY_photo_collection//Burundi_1981-82//Burundi_1981-82_FidMarks_CSV.csv"

output_image_folder = r"I://2_SfM_READY_photo_collection//Burundi_1981-82//2_ImageReady_1500dpi//"

##### NEW COORDINATES OF FIDUCIAL MARKS #####
    # (1 = upper left; 2 = upper right; 3 = lower right; 4 = lower left)
    # (If the fiducial marks are at the medians: 1 = up; 2 = right; 3 = down ; 4 = left)

pts2 = np.float32([[473,473],[12923,473],[12923,12923],[473,12923]])

##### DIMENSIONS OF THE OUTPUT IMAGE #####

dimX = 13395
dimY = 13395

##### SPECIFY THE FILE FORMAT OF YOUR INPUT IMAGE DATASET #####
    # (e.g., '*.tif', '*.jpg')

image_format = '*.tif'

#### PARALLEL PROCESSING #####
    # (Choose the number of CPU cores you want to use)
    # (minimum = 1; suggested value = (number of cores) - 1)
    # (if you don't know how many cores you have, write: 'multiprocessing.cpu_count()')

num_cores = multiprocessing.cpu_count() - 1

################################ END OF SETUP ################################

print(' ')
print('=====================================================================')
print('=         PYTHON SCRIPT FOR AIR PHOTO ARCHIVE PREPROCESSING         =')
print('=         Version 1.0.1 (May 2021)  |  B. Smets (RMCA/VUB)          =')
print('=====================================================================')
print(' ')

##### DEFINE ADDITIONAL USEFUL VARIABLES #####

images_list = glob.glob(input_image_folder + image_format)
FM = pd.read_csv(fiducialmarks_file,sep=',', header=[0])
number_images = str(len(FM))

##### DISPLAY THE NUMBER OF IMAGES TO PROCESS #####

print('Number of tasks (images to process): ' + number_images)
print(' ')

##### PROCESSING WORKFLOW #####

def reproject_and_crop(image):
        # Read the images, keep the original pixel depth (-1) and read its dimensions
        dst_filename = os.path.join(input_image_folder, os.path.splitext(os.path.basename(image))[0] + '.tif')
        img = cv2.imread(dst_filename, -1)
        rows, cols = img.shape
        
        # Extract the image name and find the corresponding row with fiducial marks coordinates, in the CSV file
        img_name=os.path.splitext(os.path.basename(image))[0]
        df=FM[FM['PHOTO_ID'].str.contains(img_name)]
        x=FM.loc[FM['PHOTO_ID']==img_name].index[0]
        pts1 = np.float32([[df['Xp1'][x],df['Yp1'][x]],[df['Xp2'][x],df['Yp2'][x]],[df['Xp3'][x],df['Yp3'][x]],[df['Xp4'][x],df['Yp4'][x]]])

        # Reproject the image by applying the new coordinates of the fiducial marks and crop it at the provided dimensions
        M = cv2.getPerspectiveTransform(pts1,pts2)
        imready = cv2.warpPerspective(img,M,(dimX,dimY))
        
        # Export the reprojected and cropped images
        cv2.imwrite(os.path.join(output_image_folder, img_name + '_standardized.tif'), imready)

##### PARALLEL PROCESSING #####

Parallel(n_jobs=num_cores, verbose=30)(delayed(reproject_and_crop)(image) for image in images_list)

##### END PROCESSING #####

sleep(3)

print(' ')
print('======================')
print(' PROCESSING COMPLETED ')
print('======================')
