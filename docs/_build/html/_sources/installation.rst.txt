.. _installation: # Optional: A target for internal links

Installation Guide
==================

This document provides a high-level guide to installing and setting up the ROS Printing Station project. It assumes you have a working ROS Noetic environment installed on your system.

Prerequisites
-------------

Before proceeding with the project-specific installation, ensure you have the following prerequisites met:

*   **ROS Noetic Installation:** The project requires ROS Noetic. If you do not have it installed, please follow the official ROS Wiki installation guide for your operating system:

    `ROS Noetic Installation Guide <https://wiki.ros.org/noetic/Installation>`_

*   **Catkin Workspace:** It is recommended to build this project within a Catkin workspace. If you don't have one, you can create one following the ROS tutorials.

Cloning the Repository
----------------------

Navigate to the `src` directory of your Catkin workspace and clone the project repository:

.. code-block:: bash

   git clone https://github.com/DavidSeyserGit/ROS_Printing_Station.git

Installing Dependencies
-----------------------

Once the repository is cloned, you need to install the project's dependencies.

1.  **Update and Install ROS Dependencies with `rosdep`:**

    Navigate back to the root of your Catkin workspace and use `rosdep` to install any declared ROS package dependencies:

    .. code-block:: bash

       cd ROS_Printing_Station/ # Replace with your actual workspace root
       sudo apt-get update  # Ensure your package list is up to date
       rosdep install --from-paths src --ignore-src -r -y

    This command will install necessary ROS packages based on the `package.xml` files in your source directories.

2.  **Install Specific ROS Packages (if not covered by rosdep):**

    While `rosdep` should handle most ROS dependencies, explicitly installing common ones like controllers and MoveIt! components is good practice:

    .. code-block:: bash

       sudo apt-get install ros-noetic-joint-trajectory-controller
       sudo apt-get install ros-noetic-robot-state-publisher
       sudo apt-get install ros-noetic-moveit

3.  **Install Python Dependencies:**

    The GUI and other Python scripts have specific Python package requirements listed in `requirements.txt`. Install these using pip:

    .. code-block:: bash

       cd ROS_Printing_Station # Navigate to the project directory
       pip install -r requirements.txt

Building the Workspace
----------------------

After installing dependencies, build your Catkin workspace:

.. code-block:: bash

   catkin_make -j16


Sourcing the Setup File
-----------------------

Source the workspace's setup file to make the installed packages and executables available in your current terminal session:

.. code-block:: bash

   source devel/setup.bash

Running the Simulation
----------------------

To launch the full simulation environment and GUI, use the provided start script:

.. code-block:: bash

   cd ROS_Printing_Station # Navigate to the project directory
   ./scripts/start.sh

This script should launch all the necessary ROS nodes and the GUI.

Further Information
-------------------

*   **Known Issues:** For information on known issues, please refer to the project's GitHub repository:

    `Open Issues on GitHub <https://github.com/DavidSeyserGit/ROS_Printing_Station/issues>`_

*   **Repository Link:** The project's source code is available on GitHub:

    `ROS_Printing_Station Repository <https://github.com/DavidSeyserGit/ROS_Printing_Station>`_

