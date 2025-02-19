#!/bin/bash

# Function to clean up background processes
cleanup() {
    echo "Stopping processes..."
    kill $ROSLAUNCH_PID
    kill $GUI_PID
    exit 0
}

# Trap the EXIT signal to ensure cleanup is called
trap cleanup EXIT

roslaunch printing_station station.launch &
ROSLAUNCH_PID=$!

# Check if PROJECT_ROOT is already set in the environment
if [[ -z "$PROJECT_ROOT" ]]; then
    echo "Error: PROJECT_ROOT environment variable not set."
    echo "Please set PROJECT_ROOT to the absolute path of your project."
    exit 1
fi

EXECUTABLE_PATH=$(realpath "$PROJECT_ROOT/external/3D-Printing-Station-GUI/target/debug/")

cd "$EXECUTABLE_PATH"
./GUI-3D-Printing-Station &
GUI_PID=$!

# Wait for background processes to finish
wait $ROSLAUNCH_PID
wait $GUI_PID
