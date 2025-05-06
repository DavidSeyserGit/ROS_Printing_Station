from tkinter import *
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from PIL import Image as PIL_Image
from PIL import ImageTk
import cv2
from cv_bridge import CvBridge
import threading
from pick_and_place import main as robot_main

class ROSGUI:
    def __init__(self, master):
        self.master = master
        master.geometry('1000x700')

        # Initialize ROS node (if not already initialized)
        rospy.init_node('gui', anonymous=True)

        rospy.Subscriber("/response", String, self.callback)
        rospy.Subscriber("/image_raw", Image, self.image_callback)
        self.test_publisher = rospy.Publisher("/chatter", String, queue_size=10)
        self.bridge = CvBridge()
        self.tk_image = None

        self.create_widgets()

    def create_widgets(self):
        self.left_frame = Frame(self.master, bg="#181818")
        self.image_frame = Frame(self.master, bg="#333333")

        # Create layout
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.image_frame.grid(row=0, column=1, sticky="nsew")

        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid_rowconfigure(2, weight=1)
        self.left_frame.grid_rowconfigure(3, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        self.image_frame.grid_rowconfigure(0, weight=1)
        self.image_frame.grid_columnconfigure(0, weight=1)

        self.left_frame.grid_propagate(False)
        self.image_frame.grid_propagate(False)

        # Status label
        self.ros_label = Label(self.left_frame, text="Hello", bg="#181818", fg="white")
        self.ros_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # "Start" button (calls external robot routine)
        self.start_button = Button(self.left_frame, text="Start", command=self.start_robot)
        self.start_button.grid(row=1, column=0, padx=10, pady=10, sticky="sew")

        # Entry frame and "Send" button for joint commands 
        self.entry_frame = Frame(self.left_frame, bg="#181818")
        self.entry_frame.grid(row=2, column=0, sticky="nsew")
        self.entry_frame.grid_columnconfigure(0, weight=1)
        self.entry_frame.grid_columnconfigure(1, weight=1)
        self.entry_frame.grid_columnconfigure(2, weight=1)

        self.x_entry = Entry(self.entry_frame, width=7, bg="#f54242")
        self.y_entry = Entry(self.entry_frame, width=7, bg="#75f542")
        self.z_entry = Entry(self.entry_frame, width=7, bg="#4278f5")
        self.x_entry.grid(row=0, column=0, sticky="sew", padx=5)
        self.y_entry.grid(row=0, column=1, sticky="sew", padx=5)
        self.z_entry.grid(row=0, column=2, sticky="sew", padx=5)

        self.send_button = Button(self.left_frame, text="Send", command=self.publish_on_topic)
        self.send_button.grid(row=3, column=0, padx=10, pady=10, sticky="sew")

        # Image display
        self.image_label = Label(self.image_frame)
        self.image_label.grid(row=0, column=0, sticky="nsew")

    def callback(self, msg):
        # Update the status label
        self.ros_label.config(text=msg.data)

    def publish_on_topic(self):
        # Publish joint commands on /chatter as a formatted string
        command = (
            "q1: " + self.x_entry.get() +
            " q2: " + self.y_entry.get() +
            " q3: " + self.z_entry.get()
        )
        self.test_publisher.publish(command)
        self.x_entry.delete(0, 'end')
        self.y_entry.delete(0, 'end')
        self.z_entry.delete(0, 'end')

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            # Convert from BGR to RGB for display
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            img = PIL_Image.fromarray(cv_image)
            img = ImageTk.PhotoImage(image=img)
            self.image_label.configure(image=img)
            self.tk_image = img  # Keep a reference to avoid garbage collection
        except Exception as e:
            print(f"Error converting image: {e}")

    def start_robot(self):
        # Run the external routine on a separate thread to avoid blocking the GUI.
        threading.Thread(target=self.run_robot_routine).start()

    def run_robot_routine(self):
        try:
            robot_main()  # Call the external routine
        except Exception as e:
            rospy.logerr("Error running external robot routine: %s", e)

if __name__ == "__main__":
    root = Tk()
    gui = ROSGUI(root)
    root.mainloop()