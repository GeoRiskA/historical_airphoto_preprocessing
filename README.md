# Historical Aerial Photo Pre-Processing  
*Last modified: 18th May 2021*  

The present repository contains a series of scripts that are useful to prepare datasets of scanned aerial photographs before their photogrammetric processing. The goal here is to go from raw scanned photographs to sets of images that have **1)** identical pixel dimensions in width and height, and **2)** the center of perspective relocated at the center of the image, based on the fiducial marks (i.e., "interior" or "intrinsic" orientation).  
  
All these scripts were developed in the frame of the **PAStECA Project** (BELSPO, BRAIN-be Programme, Contract n° BR/165/A3/PASTECA, http://pasteca.africamuseum.be/). They were written in Python 3, on MacOS, but were also tested on Windows 10 Pro and Ubuntu 20.04.
  
Each script can be run as it, by simply adapting the necessary parameters in the "setup" section of the script. All these scripts have the same 4-part structure:  
  
*1) A header providing a description of the script, the name of the authors, the required Python modules, the reference to cite if used, etc.*  
*2) A section with the Python modules to install (in addition to the recommended Anaconda/Miniconda Package distribution)*  
*3) The SETUP section with the variables and parameters that must be adapted by the user (only part that must be modified before use)*  
*4) The required coding to perform the task (should not be modified, except for specific user needs)*  
  
To get the required Python working environment, the followed philosophy was to install the Anaconda/Miniconda Distribution for Python 3, create a virtual environment dedicated to the processing of aerial photographs (using "conda create --name myenv python=3) and add the required modules using the "conda install" or "pip install" functions. The required Python modules that are needed for each script are mentioned in the header of the script.  
  
Each script has been optimized for speed by parallelizing the job using the Multiprocessing module.  
  
The scripts have also been adapted to display information about the ongoing processing in the Python console or terminal.  
  
The Python scripts are under a *GPL-3.0 license*. They are attached to a specific DOI () and the following peer-reviewed article (not published yet):  
**Authors:** *Smets, B., Dewitte, O., Michellier, C., Muganga, G., Dille, A., Kervyn, F.*  
**Title:** *Insights into the SfM photogrammetric processing of historical panchromatic aerial photographs without camera calibration information*  
**Journal:** *International Journal of Geo-Information (submitted)*  
  
If you use these scripts or an adapted version of them, please, cite the references of the repository and article in your work. Thank you in advance! (The publication status of the article will be adapted asap) 

All the scripts provided here are created by an Earth Scientist with self-learned programming skills. They can definitely be improved by a professional programmer. So, if you have constructive comments or recommendations that could help me to improve or speed up these scripts, please do not hesitate to contact me! I thank you in advance.  
  
**Benoît Smets**   
- Senior Researcher, Natural Hazards Service (GeoRiskA), Royal Museum for Central Africa (Tervuren, Belgium)  
- Assistant Professor, Cartography & GIS Research Group, Dpt. of Geography, Vrije Universiteit Brussel (Brussels, Belgium)  
  
To contact me --> MyFirstName.MyLastName@africamuseum.be or MyFirstName.MyLastName@vub.be  
  
    
-----  
  
**!!! PLEASE READ THE FOLLOWING DESCRIPTION BEFORE USING THE SCRIPTS FOR THE FIRST TIME !!!**  

## SCRIPT 0: Copy2singleFolder (optional)
*Current version:* **1.0.1** *(18th May 2021)*  

This script simply copies all the raw scanned photos that are stored in a series of subfolders, into a single folder. It has been developed as the technicians who are taking care of scanning and archiving the raw scanned photos follow a specific structure of folders and subfolders to store the raw scanned data. As all the following scripts are based on the assumption that all the photos to process are in the same folder (i.e., one directory path provided for the input data), this small script allows copying the scanned data into an appropriate single place for their preprocessing. It also has the advantage of leaving the original scans where they are, and making us working on a copy of them.

The required Python modules are **os** and **shutil**. They are both default modules within Python.

**The parameters to provide are:**  
*- The path of the source folder (i.e., master folder where all the photos and subfolders are located)*  
*- The path of the destination folder*  
*- The file format of the photos (by default, .tif), in case other files are stored in the folder and subfolders*  

## SCRIPT 1: AirPhoto_CanvasSizing 
*Current version:* **1.0.1** *(18th May 2021)*  
  
This script aims to get images with the same number of pixels in width and height, which is not always the case with scanned photographs. The script will look at all photographs available in a given directory and search for the maximum width and height values in the dataset. Once found, it will homogenize the dataset by adding rows and/or columns of black pixels to images that don't have these maximum dimensions.  
  
**The required Python modules:**  
*- Glob*  
*- Joblib*  
*- OpenCV*  
*- Pillow*  
  
**The parameters that have to be adapted by the user:**  
*- Input folder (where the raw scans are located)*  
*- Output folder (where the resized images will be saved)*  
*- The image format of the input images (e.g., tif, jpeg, png, etc.)*  
*- The number of CPU cores to use for the parallel processing (by default: max - 1)*  
  
The output images will be saved with the same name as the input images, complemented with "_CanvasSized". The images will be saved in tif format, as I personnally only work with raw (uint16) tif files. If you want to change this, you have to adapt the file format in the script, in line 109.  
  
  
## SCRIPT 2: AirPhoto_reprojection  
*Current version:* **1.0.1** *(18th May 2021)*  
  
This script aims to reproject the aerial photographs based on the pixel coordinates of the fiducial marks, in order to obtain a homogeneous dataset with the center of perspective located in the middle of the images. To run this script, you first need to create a table, in csv format, containing the XY coordinates (in pixel) of four fiducial marks used to locate the center of perspective. A template of such a table is provided. Please, keep the name of each columns similar to those in the template, as these names are used in the script to find the corresponding information.  
  
***The required Python modules:**  
*- Glob*  
*- Joblib*  
*- Numpy*  
*- OpenCV*  
*- Pandas*  
  
**The parameters that have to be adapted by the user:**  
*- Input folder (with the "canvas-sized" images)*  
*- Directory path of the csv file with the pixel coordinates of the fiducial marks*  
*- Output folder (where the standardized images will be saved)*  
*- The new pixel coordinates of the fiducial marks in the output images (must be estimated based on the type of photo and scanning resolution)*  
*- The dimensions in width (X) and height (Y) of the output images (unit = pixel)*  
*- The image format of the input images (e.g., tif, jpeg, png, etc.)*  
*- The number of CPU cores to use for the parallel processing (by default: max - 1)*   
  
The output images will be saved with the same name as the input images, complemented with "_standardized". The images will be saved in tif format, as I personally only work with raw (uint16) tif files. If you want to change this, you have to adapt the file format in the script, in line 130.

## Downsampling of the images

In order to smooth the potential noise introduced by the reprojection of each image, **I strongly suggest to downsample the images to a lower resolution**. At the RMCA, we scan the photos at a resolution of 1500 dpi (except for specific collections), which is, in general, too much considering the quality of the collections. So, we use to resample the reprojected photos to 900 dpi (+ or - 300 dpi, depending on the quality of the dataset).

After several tests with different resampling algorithms and Python modules, it appears that **the best resampling method to obtain a good photogrammetric result is the "Bicubic Sharper" algorithm of Adobe Photoshop(R)**. This algorithm is by far better than any other available with Python modules. So I strongly recommend to use Photoshop for this step. Otherwise, the downsampling could be performed with Python modules like Pillow, OpenCV or Scikit-Image.

*If, in any case, you find an open-source equivalent of the Bicubic Sharper algorithm of Photoshop, please do not hesitate to share this information with me! Thank you in advance!*  

## SCRIPT 3: CreateSingleMask (optional)
*Current version:* **1.0.1** *(18th May 2021)*  

This script is only useful for photogrammetric software that allows you to apply a single mask file to all the photos of the same dimensions, like with Agisoft Photoscan/Metashape Pro.

This script aims to create a mask with the same dimensions of the preprocessed photos (i.e., photos sized, reprojected and downsampled). The mask consists of rectangles hiding the image corners, where the fiducial marks are ususally still visible on the final photos. In a future version of the script, an option will be added to hide fiducial marks that are at mid-distance between the corners of the image.

**The required Python modules to add (in addition to the Anaconda Distribution):**  
*- Glob*   
*- Numpy*  
*- Pillow*  

**The parameters that have to be adapted by the user:**  
*- Input folder (with the reprojected photos)*  
*- Output mask folder (where the mask will be stored)*  
*- The image format (of the reprojected photos)*  
*- The size of the rectangles to mask in the corners of the photos (in percentage of the photo's width and height)*  
*- The name of the dataset (i.e., the name you will give to the mask)*  

The output mask will be saved with the given name of the dataset, complemented with "_mask". The mask will be saved in png format, as Agisoft Photoscan/Metashape Pro preferentially works with this format for masks. If you want to change this, you have to adapt the mask format in the script, in line 133.


-----

**Prof. Dr. Benoît SMETS**  
Natural Hazards Service (GeoRiskA)  
ROYAL MUSEUM FOR CENTRAL AFRICA -- Tervuren, Belgium  
Cartography & GIS Research Group (CGIS)  
VRIJE UNIVERSITEIT BRUSSEL -- Brussels, Belgium  
  
https://georiska.africamuseum.be/en  
https://we.vub.ac.be/en/cartography-and-gis  
http://www.virunga-volcanoes.org/  
https://bsmets.net/  
