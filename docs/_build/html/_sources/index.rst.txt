.. ROS Printing Station documentation master file, created by
   sphinx-quickstart on Tue May 13 13:47:24 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the ROS Printing Station Documentation!
==================================================

.. meta::
   :description: Documentation for the ROS Printing Station project, a robot manipulation application for automated printing tasks.
   :keywords: ROS, robot, manipulation, printing, automation, SCARA, MoveIt, Tkinter, GUI

This documentation provides comprehensive information about the ROS Printing Station project, a system designed to automate printing tasks using a robotic manipulator integrated with the Robot Operating System (ROS).

Project Overview
----------------

The ROS Printing Station project aims to demonstrate and implement a robotic workcell capable of performing pick-and-place operations related to printing. Key aspects include:

*   **Robot Control:** Utilizing ROS and MoveIt! for robot motion planning and execution.
*   **Perception:** Incorporating camera feedback for task execution (e.g., identifying printing areas or paper).
*   **Graphical User Interface (GUI):** Providing a user-friendly interface for monitoring status, sending commands, and viewing camera feeds.
*   **Automated Workflows:** Implementing routines for automated printing tasks.

Whether you're a developer looking to contribute, a user wanting to understand how the system works, or just curious about ROS robotics, this documentation is your guide.

Getting Started
---------------

If you're new to the project, we recommend starting with the :doc:`installation` guide to set up the necessary environment and dependencies.


(Consider adding a diagram here if you have one!)

Table of Contents
-----------------

Below is the table of contents, guiding you through the different sections of the documentation:

.. toctree::
   :maxdepth: 2
   :caption: Documentation Contents:

   installation
   gui
   GuiMover
   pick_and_place
   RobotMover