#!/usr/bin/env python
import os
import sys
import json
import time
import threading
import rospy
import moveit_commander


class RobotMove:
    def __init__(self, robot_name, move_group_name, waypoints_file):
        """
        Initialize the robot with a given namespace/robot name, move group name, and the
        path to the waypoints JSON file.
        """
        self.robot_name = robot_name
        self.move_group_name = move_group_name
        self.waypoints_file = waypoints_file

        # Initialize moveit_commander and ROS node if not already initialized.
        # Note: If using multiple robots, ensure each has a unique node name.
        if not rospy.core.is_initialized():
            rospy.init_node(f"{robot_name}_controller", anonymous=True)

        moveit_commander.roscpp_initialize(sys.argv)

        # Setup move group for this robot.
        self.move_group = moveit_commander.MoveGroupCommander(self.move_group_name)
        self.move_group.set_max_velocity_scaling_factor(0.3)
        self.move_group.set_max_acceleration_scaling_factor(0.3)

        # Load waypoints upon initialization.
        self.waypoints = self.load_waypoints(self.waypoints_file)

    def load_waypoints(self, file_path):
        """
        Load the waypoint data from a JSON file.
        """
        try:
            with open(file_path, "r") as f:
                waypoints = json.load(f)
            rospy.loginfo(
                f"Successfully loaded {len(waypoints)} waypoints from {file_path}"
            )
            return waypoints
        except FileNotFoundError:
            rospy.logerr(f"Waypoints file not found: {file_path}")
            return []
        except json.JSONDecodeError:
            rospy.logerr(f"Invalid JSON format in waypoints file: {file_path}")
            return []
        except Exception as e:
            rospy.logerr(f"Error loading waypoints file: {e}")
            return []

    def move_to_position(self, joint_positions):
        """
        Move the robot's joints to the specified positions.
        Expects joint_positions as a list, whose length should match the number of joints
        for the robot.
        
        Returns True if movement is successful.
        """
        current_joints = self.move_group.get_current_joint_values()
        if len(joint_positions) != len(current_joints):
            rospy.logerr(
                f"Expected {len(current_joints)} joint values, but got "
                f"{len(joint_positions)}"
            )
            return False

        joint_goal = current_joints[:]  # Make a copy
        for i, pos in enumerate(joint_positions):
            joint_goal[i] = pos

        self.move_group.set_joint_value_target(joint_goal)
        success = self.move_group.go(wait=True)
        self.move_group.stop()
        return success

    def print_current_pose(self):
        """
        Print the current Cartesian pose of the robot's end effector.
        """
        current_pose = self.move_group.get_current_pose().pose
        rospy.loginfo("\nTCP Cartesian Pose:")
        rospy.loginfo(
            f"Position (x, y, z): [{current_pose.position.x}, "
            f"{current_pose.position.y}, {current_pose.position.z}]"
        )

    def execute_waypoints(self):
        """
        Execute the set of waypoints loaded from the JSON file.
        Expected JSON structure for each waypoint:
        {
            "description": "some action description",
            "position": [p1, p2, ... , pN],  # list matching the number of joints,
            "pause": seconds,                # optional,
            "action": "action message"         # optional
        }
        """
        if not self.waypoints:
            rospy.logerr("No waypoints loaded!")
            return

        for i, waypoint in enumerate(self.waypoints):
            try:
                description = waypoint["description"]
                joint_positions = waypoint["position"]
                pause_time = waypoint.get("pause", 0)
                action = waypoint.get("action")

                rospy.loginfo(f"\n{i+1}. {description}...")
                success = self.move_to_position(joint_positions)
                if success:
                    rospy.loginfo(f"Successfully {description.lower()}")
                    self.print_current_pose()
                else:
                    rospy.logerr(f"Failed to {description.lower()}")
                    return

                if action:
                    rospy.loginfo(f"\n{action}")

                if pause_time > 0:
                    time.sleep(pause_time)

            except KeyError as e:
                rospy.logerr(f"Missing required key in waypoint {i+1}: {e}")
                return
            except Exception as e:
                rospy.logerr(f"Error processing waypoint {i+1}: {e}")
                return

        rospy.loginfo("\nSimulated pick and place operation complete!")


def run_robot(robot):
    """Helper function to run a robot's waypoint execution."""
    robot.execute_waypoints()