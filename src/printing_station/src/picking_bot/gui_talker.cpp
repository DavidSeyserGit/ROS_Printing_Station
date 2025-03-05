#include "ros/ros.h"
#include "std_msgs/String.h"
#include <random>
#include <chrono> // For time-related functions
#include <thread> // For sleep

int main(int argc, char **argv)
{
    ros::init(argc, argv, "gui_talker");
    ros::NodeHandle n;

    ros::Publisher status_pub = n.advertise<std_msgs::String>("/response", 1000);

    ros::Rate loop_rate(10); // You can keep this for other parts of your loop if needed

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> distrib(1, 3);

    while (ros::ok())
    {
        std_msgs::String status_msg;
        int random_status = distrib(gen);

        if (random_status == 1) {
            status_msg.data = "green";
        } else if (random_status == 2) {
            status_msg.data = "red";
        } else { // 3
            status_msg.data = "yellow";
        }

        ROS_INFO("Robot Status: %s", status_msg.data.c_str());
        status_pub.publish(status_msg);

        ros::spinOnce();

        // Wait for 3 seconds
        std::this_thread::sleep_for(std::chrono::seconds(3));  // Key change

        // If you still need other things to happen at loop_rate, keep this,
        // otherwise remove it since the sleep handles the timing:
        // loop_rate.sleep(); 
    }

    return 0;
}