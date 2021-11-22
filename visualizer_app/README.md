# Pheno4D - Visualizer
This application combines 3D point cloud information with multispectral plant information to show a 4D representation of it.

## User guide
For the application to work it is necessary to have installed the python libraries described in the requirement.txt file.
To start the application, you must enter to this folder from a terminal and execute the following command:
```bash
python main.py
```
Once the application starts, it will request the following information to be able to generate the 4D phenotyping models:
| Information                                          | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 4D calibration (Sensory Fusion)                      | path to the .csv file where the calibration data between the multispectral camera and the LiDAR 3D is located                                                                                                                                                                                                                                                                                                                                                                         |
| Geometric Calibration                                | path to the .json file where you can find the calibration data of the reference plane of the turntable and the coordinates of the center of the turntable with respect to the 3D LiDAR                                                                                                                                                                                                                                                                                                |
| Multispectral images registration calibration Folder | path to the folder where the .pickle files are located for the image registration between each of the multispectral bands to the RGB image of the camera. It is a .pickle file for each multispectral band                                                                                                                                                                                                                                                                            |
| PCD and Images Folder                                | path to the folder where the point clouds and multispectral images are located. In this folder the data must be structured in a special way. Review the data structure section *.                                                                                                                                                                                                                                                                                                     |
| Y limit                                              | the range is requested in meters from where the points in 3D space will be taken into account in relation to the Y axis. This range would filter the points that are between the sensors and the plant and the points that are behind the plant.                                                                                                                                                                                                                                      |
| Z limit                                              | the range is requested in meters from where the points in 3D space will be taken into account in relation to the Z axis. This range would filter the points that are below the base of the plant and above the height of the plant. If the sensors are located at a height of 1.5m the base of the rotating base would be approximately in a Z-min: -0.48                                                                                                                             |
| Divisor                                              | This value indicates how many angles of the sensed information will be taken into account for processing. For example, for a step angle of 12 the plant will be sensed at the angles [0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120, 132, 144, 156, 168, 180, 192 , 204, 216, 228, 240, 252, 264, 276, 288. 300. 312. 324, 336, 348] and selecting a divisor of 36 will only take into account to process the data sensed in the angles [0, 36, 72, 108, 144, 180, 216, 252, 288, 324]. |
| Step angle                                           | this value represents the steps in angles between each rotation of the turntable in which the plant was sensed. For the data captured with this platform it is 12º                                                                                                                                                                                                                                                                                                                    |
## Data structure
This section describes the structure of the data files and folders.
### 4D calibration (Sensory Fusion)
This is a csv file that has the following columns (all values are floats):
| HC | frame | u | v | x | y | z |
|----|-------|---|---|---|---|---|
### Geometric Calibration
This is a JSON file with the following structure:
| R                                                                    | x_center                                                             | y_center                                                             |
|----------------------------------------------------------------------|----------------------------------------------------------------------|----------------------------------------------------------------------|
| This is the 3x3 matrix that calibrates the turntable reference plane | x coordinate of the center of the turntable with respect the sensors | y coordinate of the center of the turntable with respect the sensors |

```json
{
    "R": [
        [
            0.99948284,
            0.00112413,
            -0.03213697
        ],
        [
            0.00112413,
            0.99755653,
            0.06985494
        ],
        [
            0.03213697,
            -0.06985494,
            0.99703937
        ]
    ],
    "x_center": 0.063,
    "y_center": -0.972
}
```

### Multispectral images registration calibration Folder
folder where the .pickle files are located for the image registration between each of the multispectral bands to the RGB image of the camera.
The file names must be as follows:
| Band     | File Name        |
|----------|------------------|
| RGB      | RGB_CALIB.pickle |
| RED EDGE | REG_CALIB.pickle |
| RED      | RED_CALIB.pickle |
| GEEN     | GRE_CALIB.pickle |
| NIR      | NIR_CALIB.pickle |

### PCD and Images Folder
Since the platform senses the plant every X rotation degree of the turntable, there will be a folder that has the name of the degree where the plant was sensed and within this folder there will be the multi-spectral images corresponding to the sensing.
At the same level as the folders that contain the images, it will be found a CSV file that has the name of the degree where the plant was sensed that contains the information of the point cloud of the plant at that angle in which it was sensed.

📦 4D_data (PCD and Images Folder)
 ┣ 📂 0
 ┃ ┣ 📜 IMG_160101_033302_0000_GRE.TIF
 ┃ ┣ 📜 IMG_160101_033302_0000_NIR.TIF
 ┃ ┣ 📜 IMG_160101_033302_0000_RED.TIF
 ┃ ┣ 📜 IMG_160101_033302_0000_REG.TIF
 ┃ ┣ 📜 IMG_160101_033302_0000_RGB.JPG
 ┣ 📂 12
 ┃ ┣ 📜 IMG_160101_033413_0000_GRE.TIF
 ┃ ┣ 📜 IMG_160101_033413_0000_NIR.TIF
 ┃ ┣ 📜 IMG_160101_033413_0000_RED.TIF
 ┃ ┣ 📜 IMG_160101_033413_0000_REG.TIF
 ┃ ┣ 📜 IMG_160101_033413_0000_RGB.JPG
 ┃ ...
 ┣ 📜 0.csv
 ┣ 📜 12.csv
 ┣ ...
 
The CSV file that contains the point cloud information has the following columns:
| X | Y | Z | azimuth | laser_id |
|---|---|---|---------|----------|
