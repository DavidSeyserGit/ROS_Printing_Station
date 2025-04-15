#!/usr/bin/env python
import rospy
import moveit_commander
import sys

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
    # Add more joints as needed
    
    # Move to target
    move_group.set_joint_value_target(joint_goal)
    success = move_group.go(wait=True)
    
    if success:
        rospy.loginfo("Joint movement successful")
    else:
        rospy.logwarn("Joint movement failed")

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass