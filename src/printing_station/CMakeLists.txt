# %Tag(FULLTEXT)%
cmake_minimum_required(VERSION 3.0)
project(printing_station)

## Find catkin and any catkin packages
find_package(catkin REQUIRED COMPONENTS roscpp rospy std_msgs genmsg)

## Declare a catkin package
catkin_package()

## Build talker and listener
include_directories(include ${catkin_INCLUDE_DIRS})



# %EndTag(FULLTEXT)%