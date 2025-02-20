# Robot Station for 3D Printing with Vision Detection

![Python](https://img.shields.io/badge/Python-3.8-blue.svg)
![C++](https://img.shields.io/badge/C++-17-blue.svg)
![ROS](https://img.shields.io/badge/ROS-Noetic-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## Overview

This project implements a robot station for automated 3D printing in a production environment, leveraging the Robot Operating System (ROS) for seamless integration and control. The station integrates a vision detection system to optimize the printing process and enhance efficiency.  The core components of the station, all managed within the ROS framework, are:

* **3D Printing:** 
* **Robot Manipulation:** A robotic arm, controlled through ROS, is used to unload the printed objects from the printers.
* **Vision System:**

## Functional Description
![Flow Chart of the ROS Nodes](docs/flowchart/flowchart.png){ width=70% }


## Hardware Components

* **Robot Arm:** 
* **Vision System:** 

## Software Components (ROS-focused)


## ROS Nodes

## Build Instructions (ROS-specific)

1. **ROS Environment:** Ensure you have a ROS environment set up with the required ROS distribution.
2. **Dependencies:** Install the necessary ROS packages using `rosdep`:

   ```bash
   sudo apt-get update  # Update package list
   rosdep install --from-paths src --ignore-src -r -y

## This is for a Course in the Master Robotics Engineering at UAS Technikum Wien
