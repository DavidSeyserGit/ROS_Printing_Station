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
from std_msgs.msg import String

pub = rospy.Publisher("response", String, queue_size=10)

traget_pose_1 = [-1, 3, 1.7 , 0, 0, 0, 1]
traget_pose_2 = [ 0.3, 3, 1.7 , 0, 0, 0, 1]
traget_pose_3 = [ 0.3, 2.5, 1.7, 0, 0, 0, 1]
traget_pose_4 = [ -1, 2.5, 1.7, 0, 0, 0, 1]
traget_pose_5 = [-0.5, 3.5, 1.7, 0, 0, 0, 1]
drop_off_pose = [-0.4, 2.2, 0.9, 0, -0.707, 0, 0.707] # Renamed for clarity

# Define joint targets for the 'knick' arm corresponding to each traget_pose
joint_target_1 = [-0.6, -0.57, -0.415, -1.25, 0.565, -0.631] 
joint_target_2 = [-2.8, -0.2, -0.93, -0.53, 0.17, -1.5] 
joint_target_3 = [2.75, -0.395, -0.66, -0.227, 0.126, 0] 
joint_target_4 = [0.87, -0.43, -0.64, 0.872, 0.577, 0.857] 
joint_target_5 = [-1.248, -0.142, -0.711, 0.8533, -0.16, 1.582] 

# Joint target for the drop off position
joint_target_drop_off = [1.4, -0.756, -0.954, -0.269, 0.735, -0.608] # Example joint values for drop off pose


#spawning the placeholder object 
def spawn_object(model_path, model_name, initial_pose):
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
    pub.publish("yellow")
    target_index = random.randint(1, 5)
    print (f"Target index chosen: {target_index}")
    #rospy.init_node("gazebo_moveit_waypoints", anonymous=True)
    moveit_commander.roscpp_initialize([])

    # Spawn the object at one of the target locations randomly
    model_file = "src/printing_station/urdf/morobot.sdf"
    model_name = "object_model"
    initial_object_pose = Pose() # Renamed for clarity
    selected_traget_pose = globals()[f"traget_pose_{target_index}"]

    # Assign the selected target pose to the spawn position
    initial_object_pose.position.x = selected_traget_pose[0]
    initial_object_pose.position.y = selected_traget_pose[1]
    initial_object_pose.position.z = selected_traget_pose[2]-0.5
    initial_object_pose.orientation.w = 1

    try:
        spawn_success = spawn_object(model_file, model_name, initial_object_pose)
        if not spawn_success:
             rospy.logwarn("Object spawning failed, continuing without object.")
    except Exception as e:
        rospy.logerr(f"Error during object spawning: {e}")
        rospy.logwarn("Continuing without object due to spawning error.")


    rospy.sleep(1.0)
    try:
        move_group = moveit_commander.MoveGroupCommander("knick")
        move_group.set_planning_time(10.0) # Increased planning time
        move_group.set_num_planning_attempts(5) # Increased planning attempts


        # Select the corresponding joint target based on the randomly chosen target_index
        selected_joint_target = globals()[f"joint_target_{target_index}"]

        # Set joint target for the pick-up position
        rospy.loginfo(f"Moving 'knick' arm to joint target for traget_pose_{target_index}")
        move_group.set_joint_value_target(selected_joint_target)
        plan_result = move_group.plan()
        success = plan_result[0]
        plan = plan_result[1]

        if success:
            rospy.loginfo("Planning successful, executing motion.")
            move_group.execute(plan, wait=True)
            rospy.loginfo("'knick' arm reached the pick-up position.")
        else:
            rospy.logerr(f"Failed to plan motion to joint target for traget_pose_{target_index}.")
            pub.publish("red")


        rospy.loginfo("Moving 'knick' arm to joint target for drop off position.")
        move_group.set_joint_value_target(joint_target_drop_off)
        plan_result = move_group.plan()
        success = plan_result[0]
        plan = plan_result[1]

        if success:
            rospy.loginfo("Planning successful, executing motion.")
            move_group.execute(plan, wait=True)
            rospy.loginfo("'knick' arm reached the drop off position.")
        else:
            rospy.logerr(f"Failed to plan motion to joint target for drop off position.")
            pub.publish("red")

        # Determine which waypoints file to use based on the random target index
        if target_index % 2 == 0:
            scara_waypoints_file = "/home/david/ROS_Printing_Station/src/printing_station/waypoints/scara_wp.json"
        else:
            scara_waypoints_file = "/home/david/ROS_Printing_Station/src/printing_station/waypoints/scara_wp2.json"

        # Initialize the scara robot with the selected waypoints file
        scara_robot = RobotMove(
            robot_name="scara",
            move_group_name="scara",
            waypoints_file=scara_waypoints_file,
        )

        run_robot(scara_robot)


        try:
            # Only attempt to delete the model if spawning was successful
            if 'spawn_success' in locals() and spawn_success:
                delete_model = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
                delete_model(model_name)
                rospy.loginfo(f"Successfully despawned {model_name}.")
        except rospy.ServiceException as e:
            rospy.logerr(f"Service call to delete model failed: {e}")
            pub.publish("red")


    except Exception as e:
        rospy.logerr(f"Error in MoveGroup execution or planning: {e}")
        pub.publish("red")
        moveit_commander.roscpp_shutdown()
    pub.publish("green")
if __name__ == "__main__":
    pub = rospy.Publisher("response", String, queue_size=10)
    try:
        main()
    except rospy.ROSInterruptException:
        rospy.loginfo("Program interrupted before completion")
    except Exception as e:
        rospy.logerr(f"Unexpected error: {e}")
    finally:
        moveit_commander.roscpp_shutdown()
