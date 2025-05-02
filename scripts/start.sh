#!/bin/bash
# Start the GUI application
echo "Starting GUI..."
#python3 scripts/gui/gui.py &

# Launch the ROS launch file
echo "Starting ROS launch..."
roslaunch printing_station run.launch