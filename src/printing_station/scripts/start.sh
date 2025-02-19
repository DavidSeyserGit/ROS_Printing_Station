#!/bin/bash

# Start the GUI application
echo "Starting GUI..."
# Replace 'your_gui_application' with the actual command to start your GUI
python3 src/gui/gui.py &

# Wait for a few seconds to ensure the GUI has started
sleep 5

# Launch the ROS launch file
echo "Starting ROS launch..."
# Replace 'your_ros_package' and 'your_launch_file.launch' with your actual package and launch file names
roslaunch printing_station station.launch