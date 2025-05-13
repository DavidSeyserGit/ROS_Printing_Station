GUI Mover
==============================

This module (`GuiMover.py`) acts as a ROS node responsible for receiving joint commands from the GUI and controlling the SCARA robot using MoveIt!. It subscribes to the ``/chatter`` topic to get target joint values and uses the MoveIt! commander to plan and execute robot movements.


Code Structure
--------------

.. code-block:: python

   #!/usr/bin/env python
   import sys
   import rospy
   import moveit_commander
   from std_msgs.msg import String

   status_pub = rospy.Publisher("response", String, queue_size=10)
   error_pub = rospy.Publisher("error", String, queue_size=10)

   def chatter_callback(message):
       # ... callback logic ...
       pass

   if __name__ == '__main__':
       # ... initialization and main loop ...
       pass

Publishers
----------

The module initializes two ROS publishers:

*   ``status_pub`` (``rospy.Publisher``, topic: ``/response``, message type: ``std_msgs.msg.String``): Publishes status updates, typically the color of the status indicator, back to the GUI.
*   ``error_pub`` (``rospy.Publisher``, topic: ``/error``, message type: ``std_msgs.msg.String``): Publishes error messages encountered during message processing or motion execution back to the GUI. *(Note: The provided GUI code has an `error_callback` but doesn't explicitly subscribe to an `/error` topic; this suggests a potential area for synchronization between the GUI and this module if you intend to display these errors).*

Callback Function (`chatter_callback`)
--------------------------------------

This function is the callback for messages received on the ``/chatter`` topic. It is triggered when the GUI sends joint commands.

*   **Parameters:**
    *   ``message`` (``std_msgs.msg.String``): The received String message containing the target joint values from the GUI. The message is expected to be in the format "q1: <value> q2: <value> q3: <value>".

*   **Functionality:**
    *   Parses the incoming string message to extract the target values for joints q1, q2, and q3.
    *   Logs the received target joint values.
    *   Gets the current joint values of the robot using MoveIt!.
    *   Updates the target values for joints 0, 1, and 2 (corresponding to q1, q2, and q3) in the joint goal.
    *   Attempts to move the robot to the target joint configuration using ``move_group.go()``.
    *   If the motion execution fails, it publishes "red" to the ``/response`` topic and the error message to the ``/error`` topic.
    *   Stops any residual movement after the command using ``move_group.stop()``.
    *   Logs a success message if the motion completes without raising an exception.
    *   Includes general error handling to catch exceptions during message processing.

Main Execution Block
--------------------------------------------------

This block is executed when the script is run directly.

*   **Initialization:**
    *   Initializes the MoveIt! commander with command-line arguments.
    *   Initializes the ROS node named 'moveit_scara_controller'.
    *   Creates a ``RobotCommander`` and ``PlanningSceneInterface`` instance from MoveIt!.
    *   Initializes a ``MoveGroupCommander`` for the "scara" planning group.
    *   Logs a message indicating the node has been initialized and is waiting for commands.

*   **Subscription:**
    *   Subscribes to the ``/chatter`` topic with the ``chatter_callback`` function as the handler.

*   **ROS Spin:**
    *   Enters the ROS spin loop (``rospy.spin()``), which keeps the node alive and allows it to receive messages on subscribed topics. The script will remain active until it is shut down (e.g., by pressing Ctrl+C or a ROS shutdown command).

*   **Shutdown:**
    *   Performs necessary MoveIt! commander shutdown before the script exits.

