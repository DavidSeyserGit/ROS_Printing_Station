#!/bin/bash

roslaunch printing_station station.launch &

sleep 5

# Navigate to the external directory
cd ../../external/3D-Printing-Station-GUI/target/debug

./GUI-3D-Printing-Station &
