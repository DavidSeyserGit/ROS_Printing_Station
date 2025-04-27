import rospy
import rospkg
from gazebo_msgs.srv import SpawnModel
from geometry_msgs.msg import Pose

from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Pose, Twist


#!/usr/bin/env python


def spawn_urdf_model():
    rospy.init_node('spawn_morobot', anonymous=True)

    # Get the path to the URDF file
    rospack = rospkg.RosPack()
    urdf_path = 'src/printing_station/urdf/morobot.sdf'

    # Read the URDF file
    with open(urdf_path, 'r') as urdf_file:
        urdf_content = urdf_file.read()

    # Define the initial pose of the robot
    initial_pose = Pose()
    initial_pose.position.x = -0.1
    initial_pose.position.y = 0
    initial_pose.position.z = 3.0
    initial_pose.orientation.x = 0.0
    initial_pose.orientation.y = 0.0
    initial_pose.orientation.z = 0.0
    initial_pose.orientation.w = 1.0

    # Wait for the spawn_model service to be available
    rospy.wait_for_service('/gazebo/spawn_urdf_model')
    try:
        spawn_model = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        spawn_model(model_name='morobot', model_xml=urdf_content, robot_namespace='', initial_pose=initial_pose, reference_frame='world')
        rospy.loginfo("URDF model spawned successfully!")
    except rospy.ServiceException as e:
        rospy.logerr(f"Failed to spawn URDF model: {e}")

def move_model(x,y,z):
    # Wait for the set_model_state service to be available
    rospy.wait_for_service("/gazebo/set_model_state")
    try:
        set_state = rospy.ServiceProxy("/gazebo/set_model_state", SetModelState)

        # Define the new pose for the model
        new_pose = Pose()
        new_pose.position.x = x  # Specify your desired x position
        new_pose.position.y = y  # Specify your desired y position
        new_pose.position.z = z  # Keep z appropriate as needed

        new_pose.orientation.x = -0.4
        new_pose.orientation.y = 1
        new_pose.orientation.z = 0.0
        new_pose.orientation.w = 1.0

        # Optionally, define twist (velocity) if needed
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0

        # Prepare the ModelState message
        state_msg = ModelState()
        state_msg.model_name = "morobot"  # Ensure the name matches your spawned model's name
        state_msg.pose = new_pose
        state_msg.twist = twist
        state_msg.reference_frame = "world"  # or any other reference frame appropriate for your setup

        # Call the service to update the model's state
        resp = set_state(state_msg)
        if resp.success:
            rospy.loginfo("Model moved successfully!")
        else:
            rospy.logerr("Failed to move the model. Service response: %s", resp.status_message)
    except rospy.ServiceException as e:
        rospy.logerr("Service call failed: %s", e)

if __name__ == '__main__':
    try:
        #spawn_urdf_model()
        move_model(-0.3,2,1)
    except rospy.ROSInterruptException:
        pass