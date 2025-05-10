#!/usr/bin/env python
import sys
import rospy
import moveit_commander
from std_msgs.msg import String

status_pub = rospy.Publisher("response", String, queue_size=10)
error_pub = rospy.Publisher("error", String, queue_size=10)

def chatter_callback(message):
    try:
        #splitting the message in the corresponding tokens
        #might be nice to use different message and not a string 
        tokens = message.data.strip().split()
        if len(tokens) < 6:
            rospy.logwarn("Unexpected message format: %s", message.data)
            return

        q1 = float(tokens[1])
        q2 = float(tokens[3])
        q3 = float(tokens[5])
        rospy.loginfo("Received target joint values: q1=%.2f, q2=%.2f, q3=%.2f", q1, q2, q3)
        joint_goal = move_group.get_current_joint_values()

        joint_goal[0] = q1
        joint_goal[1] = q2
        joint_goal[2] = q3
        
        # WHY DOES GO WORK AND EXECUTE NOT???????
        try:
            move_group.go(joint_goal, wait=True)
        except Exception as e:
             status_pub.publish("red")
             error_pub.publish(str(e))
        move_group.stop()

        rospy.loginfo("Motion executed successfully.")

    except Exception as e:
        rospy.logerr("Error in processing message: %s", e)

if __name__ == '__main__':

    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('moveit_scara_controller', anonymous=True)
    
    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()

    group_name = "scara"
    move_group = moveit_commander.MoveGroupCommander(group_name)

    rospy.loginfo("SCARA MoveIt controller initialized and waiting for joint commands on /chatter.")

    # Subscribe to the gui
    # on callback we start the movement
    rospy.Subscriber("/chatter", String, chatter_callback)
    rospy.spin()

    moveit_commander.roscpp_shutdown()
