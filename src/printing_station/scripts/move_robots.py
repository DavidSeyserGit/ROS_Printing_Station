from RobotMover import RobotMove
from RobotMover import run_robot
import threading
import rospy


def main():
    # Initialize the SCARA robot (3 joints, for example).
    scara_waypoints_file = "src/printing_station/waypoints/scara_wp.json"
    scara_robot = RobotMove(
        robot_name="scara",
        move_group_name="scara",
        waypoints_file=scara_waypoints_file,
    )
    
    scara_waypoints_file = "src/printing_station/waypoints/scara_wp.json"
    scara_robot = RobotMove(
        robot_name="scara",
        move_group_name="scara",
        waypoints_file=scara_waypoints_file,
    )

    # Create threads for parallel execution.
    scara_thread = threading.Thread(target=run_robot, args=(scara_robot,))

    # Start both threads.
    scara_thread.start()

    # Wait for threads to complete.
    scara_thread.join()

    rospy.loginfo("Both robot operations have completed.")


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        rospy.loginfo("Program interrupted before completion")
    except Exception as e:
        rospy.logerr(f"Unexpected error: {e}")
