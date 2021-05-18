#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------------------
PYTHON SCRIPT TO COPY ALL PHOTOS FROM A FOLDER AND SUBFOLDERS
INTO A SINGLE FOLDER, FOR THEIR PREPROCESSING
------------------------------------------------------------------------------

Version: 1.0.1 (18/05/2021)
Author: Benoît SMETS
        (Royal Museum for Central Africa  /  Vrije Universiteit Brussel)

Citation:
    Smets, B., 2021
    Historical Aerial Photo Pre-Processing
    [Script_0_Copy2singleFolder_v101.py].
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
      
    - No specific Python module is required.
    
    - To use this script, simply adapt the directory paths and required values
      in the setup section of the script.


"""

import os
import shutil

################################    SETUP     ################################

source_folder = r'G://Lubefu-Fizi_Kasongo-selection'
dest_folder = r'G://0_RAW'
file_format = '.tif'

################################ END OF SETUP ################################

print(' ')
print('=====================================================================')
print('=         PYTHON SCRIPT TO COPY FILES INTO A SINGLE FOLDER          =')
print('=         Version 1.0.1 (May 2021)  |  B. Smets (RMCA/VUB)          =')
print('=====================================================================')
print(' ')

for root, dirs, files in os.walk(source_folder):
   for file in files:
       if file.endswith(file_format):           # select only files with given format
           path_file = os.path.join(root,file)  # concatenate all paths
           shutil.copy2(path_file, dest_folder) # send everything into dest_folder

#######################################

print(' ')
print('done!')