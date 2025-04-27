#!/usr/bin/env python
import threading
import rospy
import moveit_commander
from geometry_msgs.msg import Pose
from gazebo_msgs.srv import SpawnModel, SpawnModelRequest
from RobotMover import RobotMove, run_robot


def spawn_object(model_path, model_name, initial_pose):
    """
    Spawns an object into Gazebo using its SDF model.
    """
    rospy.loginfo("Waiting for gazebo spawn service...")
    rospy.wait_for_service('/gazebo/spawn_sdf_model')
    try:
        spawn_model = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        with open(model_path, "r") as file:
            model_xml = file.read()

        req = SpawnModelRequest()
        req.model_name = model_name
        req.model_xml = model_xml
        req.initial_pose = initial_pose
        req.reference_frame = "world"

        rospy.loginfo(f"Spawning {model_name} at position: {initial_pose.position}")
        response = spawn_model(req.model_name, req.model_xml, "", 
                               req.initial_pose, req.reference_frame)
        if response.success:
            rospy.loginfo(f"Successfully spawned {model_name}.")
            return True
        else:
            rospy.logerr(f"Failed to spawn {model_name}: {response.status_message}")
            return False
    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")
        return False


def main():
    rospy.init_node("gazebo_moveit_waypoints", anonymous=True)
    moveit_commander.roscpp_initialize([])
    
    # 1. Spawn the object in Gazebo
    model_file = "src/printing_station/urdf/morobot.sdf"
    model_name = "object_model"
    target_pose = Pose()
    target_pose.position.x = -0.3
    target_pose.position.y = 0.65
    target_pose.position.z = 0.5
    target_pose.orientation.w = 1.0

    spawn_success = spawn_object(model_file, model_name, target_pose)
    
    rospy.sleep(1.0)  # Short pause to ensure model is fully loaded

    # 2. Use RobotMover to handle robot motion
    try:
        scara_waypoints_file = "src/printing_station/waypoints/scara_wp.json"
        scara_robot = RobotMove(
            robot_name="scara",
            move_group_name="scara",
            waypoints_file=scara_waypoints_file,
        )

        # Run the robot motion in the main thread since we don't need to do anything else
        run_robot(scara_robot)
        
        rospy.loginfo("Completed executing waypoint motions.")
    except Exception as e:
        rospy.logerr(f"Error in RobotMover execution: {e}")


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        rospy.loginfo("Program interrupted before completion")
    except Exception as e:
        rospy.logerr(f"Unexpected error: {e}")
    finally:
        moveit_commander.roscpp_shutdown()
