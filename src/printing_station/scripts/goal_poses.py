#!/usr/bin/env python
"""
SCARA Robot Pick and Place Simulation.

This script loads waypoints from a JSON file and executes a
simulated pick and place operation with a SCARA robot.
"""

import os
import sys
import json
import time
import rospy
import moveit_commander


def main():
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('scara_pick_place_simulation')
    
    # Setup move group
    move_group = moveit_commander.MoveGroupCommander("scara")
    
    # Set motion parameters for smooth movement
    move_group.set_max_velocity_scaling_factor(0.3)
    move_group.set_max_acceleration_scaling_factor(0.3)
    
    def move_to_position(q1, q2, q3):
        joint_goal = move_group.get_current_joint_values()
        joint_goal[0] = q1   # Joint 1 position
        joint_goal[1] = q2   # Joint 2 position
        joint_goal[2] = q3   # Joint 3 position
        move_group.set_joint_value_target(joint_goal)
        success = move_group.go(wait=True)
        move_group.stop()
        return success
    
    def print_current_pose():
        """Print the current Cartesian pose of the robot's end effector."""
        current_pose = move_group.get_current_pose().pose
        print("\nTCP Cartesian Pose:")
        print("Position (x,y,z):", [
            current_pose.position.x, 
            current_pose.position.y, 
            current_pose.position.z
        ])
    
    # Load waypoints from external file
    waypoints_file = 'src/printing_station/waypoints/scara_wp.json'
    
    try:
        with open(waypoints_file, 'r') as f:
            waypoints = json.load(f)
        print(f"Successfully loaded {len(waypoints)} waypoints from {waypoints_file}")
    except FileNotFoundError:
        rospy.logerr(f"Waypoints file not found: {waypoints_file}")
        return
    except json.JSONDecodeError:
        rospy.logerr(f"Invalid JSON format in waypoints file: {waypoints_file}")
        return
    except Exception as e:
        rospy.logerr(f"Error loading waypoints file: {e}")
        return
    
    # Execute each waypoint in sequence
    for i, waypoint in enumerate(waypoints):
        try:
            # Extract waypoint data
            description = waypoint['description']
            position = waypoint['position']
            pause_time = waypoint.get('pause', 0)
            action = waypoint.get('action')
            
            # Move to the waypoint position
            rospy.loginfo(f"\n{i+1}. {description}...")
            q1, q2, q3 = position
            success = move_to_position(q1, q2, q3)
            
            if success:
                rospy.loginfo(f"Successfully {description.lower()}")
                print_current_pose()
            else:
                rospy.logerr(f"Failed to {description.lower()}")
                return
            
            # Print any associated action message
            if action:
                rospy.loginfo(f"\n{action}")
            
            # Pause if specified
            if pause_time > 0:
                time.sleep(pause_time)
                
        except KeyError as e:
            rospy.logerr(f"Missing required key in waypoint {i+1}: {e}")
            return
        except Exception as e:
            rospy.logerr(f"Error processing waypoint {i+1}: {e}")
            return
    
    rospy.loginfo("\nSimulated pick and place operation complete!")


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        rospy.loginfo("Program interrupted before completion")
    except Exception as e:
        rospy.logerr(f"Unexpected error: {e}")
