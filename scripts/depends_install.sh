#!/bin/bash
# ==================================================
# PRINTING STATION DEPENDENCY INSTALLER
# For systems with ROS Noetic already installed
# ==================================================

echo "[1/4] Installing MoveIt and dependencies..."
sudo apt-get install -y \
    ros-noetic-moveit-ros \
    ros-noetic-moveit-planners \
    ros-noetic-moveit-ros-move-group \
    ros-noetic-moveit-simple-controller-manager \
    ros-noetic-moveit-ros-visualization \
    ros-noetic-joint-trajectory-controller \
    ros-noetic-position-controllers

echo "[2/4] Installing Gazebo integration..."
sudo apt-get install -y \
    ros-noetic-gazebo-ros-pkgs \
    ros-noetic-gazebo-ros-control

echo "[3/4] Installing ROS control stack..."
sudo apt-get install -y \
    ros-noetic-ros-control \
    ros-noetic-ros-controllers \
    ros-noetic-robot-state-publisher

echo "[4/4] Verifying installations..."
rospack find moveit_ros_move_group > /dev/null && echo "✓ MoveIt found" || echo "✗ MoveIt missing"
rospack find gazebo_ros > /dev/null && echo "✓ Gazebo ROS found" || echo "✗ Gazebo ROS missing"
rospack find joint_trajectory_controller > /dev/null && echo "✓ Controllers found" || echo "✗ Controllers missing"

echo "===================================="
echo "Installation complete! Source your workspace:"
echo "source /opt/ros/noetic/setup.bash"
echo "source ~/ROS_Printing_Station/devel/setup.bash"
echo "===================================="