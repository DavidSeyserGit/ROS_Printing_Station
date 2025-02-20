# Robot Station for Automated 3D Printing with Vision Detection

This project implements a robotic station for automated 3D printing, featuring two robotic arms and a vision detection system. The station is designed for a production environment, leveraging ROS for seamless integration and control.  This documentation covers the setup, installation, and operation of the entire system, as well as specific details for each robot's program.

## Overview

The automated 3D printing station utilizes two robotic arms to handle printed objects, increasing throughput and efficiency.  A vision system monitors the printing process and provides feedback for optimized operation.  This project aims to provide comprehensive documentation for all aspects of the station, from the overall environment setup to the individual robot programs.

## Documentation Structure

This documentation is divided into the following sections:

* **[Environment Setup](environment_setup.md):**  Instructions for setting up the required software environment, including ROS installation, dependencies, and any other necessary configurations. This covers the shared environment for both robots.
* **[Installation and Build](installation.md):**  Detailed steps for installing the project, cloning the repository, resolving dependencies, and building the ROS workspace.  This covers the build process for the entire system.
* **Robot Documentation:**
    * **[Robot 1](robot1/index.md):** Documentation specific to Robot 1, including:
        * **[Program Description](robot1/program_description.md):**  Details about Robot 1's program, its functionality, inputs, outputs, and any specific configurations.
        * **[Usage](robot1/usage.md):** Instructions for running Robot 1's program.
        * **[API Reference (Optional)](robot1/api.md):** If applicable, a reference for any custom APIs used in the program.
    * **[Robot 2](robot2/index.md):** Documentation specific to Robot 2, including:
        * **[Program Description](robot2/program_description.md):** Details about Robot 2's program, its functionality, inputs, outputs, and any specific configurations.
        * **[Usage](robot2/usage.md):** Instructions for running Robot 2's program.
        * **[API Reference (Optional)](robot2/api.md):** If applicable, a reference for any custom APIs used in the program.
* **[Vision System](vision.md):** Documentation for the vision system, including setup, calibration, and usage.
* **[Troubleshooting](troubleshooting.md):** Common issues and solutions related to the station.
* **[Contribution Guidelines](contributing.md):** Information on how to contribute to the project.
* **[License](license.md):** The license under which the project is released.

## Getting Started

To begin setting up the station, please start with the [Environment Setup](environment_setup.md) section.

## Contributing

Contributions are welcome! See the [Contribution Guidelines](contributing.md) for details.

## License

This project is licensed under the MIT License.  See the [License](license.md) file for details.