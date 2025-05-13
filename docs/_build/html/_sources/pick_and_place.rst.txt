Pick and Place Module
===================================

This module (`pick_and_place.py`) orchestrates the automated pick-and-place operation for the ROS Printing Station. It involves spawning a placeholder object in Gazebo, moving the "knick" arm to grasp it (simulated by reaching a pre-defined pose), and then moving a SCARA arm along waypoints for the printing task, and finally despawning the object.

.. _pick_and_place_module: RobotMover

Code Structure
--------------

.. code-block:: python

   #!/usr/bin/env python
   import rospy
   import moveit_commander
   # ... other imports ...
   from RobotMover import RobotMove, run_robot # <-- Imported from RobotMover
   import random
   from std_msgs.msg import String

   pub = rospy.Publisher("response", String, queue_size=10)

   # ... pre-defined poses and joint targets ...

   def spawn_object(model_path, model_name, initial_pose):
       # ... spawn object logic ...
       pass

   def main():
       # ... main pick and place routine ...
       pass

   if __name__ == "__main__":
       # ... initialization and execution ...
       pass

Publishers
----------

The module utilizes one ROS publisher:

*   ``pub`` (``rospy.Publisher``, topic: ``/response``, message type: ``std_msgs.msg.String``): Publishes status updates (like "yellow", "red", "green") back to the GUI to indicate the state of the pick-and-place process.

Pre-defined Poses and Joint Targets
-----------------------------------

The script defines several pre-configured poses and corresponding joint targets used during the pick-and-place sequence.

*   ``traget_pose_1`` to ``traget_pose_5``: Cartesian poses (X, Y, Z, Quaternion) representing potential pick-up locations for the object.
*   ``drop_off_pose``: A Cartesian pose representing the location where the object is notionally placed.
*   ``joint_target_1`` to ``joint_target_5``: Joint space configurations (for the "knick" arm) corresponding to reaching the respective ``traget_pose_X`` locations.
*   ``joint_target_drop_off``: A joint space configuration for the "knick" arm at the drop-off position.

Spawning Object Function (`spawn_object`)
-----------------------------------------

This function handles the spawning of a specified SDF model into the Gazebo simulation environment.

*   **Parameters:**
    *   ``model_path`` (``str``): The file path to the SDF model file.
    *   ``model_name`` (``str``): The desired name for the spawned model in Gazebo.
    *   ``initial_pose`` (``geometry_msgs.msg.Pose``): The initial pose (position and orientation) where the model should be spawned.

*   **Functionality:**
    *   Waits for the ``/gazebo/spawn_sdf_model`` service to be available.
    *   Reads the SDF model XML from the specified file.
    *   Calls the spawn service with the provided model name, XML, and initial pose.
    *   Logs success or failure of the spawning operation.

Main Execution (`main`)
-------------------------------

This is the primary function that orchestrates the automated pick-and-place process. It is typically called by the GUI's start routine.

*   **Process Flow:**
    1.  Publishes "yellow" to the ``/response`` topic to indicate the start of the process.
    2.  Randomly selects one of the five target pick-up locations (``traget_pose_1`` to ``traget_pose_5``).
    3.  Determines the corresponding initial pose for the object in Gazebo (slightly below the target pick-up pose).
    4.  Attempts to spawn the specified object model at the determined initial pose using the ``spawn_object`` function. Logs a warning if spawning fails.
    5.  Initializes the MoveIt! commander (if not already initialized by the ROS node).
    6.  Creates a ``MoveGroupCommander`` for the "knick" arm and configures planning parameters.
    7.  Sets the joint target for the "knick" arm to the selected pick-up joint configuration (corresponding to the randomly chosen target pose).
    8.  Plans and attempts to execute the motion for the "knick" arm to reach the pick-up position. Publishes "red" if planning fails.
    9.  Sets the joint target for the "knick" arm to the drop-off joint configuration.
    10. Plans and attempts to execute the motion for the "knick" arm to reach the drop-off position. Publishes "red" if planning fails.
    11. Selects the appropriate SCARA waypoints file (`scara_wp.json` or `scara_wp2.json`) based on whether the randomly chosen target index was even or odd.
    12. **Initializes a robot control object:**
        Uses the :py:class:`RobotMove` class from the :ref:`RobotMover` to create an instance for controlling the "scara" arm with the selected waypoints file.

        .. code-block:: python

           scara_robot = RobotMove(
               robot_name="scara",
               move_group_name="scara",
               waypoints_file=scara_waypoints_file,
           )

    13. **Runs the SCARA routine:**
        Calls the :py:func:`run_robot` helper function (also from the :ref:`RobotMover`) to execute the waypoints defined in the selected file for the SCARA arm.

        .. code-block:: python

           run_robot(scara_robot)

    14. Attempts to delete the spawned object model from Gazebo using the ``/gazebo/delete_model`` service. Logs errors if despawning fails.
    15. Publishes "green" to the ``/response`` topic to indicate successful completion of the entire routine.
    16. Includes general error handling for issues during MoveIt! planning or execution.

Main Execution Block
--------------------------------------------------

This block is executed when the script is run directly (though it's typically called as a function from the GUI).

*   Initializes the ``pub`` publisher (though it's already initialized at the module level, which is slightly redundant).
*   Calls the ``main()`` function within a try-except block to catch potential ROS interrupt exceptions and other unexpected errors.
*   Ensures ``moveit_commander.roscpp_shutdown()`` is called in a ``finally`` block to clean up MoveIt! resources when the script exits.

