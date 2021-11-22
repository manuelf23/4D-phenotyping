# Pheno4D - Calibration
This application allows to generate the calibration files for the system to be able to produce the 4D phenotyping

## User guide
For the application to work it is necessary to have installed the python libraries described in the requirement.txt file.
To start the application, you must enter this folder from a terminal and execute the following command:
```bash
python main.py
```
Once the application starts, it will request the following information to be able to generate the calibrations:      
| Information                                                 | Description                                                                                                                                                                                                                                                                                                                                               |
|-------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Folder for saving calibrations                              | folder path to save the results of the all calibrations                                                                                                                                                                                                                                                                                                   |
| Geometric Calibration - Plane calibration                   | path to the folder where the PCD data for plane calibration is                                                                                                                                                                                                                                                                                            |
| Geometric Calibration - Center of the turntable calibration | path to the .csv file that contains the PCD for finding the center of the turn table                                                                                                                                                                                                                                                                      |
| Y limit                                                     | the range is requested in meters from where the points in 3D space will be taken into account in relation to the Y axis. This range would filter the points that are between the sensors and the plant and the points that are behind the plant.                                                                                                          |
| Z limit                                                     | the range is requested in meters from where the points in 3D space will be taken into account in relation to the Z axis. This range would filter the points that are below the base of the plant and above the height of the plant. If the sensors are located at a height of 1.5m the base of the rotating base would be approximately in a Z-min: -0.48 |
| Multispectral image registration                            | path to the folder where the multispectral images with the calibration board are                                                                                                                                                                                                                                                                          |
| 4D Geometric calibration (sensory fusion)                   | path to the folder where the multispectral images and PCD data for sensory fusion calibration are                                                                                                                                                                                                                                                         |
## Data structure
This section describes the structure of the data files and folders.
### Geometric Calibration - Plane calibration
This is a folder with .cvs files that contains the PCD data for the plane calibration. Each .csv file must have as name the angle where the sensing was made.
The .csv files have the following columns:
| X | Y | Z | azimuth | laser_id |
|---|---|---|---------|----------|

### Geometric Calibration - Center of the turntable calibration
This is a .csv file that contains the PCD for finding the center of the turn table
The .csv file has the following columns:
| X | Y | Z | azimuth | laser_id |
|---|---|---|---------|----------|

### Multispectral image registration
This is a folder that contains the images for the multispectral image registration calibration.
The structure of the folder is as follows:
📦 multispectral_image_registration
 ┣ 📂 0710
 ┃ ┣ 📜 IMG_160101_001209_0000_GRE.TIF
 ┃ ┣ 📜 IMG_160101_001209_0000_NIR.TIF
 ┃ ┣ 📜 IMG_160101_001209_0000_RED.TIF
 ┃ ┣ 📜 IMG_160101_001209_0000_REG.TIF
 ┃ ┣ 📜 IMG_160101_001209_0000_RGB.JPG
 ┣ 📂 0711
 ┃ ┣ 📜 IMG_160101_001219_0000_GRE.TIF
 ┃ ┣ 📜 IMG_160101_001219_0000_NIR.TIF
 ┃ ┣ 📜 IMG_160101_001219_0000_RED.TIF
 ┃ ┣ 📜 IMG_160101_001219_0000_REG.TIF
 ┃ ┣ 📜 IMG_160101_001219_0000_RGB.JPG

### 4D Geometric calibration (sensory fusion)
This is a folder that contains the multispectral images and PDC data for the sensory fusion calibration.
The structure of the folder is as follows:
A folder with the multispectral images and .csv file with the PCD data at the same level of the images folder.
📦 sensory_fusion
 ┣ 📂 1
 ┃ ┣ 📜 IMG_160101_050739_0000_GRE.TIF
 ┃ ┣ 📜 IMG_160101_050739_0000_NIR.TIF
 ┃ ┣ 📜 IMG_160101_050739_0000_RED.TIF
 ┃ ┣ 📜 IMG_160101_050739_0000_REG.TIF
 ┃ ┣ 📜 IMG_160101_050739_0000_RGB.JPG
 ┣ 📂 2
 ┃ ┣ 📜 IMG_160101_051215_0000_GRE.TIF
 ┃ ┣ 📜 IMG_160101_051215_0000_NIR.TIF
 ┃ ┣ 📜 IMG_160101_051215_0000_RED.TIF
 ┃ ┣ 📜 IMG_160101_051215_0000_REG.TIF
 ┃ ┣ 📜 IMG_160101_051215_0000_RGB.JPG
 ┣ 📂 3
 ┃ ┣ 📜 IMG_160101_051356_0000_GRE.TIF
 ┃ ┣ 📜 IMG_160101_051356_0000_NIR.TIF
 ┃ ┣ 📜 IMG_160101_051356_0000_RED.TIF
 ┃ ┣ 📜 IMG_160101_051356_0000_REG.TIF
 ┃ ┣ 📜 IMG_160101_051356_0000_RGB.JPG
 ┣ 📜 1.csv
 ┣ 📜 2.csv
 ┣ 📜 3.csv
 The .csv file has the following columns:
 | X | Y | Z | azimuth | laser_id |
|---|---|---|---------|----------|
WARNING: For the auto extraction of 2D points it is necesary that the RGB images have a blue or green background.