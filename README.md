| Supported Target | Jetson Orin Nano/Stm32 |
| ----------------- | ------- |

# WRO2025-AFTON

## Introduction

Welcome to the WRO2025-AFTON project! This innovative project focuses on developing a self-driving car system using how SBM the Stm32 microcontroller and how SBC a Jetson Orin Nano. The project leverages machine learning to navigate a track with randomly placed green and red traffic signs, ensuring the vehicle follows the correct lane. The primary components of the system include the AFTON API for training the model and the AFTON SmartWheels for the main microcontroller operations. Detailed information can be found in the Technical Specification Document.

![Team Photo](v-photos/AftonSmartWheels(Prom).png)


![d](D:\Users\yulia\Nueva carpeta\WRO2025-AFTON\img.png)
## Content
This repository contains the following main directories and files:

* `t-photos` contains 2 photos of the team (an official one and one funny photo with all team members)
* `v-photos` contains 6 photos of the vehicle (from every side, from top and bottom)
* `video` contains the video.md file with the link to a video where driving demonstration exists
* `schemes` contains one or several schematic diagrams in form of JPEG, PNG or PDF of the electromechanical components illustrating all the elements (electronic components and motors) used in the vehicle and how they connect to each other.
* `src` contains code of control software for all components which were programmed to participate in the competition.
  - **src**: Source code for the project, including two main components:
    - **afton-selfdriving-car**: Code (Version 2) for the main microcontroller Rock 3A
    - **afton-api**: Code (Version 1) for training the machine learning model.
    - **afton-smartwheels**: Code (Version 1) for the main microcontroller ESP32S3.
* `models` is for the files for models used by 3D printers, laser cutting machines and CNC machines to produce the vehicle elements. If there is nothing to add to this location, the directory can be removed.
* `other` is for other files which can be used to understand how to prepare the vehicle for the competition. It may include documentation how to connect to a SBC/SBM and upload files there, datasets, hardware specifications, communication protocols descriptions etc. If there is nothing to add to this location, the directory can be removed.

## How to Clone the Repository

To clone this repository, use the following command:

```bash
git clone https://github.com/danielvvhfk/WRO2025-AFTON.git
```


## Instructions to Install
Follow these steps to set up the development environment:

### Visual Studio Code

1. Download and install Visual Studio Code from [here](https://code.visualstudio.com/).
2. Install the necessary extensions for ESP-IDF development.


### Radxa Rock 3A

1. Follow the getting started guide for Radxa Rock 3A from the official Radxa documentation [here](https://wiki.radxa.com/Rock3/getting_started/rock-3a).

### Python

1. Download and install Python from [here](https://www.python.org/).
2. Ensure that Python is added to your system PATH.

### Install Dependencies

Navigate to the project directory and install the required Python packages:

```bash
pip install -r requirements.txt
```

### TVL Library

Install the TVL library for AI model training:

```bash
pip install tvl
```

### LLVM Library

Install the LLVM library for AI model training:

```bash
pip install llvm
```

## Technical Specification Document

For a comprehensive overview of the project, refer to the Technical Specification Document located at:

```
WRO2025-AFTON/other/Technical Specification Document Future Engineers AFTON TECH(V2).pdf
```

