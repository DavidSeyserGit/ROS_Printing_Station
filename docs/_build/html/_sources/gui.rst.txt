GUI
========================

This section provides documentation for the Graphical User Interface (GUI) module of the ROS Printing Station, which allows for interaction with the ROS nodes and robot control.

The GUI is implemented in a single Python file (e.g., `gui.py`) and utilizes the Tkinter library for the user interface and the `rospy` library for interacting with the ROS system.

Key Features:

*   Visual feedback of robot status (via color indicator).
*   Display of two camera feeds.
*   Button to initiate the robot's automated routine.
*   Entry fields and button to send joint commands (X, Y, Z values).
*   Ability to toggle between the two camera views.
*   Display of error messages received from the ROS system.

ROSGUI Class
------------

The main component of the GUI is the ``ROSGUI`` class.

.. code-block:: python

   class ROSGUI:
       def __init__(self, master):
           # ... initialization code ...

       def create_widgets(self):
           # ... widget creation code ...

       # ... other methods ...

The ``ROSGUI`` class is responsible for setting up the Tkinter window, initializing ROS nodes and subscribers/publishers, and handling user interactions and ROS message callbacks.

Initialization (`__init__`)
^^^^^^^^^^^^^^^^^^^^^^^^^^

The `__init__` method sets up the main window, initializes the ROS node if necessary, creates ROS subscribers and publishers, and initializes variables for image handling and camera view tracking.

*   **Parameters:**
    *   ``master`` (``tkinter.Tk``): The root Tkinter window.

*   **Key Actions:**
    *   Sets the window title and geometry.
    *   Configures the window's background color.
    *   Initializes the ROS node named 'gui'.
    *   Subscribes to ``/response`` (String), ``/static_camera/image_raw`` (Image), and ``/camera2/image_raw`` (Image).
    *   Creates a publisher for the ``/chatter`` topic (String).
    *   Initializes ``cv_bridge`` for image conversion.
    *   Initializes variables for storing camera images and the active camera view.
    *   Calls ``create_widgets`` to build the GUI elements.

Creating Widgets (`create_widgets`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``create_widgets`` method constructs all the visual elements of the GUI using Tkinter.

*   **Layout:** Uses a grid layout manager for the main frames and packed/gridded elements within frames.
*   **Sections:** Organizes widgets into sections like Status, Controls, and Camera Views.
*   **Widgets Created:**
    *   Frames (``left_frame``, ``image_frame``, ``status_section``, ``entry_frame``, ``camera_controls``).
    *   Labels (for status, error messages, coordinate entries, camera views).
    *   A Canvas for the ROS status indicator.
    *   Buttons (Start Robot Operation, Send Joint Values, Switch Camera View).
    *   Entry fields (for X, Y, and Z coordinates).
    *   Labels to display camera feeds (``image_label1``, ``image_label2``).

Toggle Camera View (`toggle_camera_view`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Switches the currently displayed camera feed between the first and second camera views.

*   **Action:** Hides the currently active camera label and displays the other one. Updates the ``active_camera`` attribute and changes the appearance of the camera labels to indicate the active view.

ROS Message Callback (`callback`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Callback function for the ``/response`` topic.

*   **Parameters:**
    *   ``msg`` (``std_msgs.msg.String``): The received String message.
*   **Action:** Updates the color of the ROS status indicator circle based on the received message data.

Publish on Topic (`publish_on_topic`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Publishes the values from the X, Y, and Z entry fields onto the ``/chatter`` topic.

*   **Action:** Reads the text from the X, Y, and Z entry widgets, formats it into a single string, publishes it, and then clears the entry fields.

Error Callback (`error_callback`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Callback function for receiving error messages. *(Note: Your code defines this method but does not subscribe to an error topic.)*

*   **Parameters:**
    *   ``msg`` (``std_msgs.msg.String``): The received error message.
*   **Action:** Updates the text and color of the error label to display the received error message.

Image Callback 1 (`image_callback1`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Callback function for the ``/static_camera/image_raw`` topic.

*   **Parameters:**
    *   ``msg`` (``sensor_msgs.msg.Image``): The received Image message.
*   **Action:** Converts the ROS Image message to a format usable by Tkinter (using ``cv_bridge`` and PIL), and updates ``image_label1`` to display the image. Includes error handling for the conversion process.

Image Callback 2 (`image_callback2`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Callback function for the ``/camera2/image_raw`` topic.

*   **Parameters:**
    *   ``msg`` (``sensor_msgs.msg.Image``): The received Image message.
*   **Action:** Converts the ROS Image message to a format usable by Tkinter (using ``cv_bridge`` and PIL), and updates ``image_label2`` to display the image. Includes error handling for the conversion process.

Start Robot Operation (`start_robot`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Initiates the main robot routine on a separate thread.

*   **Action:** Creates and starts a new Python thread that executes the ``run_robot_routine`` method. This prevents the robot operation from freezing the GUI.

Run Robot Routine (`run_robot_routine`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Executes the external robot pick-and-place routine.

*   **Action:** Calls the ``robot_main()`` function imported from the ``pick_and_place`` module. Includes basic error logging for exceptions that occur during the routine execution.

