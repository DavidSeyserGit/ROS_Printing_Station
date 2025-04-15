#!/usr/bin/env python
import rospy
import moveit_commander
import sys
from math import pi

def main():
    # Initialize
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('joint_goal_sender')
    
    # Setup move group
    move_group = moveit_commander.MoveGroupCommander("knick")
    
    # Set target joint values (in radians)
    joint_goal = move_group.get_current_joint_values()
    joint_goal[0] = 0.0    # Joint 1 position
    joint_goal[1] = 3.14/4  # Joint 2 position (45 degrees down)
    joint_goal[2] = 0.0     # Joint 3 position
    joint_goal[3] = 0.0
    joint_goal[4] = 0.0
    joint_goal[5] = 0.0
    # Add more joints as needed
    
    # Move to target
    print("\nMoving to joint goal...")
    move_group.set_joint_value_target(joint_goal)
    success = move_group.go(wait=True)
    
    current_pose = move_group.get_current_pose().pose
    print("\nTCP Cartesian Pose:")
    print("Position (x,y,z):", [current_pose.position.x, 
                            current_pose.position.y, 
                            current_pose.position.z])
    print("Orientation (x,y,z,w):", [current_pose.orientation.x,
                                current_pose.orientation.y,
                                current_pose.orientation.z,
                                current_pose.orientation.w])
                                
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass