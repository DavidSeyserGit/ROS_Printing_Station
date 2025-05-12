#!/usr/bin/env python
import sys
import rospy
import moveit_commander
import geometry_msgs.msg
from std_msgs.msg import String

status_pub = rospy.Publisher("response", String, queue_size=10)
error_pub = rospy.Publisher("error", String, queue_size=10)

def chatter_callback(message):
    try:
        # Splitting the message into tokens
        tokens = message.data.strip().split()
        if len(tokens) < 6:
            rospy.logwarn("Unexpected message format: %s", message.data)
            return

        # Parse Cartesian coordinates from the message
        # These coordinates are in the robot's base frame
        x = float(tokens[1])
        y = float(tokens[3])
        z = float(tokens[5])
        rospy.loginfo("Received target position in base frame: x=%.2f, y=%.2f, z=%.2f", x, y, z)
        
        # Create a pose goal in the robot's base frame
        pose_goal = geometry_msgs.msg.Pose()
        pose_goal.position.x = x
        pose_goal.position.y = y
        pose_goal.position.z = z
        
        move_group.set_position_target([x, y, z])
        
        # Plan and execute
        try:
            plan = move_group.plan()
            
            if isinstance(plan, tuple):
                success = plan[0]
                trajectory = plan[1]
            else:
                pass
            
            if success:
                move_group.execute(trajectory, wait=True)
                rospy.loginfo("Motion executed successfully.")
                status_pub.publish("green")
            else:
                rospy.logerr("Planning failed")
                status_pub.publish("red")
                error_pub.publish("Planning failed")
        except Exception as e:
            status_pub.publish("red")
            error_pub.publish(str(e))
            rospy.logerr("Error during execution: %s", e)
        
        move_group.stop()

    except Exception as e:
        rospy.logerr("Error in processing message: %s", e)
        status_pub.publish("red")
        error_pub.publish(str(e))

if __name__ == '__main__':
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('moveit_knick_controller', anonymous=True)
    
    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()

    group_name = "knick"
    move_group = moveit_commander.MoveGroupCommander(group_name)

    rospy.loginfo("Knick MoveIt controller initialized and waiting for position commands on /chatter.")

    # Subscribe to the gui
    rospy.Subscriber("/chatter", String, chatter_callback)
    rospy.spin()
    # Clean up
    move_group.stop()
    move_group.clear_pose_targets()
    move_group.clear_path_constraints()
    moveit_commander.roscpp_shutdown()
