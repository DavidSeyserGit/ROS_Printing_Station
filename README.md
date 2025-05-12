# Robot Station for 3D Printing with Vision Detection

![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/DavidSeyserGit/ROS_Printing_Station)
![Python](https://img.shields.io/badge/Python-3.8-blue.svg)
![C++](https://img.shields.io/badge/C++-17-blue.svg)
![ROS](https://img.shields.io/badge/ROS-Noetic-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This project implements a simulation for robot station for automated 3D printing in a production environment.
## Functional Description

## Quick Start
move to the repo and compile

   ```bash
   cd ROS_Printing_Station
   catkin_make -j16
   source /devel/setup.sh
   ```

to start the simulation run the following:

   ```bash
   ./scripts/start.sh
   ```
   
## Software Components
This Porject requires ROS Noetic to be install on your system. For a detailed guide on how to install ROS please use the ROS Wiki. [ROS-Wiki](https://wiki.ros.org/noetic/Installation)

### GUI
The GUI is written in Python, to include all neccesarry python packages please use the requirements.txt file. 

   ```bash
   pip install -r requirments.txt
   ```
## Known Issues
The see the current open Issues please look at the issues tab
[Open Issues](https://github.com/USERNAME/REPOSITORY/issues)

## Build Instructions (ROS-specific)

1. **ROS Environment:** Ensure you have a ROS environment set up with the required ROS distribution
2. **Dependencies:** Install the necessary ROS packages using `rosdep`:

   ```bash
   sudo apt-get update  # Update package list
   rosdep install --from-paths src --ignore-src -r -y
   sudo apt-get install ros-noetic-joint-trajectory-controller
   sudo apt-get install ros-noetic-robot-state-publisher
   sudo apt-get install ros-noetic-moveit
   ```

## Link to this repo 
https://github.com/DavidSeyserGit/ROS_Printing_Station
## This is for a Course in the Master Robotics Engineering at UAS Technikum Wien
