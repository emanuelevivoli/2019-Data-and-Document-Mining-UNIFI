# 2019 Data and Document Mining @ UniFi

<p align="center">
    <img src="University_of_Florence.png" alt="logo-UniFi" width="200"/>
</p>

# Introduction
This repo contains codes and documentations for the "Data and Document Mining" course at University of Florence.

The projects has been conducted together with @francidellungo.

The description report (in _Italian_) can be found in [Report_DDM](https://github.com/emanuelevivoli/2019-Data-and-Document-Mining-UNIFI/tree/main/Report_DDM.pdf).

# Structure

The repo is structured as follow:
- [Cs_to_Py](https://github.com/emanuelevivoli/2019-Data-and-Document-Mining-UNIFI/tree/main/Cs_to_Py) 
- [ClientCs_ServerPy](https://github.com/emanuelevivoli/2019-Data-and-Document-Mining-UNIFI/tree/main/ClientCs_ServerPy)

    ![C#](https://img.shields.io/badge/c%23-%23239120.svg?style=plastic&logo=c-sharp&logoColor=white) 
    ![Python](https://img.shields.io/badge/python-3670A0?style=plastic&logo=python&logoColor=ffdd54)
    
    Bridge for interconnecting position coordinates streams from eye tracker from `C#` SDK to `python` - _Italian_

- [DDM_eye_tracker](https://github.com/emanuelevivoli/2019-Data-and-Document-Mining-UNIFI/tree/main/DDM_eye_tracker)

    ![Python](https://img.shields.io/badge/python-3670A0?style=plastic&logo=python&logoColor=ffdd54)

    Analysis of position coordinates streams from the eye tracker to study where eyes concentrate most on text-ful screen - _Italian_

- [Gaze-plot](https://github.com/emanuelevivoli/2019-Data-and-Document-Mining-UNIFI/tree/main/Gaze-plot)
    
    ![Python](https://img.shields.io/badge/python-3670A0?style=plastic&logo=python&logoColor=ffdd54)

    A gaze plot displays movement sequence, order and duration of gaze fixation.


# Examples

Some images that show the text (1), its characters, words ans lines (2), the person saccades and fixations (3), and finally the gaze heatmap plot (4).

<p align="center">
    <img src="./ClientCs_ServerPy/gaze_analysis_example/PHOTO_00/PHOTO_00.png" alt="Original-Image" width="300"/>
    <img src="./ClientCs_ServerPy/gaze_analysis_example/PHOTO_00/PHOTO_00_colori.png" alt="Original-Image" width="300"/>
    <img src="./ClientCs_ServerPy/gaze_analysis_example/PHOTO_00/PHOTO_00_fixs.png" alt="Original-Image" width="300"/>
    <img src="./ClientCs_ServerPy/gaze_analysis_example/PHOTO_00/PHOTO_00_heat.png" alt="Original-Image" width="300"/>
</p>

Some of the files recorded from the user activity.


| id  | sec | word        | row_id  |
|----|----|--------------|----|
| 0  | 16 | monti        | 0  |
| 1  | 22 | golfi        | 4  |
| 2  | 2  | del          | 0  |
| 3  | 0  | Quel         | 2  |
| 4  | 1  | ramo         | 2  |
| 5  | 3  | lago         | 3  |
| 6  | 5  | Como         | 2  |
|    |    |     ...      |    |


# Contacts
If you are interested and have some questions, don't hesitate to contact us or open an issue.


# Licence
Thid-party licences must be respected ([tobi](https://developer.tobii.com/license-agreement/)).
We do not take responsability for the usage of this software.