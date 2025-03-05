from tkinter import *
import rospy
from std_msgs.msg import String

class ROSGUI:
    def __init__(self, master):
        self.master = master
        master.geometry('1400x700')

        # Initialize ROS node and subscriber
        rospy.init_node('gui', anonymous=True)
        rospy.Subscriber("/response", String, self.callback)
        self.test_publisher = rospy.Publisher("/chatter", String, queue_size=10)

        self.create_widgets()

    def create_widgets(self):
        self.left_frame = Frame(self.master, bg="#181818")
        self.right_frame = Frame(self.master, bg="#181818")

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid_rowconfigure(2, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(2, weight=1)

        self.left_frame.grid_propagate(False)
        self.right_frame.grid_propagate(False)

        self.ros_label = Label(self.left_frame, text="Hello")
        self.send_button = Button(self.left_frame, text="Send", command=self.publish_on_topic)

        self.entry_frame = Frame(self.left_frame, bg="#181818")
        self.entry_frame.grid_columnconfigure(0, weight=1)
        self.entry_frame.grid_columnconfigure(1, weight=1)
        self.entry_frame.grid_columnconfigure(2, weight=1)

        self.x_entry = Entry(self.entry_frame, width=7, bg="#f54242")
        self.y_entry = Entry(self.entry_frame, width=7, bg="#75f542")
        self.z_entry = Entry(self.entry_frame, width=7, bg="#4278f5")

        self.ros_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.send_button.grid(row=2, column=0, padx=10, pady=10, sticky="sew")
        self.entry_frame.grid(row=1, column=0, sticky="sew")
        self.x_entry.grid(row=0, column=0, sticky="sew", padx=5)
        self.y_entry.grid(row=0, column=1, sticky="sew", padx=5)
        self.z_entry.grid(row=0, column=2, sticky="sew", padx=5)

        self.right_label = Label(self.right_frame, text="Right Side Content")
        self.test_button = Button(self.right_frame, text="Test")
        self.right_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.test_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    def callback(self, msg):
        self.ros_label.config(text=msg.data)

    def publish_on_topic(self):
        self.test_publisher.publish("x: " + self.x_entry.get() + " y: " + self.y_entry.get() + " z: " + self.z_entry.get())
        self.x_entry.delete(0, 'end')
        self.y_entry.delete(0, 'end')
        self.z_entry.delete(0, 'end')

if __name__ == "__main__":
    root = Tk()
    my_gui = ROSGUI(root)
    root.mainloop()