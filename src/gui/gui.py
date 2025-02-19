from tkinter import *
import rospy
from std_msgs.msg import String 

# Callback function to update the label text
def callback(msg):
    ros_label.config(text=msg.data)  # Update the label text with the received message

# Initialize the ROS node and subscriber
rospy.init_node('listener', anonymous=True) 
rospy.Subscriber("/response", String, callback) 

# Initialize the Tkinter GUI
gui = Tk()
gui.geometry('1440x800')
ros_label = Label(gui, text='Hello World')
ros_label.pack(side=BOTTOM, pady=10)  # Make sure to pack the label so it appears in the window

# Start the Tkinter main loop
gui.mainloop()