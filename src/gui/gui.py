from tkinter import *
import rospy
from std_msgs.msg import String

def callback(msg):
    ros_label.config(text=msg.data)

def publish_on_topic():
    """
    @brief Publishes coordinates on a ROS topic and clears the input fields.
    
    This function retrieves the values from the x_entry, y_entry, and z_entry input fields,
    concatenates them into a single string in the format "x: <value> y: <value> z: <value>",
    and publishes this string on a predefined ROS topic using the test_publisher. After publishing,
    it clears the input fields.
    
    @param None
    
    @return None
    """
    test_publisher.publish("x: " + x_entry.get() + " y: " + y_entry.get() + " z: " + z_entry.get())
    x_entry.delete(0, 'end')
    y_entry.delete(0, 'end')
    z_entry.delete(0, 'end')

# Initialize the ROS node and subscriber
rospy.init_node('gui', anonymous=True)
rospy.Subscriber("/response", String, callback)
test_publisher = rospy.Publisher("/chatter", String, queue_size=10)

# Initialize the Tkinter GUI
gui = Tk()
gui.geometry('1400x700')

left_frame = Frame(gui)
right_frame = Frame(gui)

gui.grid_columnconfigure(0, weight=1)
gui.grid_columnconfigure(1, weight=1)
gui.grid_rowconfigure(0, weight=1)

left_frame = Frame(gui, bg="#181818")
right_frame = Frame(gui, bg="#181818")

left_frame.grid(row=0, column=0, sticky="nsew")
right_frame.grid(row=0, column=1, sticky="nsew")

# Configure rows and columns within the frames for even distribution
left_frame.grid_rowconfigure(0, weight=1)  # Label
left_frame.grid_rowconfigure(1, weight=1)  # Button
left_frame.grid_rowconfigure(2, weight=1)  # Entries Row
left_frame.grid_columnconfigure(0, weight=1) # All columns in left frame

right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_columnconfigure(0, weight=1)
right_frame.grid_columnconfigure(1, weight=1)
right_frame.grid_columnconfigure(2, weight=1)

left_frame.grid_propagate(False)
right_frame.grid_propagate(False)

#LEFT SIDE

ros_label = Label(left_frame, text="Hello")
send_button = Button(left_frame, text="Send", command=publish_on_topic)

# Use a separate frame for the entry widgets to manage their layout
entry_frame = Frame(left_frame, bg="#181818")
entry_frame.grid_columnconfigure(0, weight=1) # Distribute space in entry frame
entry_frame.grid_columnconfigure(1, weight=1)
entry_frame.grid_columnconfigure(2, weight=1)

x_entry = Entry(entry_frame, width=7, bg="#f54242")
y_entry = Entry(entry_frame, width=7, bg="#75f542")
z_entry = Entry(entry_frame, width=7, bg="#4278f5")


ros_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
send_button.grid(row=2, column=0, padx=10, pady=10, sticky="sew")
entry_frame.grid(row=1, column=0, sticky="sew")  # Span full width of left_frame
x_entry.grid(row=0, column=0, sticky="sew", padx=5)  # sticky="ew" to expand horizontally
y_entry.grid(row=0, column=1, sticky="sew", padx=5)
z_entry.grid(row=0, column=2, sticky="sew", padx=5)

#RIGHT SIDE

right_label = Label(right_frame, text="Right Side Content")
test_button = Button(right_frame, text="Test")
right_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
test_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")


gui.mainloop()