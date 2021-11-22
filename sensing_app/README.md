# Pheno4D - Sensing

This application runs on the embedded system of the phenotyping platform and is responsible for managing the actuators and sensors of the platform to capture morphological and biochemical information on plants.

## User guide
For the application to work it is necessary to have installed the python libraries described in the ./requirement.txt file.
To start the application, you must enter to this folder from a terminal and execute the following command:
```bash
python capture_data_pheno4d.py <ethernet-interface> <turntable_step_grade>
```
| Argument             | Type   | Description                                                                                                                                                                                                                                                                                                                                                                                            |
|----------------------|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ethernet-interface   | string | Network interface through which the LiDAR is connected to the platform                                                                                                                                                                                                                                                                                                                                 |
| turntable_step_grade | int    | For phenotyping, the platform rotates the plant that is on the turntable every x degrees and in those degrees the plant is sensed until completing a complete revolution of the plant. This parameter represents the steps in degrees that the plant will rotate for each sensing. For this version of the platform use one of the following values [6, 12, 18, 24, 30, 36, 60, 72, 90, 120, 180, 360] |