#!/usr/bin/env python
import rospy
import moveit_commander
from geometry_msgs.msg import Pose
from gazebo_msgs.srv import SpawnModel, SpawnModelRequest, DeleteModel
from moveit_commander import PlanningSceneInterface
from moveit_msgs.msg import AttachedCollisionObject
from gazebo_msgs.msg import ContactsState
from RobotMover import RobotMove, run_robot
import random

traget_pose_1 = [-1, 3, 1.7 , 0, 0, 0, 1]
traget_pose_2 = [ 0.3, 3, 1.7 , 0, 0, 0, 1]
traget_pose_3 = [ 0.3, 2.5, 1.7, 0, 0, 0, 1]
traget_pose_4 = [ -1, 2.5, 1.7, 0, 0, 0, 1]
traget_pose_5 = [-0.5, 3.5, 1.7, 0, 0, 0, 1]
drop_off = [-0.4, 2.2, 0.9, 0, -0.707, 0, 0.707]  # Quaternion for z-axis pointing to -y (doesnt work for what ever reason)

target_index = random.randint(1, 5)

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
    print (target_index)
    rospy.init_node("gazebo_moveit_waypoints", anonymous=True)
    moveit_commander.roscpp_initialize([])
    # Initialize planning scene
    planning_scene = PlanningSceneInterface()


    # Spawn the object at one of the target locations randomly
    model_file = "src/printing_station/urdf/morobot.sdf"
    model_name = "object_model"
    target_pose = Pose()
    selected_target_pose = globals()[f"traget_pose_{target_index}"]

    # Assign the selected target pose to the spawn position
    target_pose.position.x = selected_target_pose[0]
    target_pose.position.y = selected_target_pose[1]
    target_pose.position.z = selected_target_pose[2]-0.5
    target_pose.orientation.w = 1

    try:
        spawn_success = spawn_object(model_file, model_name, target_pose)
    except:
        pass
    
    #need to have 5 targets where i can move to
    rospy.sleep(1.0)
    try:
        move_group = moveit_commander.MoveGroupCommander("knick")
        move_group.set_planning_time(5.0) # Increase planning time if needed
        
        #i have to move to the position and then move to the drop off location
        move_group.set_pose_target(selected_target_pose)
        plan_result = move_group.plan()
        success = plan_result[0]
        plan = plan_result[1]
        
        if success:
                move_group.execute(plan, wait=True)
        
        else:
            rospy.logerr(f"Failed to plan motion.")
            
        #i have to move to the position and then move to the drop off location
        move_group.set_pose_target(drop_off)
        plan_result = move_group.plan()
        success = plan_result[0]
        plan = plan_result[1]
        
        if success:
                move_group.execute(plan, wait=True)
        
        else:
            rospy.logerr(f"Failed to plan motion.")

        scara_waypoints_file = "src/printing_station/waypoints/scara_wp.json"
        scara_robot = RobotMove(
            robot_name="scara",
            move_group_name="scara",
            waypoints_file=scara_waypoints_file,
        )

        # Run the robot motion in the main thread since we don't need to do anything else
        run_robot(scara_robot)

        try:
            delete_model = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
            delete_model(model_name)
            rospy.loginfo(f"Successfully despawned {model_name}.")
        except rospy.ServiceException as e:
            rospy.logerr(f"Service call to delete model failed: {e}")


    except Exception as e:
        rospy.logerr(f"Error in MoveGroup execution or planning: {e}")
        # If an exception occurs, ensure MoveIt commander is shut down
        moveit_commander.roscpp_shutdown()
        
if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        rospy.loginfo("Program interrupted before completion")
    except Exception as e:
        rospy.logerr(f"Unexpected error: {e}")
    finally:
        moveit_commander.roscpp_shutdown()

    """
    """