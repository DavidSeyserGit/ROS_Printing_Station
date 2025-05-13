Robot Mover Module
================================

This module (`RobotMover.py`) provides the ``RobotMove`` class and a helper function ``run_robot`` for controlling a robot arm using MoveIt! and executing pre-defined sequences of joint waypoints loaded from a JSON file.

.. _robot_mover_module: # Optional: A target for internal links

Code Structure
--------------

.. code-block:: python

   #!/usr/bin/env python
   import os
   import sys
   import json
   import time
   import threading # Note: Not directly used in the provided code snippet
   import rospy
   import moveit_commander

   class RobotMove:
       def __init__(self, robot_name, move_group_name, waypoints_file):
           # ... initialization ...
           pass

       def load_waypoints(self, file_path):
           # ... waypoint loading logic ...
           pass

       def move_to_position(self, joint_positions):
           # ... movement logic ...
           pass

       def print_current_pose(self):
           # ... print pose logic ...
           pass

       def execute_waypoints(self):
           # ... waypoint execution logic ...
           pass

   def run_robot(robot):
       # ... helper function ...
       pass

RobotMove Class
---------------

The ``RobotMove`` class encapsulates the functionality for controlling a specific robot arm defined within MoveIt!.

.. code-block:: python

   class RobotMove:
       def __init__(self, robot_name, move_group_name, waypoints_file):
           # ... initialization code ...
           pass
       # ... other methods ...

Initialization (`__init__`)
^^^^^^^^^^^^^^^^^^^^^^^^^^

Initializes the ``RobotMove`` object, setting up the connection to MoveIt! and loading the waypoints.

*   **Parameters:**
    *   ``robot_name`` (``str``): A name for the robot instance (e.g., used for ROS node name).
    *   ``move_group_name`` (``str``): The name of the MoveIt! planning group for this robot (e.g., "scara", "knick").
    *   ``waypoints_file`` (``str``): The file path to the JSON file containing the waypoint definitions.

*   **Key Actions:**
    *   Initializes a unique ROS node if one is not already initialized.
    *   Initializes the MoveIt! commander.
    *   Creates a ``MoveGroupCommander`` for the specified planning group.
    *   Sets velocity and acceleration scaling factors for planning and execution.
    *   Loads the waypoints from the specified JSON file using the ``load_waypoints`` method.

Load Waypoints (`load_waypoints`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Loads the waypoint data from a specified JSON file.

*   **Parameters:**
    *   ``file_path`` (``str``): The path to the JSON waypoints file.

*   **Returns:**
    *   ``list``: A list of dictionaries, where each dictionary represents a waypoint. Returns an empty list if the file is not found or has an invalid format.

*   **Expected Waypoint JSON Structure:** Each item in the list should be a dictionary with:
    *   ``"description"`` (``str``): A description of the waypoint action.
    *   ``"position"`` (``list[float]``): A list of joint values for the target position. The length of this list must match the number of joints in the MoveIt! planning group.
    *   ``"pause"`` (``float``, optional): The duration to pause in seconds after reaching this waypoint.
    *   ``"action"`` (``str``, optional): An optional message to log after reaching the waypoint.

*   **Error Handling:** Includes error handling for `FileNotFoundError`, `json.JSONDecodeError`, and other potential exceptions during file reading.

Move to Position (`move_to_position`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Commands the robot's joints to move to a specified set of joint positions.

*   **Parameters:**
    *   ``joint_positions`` (``list[float]``): A list of target joint values.

*   **Returns:**
    *   ``bool``: ``True`` if the movement successfully completes, ``False`` otherwise.

*   **Functionality:**
    *   Checks if the length of the provided joint positions matches the number of joints in the move group. Logs an error and returns ``False`` if they don't match.
    *   Sets the target joint values for the MoveIt! planning group.
    *   Executes the motion plan using ``move_group.go()`` with ``wait=True``.
    *   Calls ``move_group.stop()`` after the movement attempt.

Print Current Pose (`print_current_pose`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Logs the current Cartesian pose (position and orientation) of the robot's end effector (TCP - Tool Center Point).

*   **Action:** Retrieves the current pose using ``move_group.get_current_pose()`` and logs its position.

Execute Waypoints (`execute_waypoints`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Iterates through the loaded waypoints and commands the robot to move to each target joint position sequentially, including pauses and action logging as defined in the waypoint data.

*   **Action:**
    *   Checks if waypoints were successfully loaded.
    *   Loops through each waypoint in the loaded list.
    *    Extracts the description, joint positions, optional pause time, and optional action message.
    *   Logs the waypoint description.
    *   Calls ``move_to_position`` to move the robot to the waypoint's joint positions.
    *   Logs success or failure for each movement.
    *   Calls ``print_current_pose`` after a successful move.
    *   Logs the action message if provided.
    *   Pauses execution for the specified duration if a pause time is defined.
    *   Includes error handling for missing keys in waypoint data or other exceptions during waypoint processing.
    *   Logs a completion message after all waypoints are executed.

Helper Function (`run_robot`)
-----------------------------

A simple helper function to execute the waypoints for a given ``RobotMove`` object.

.. code-block:: python

   def run_robot(robot):
       """Helper function to run a robot's waypoint execution."""
       robot.execute_waypoints()

*   **Parameters:**
    *   ``robot`` (``RobotMove``): An instance of the ``RobotMove`` class.

*   **Action:** Calls the ``execute_waypoints`` method of the provided ``RobotMove`` object.

