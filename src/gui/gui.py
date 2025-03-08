from tkinter import *
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from PIL import Image as PIL_Image
from PIL import ImageTk
import cv2
from cv_bridge import CvBridge

class ROSGUI:
    def __init__(self, master):
        self.master = master
        master.geometry('1000x700')  # Adjust width

        # Initialize ROS node and subscriber
        rospy.init_node('gui', anonymous=True)
        rospy.Subscriber("/response", String, self.callback)
        rospy.Subscriber("/image_raw", Image, self.image_callback)
        self.test_publisher = rospy.Publisher("/chatter", String, queue_size=10)
        self.bridge = CvBridge()
        self.tk_image = None

        self.create_widgets()

    def create_widgets(self):
        self.left_frame = Frame(self.master, bg="#181818")
        self.image_frame = Frame(self.master, bg="#333333") #Frame for camera feed

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.image_frame.grid(row=0, column=1, sticky="nsew") #Place the camera feed frame

        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid_rowconfigure(2, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        self.image_frame.grid_rowconfigure(0, weight=1)
        self.image_frame.grid_columnconfigure(0, weight=1)

        self.left_frame.grid_propagate(False)
        self.image_frame.grid_propagate(False)

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

        self.image_label = Label(self.image_frame) #Label to display the image
        self.image_label.grid(row=0, column=0, sticky="nsew")

    def callback(self, msg):
        self.ros_label.config(text=msg.data)

    def publish_on_topic(self):
        self.test_publisher.publish("x: " + self.x_entry.get() + " y: " + self.y_entry.get() + " z: " + self.z_entry.get())
        self.x_entry.delete(0, 'end')
        self.y_entry.delete(0, 'end')
        self.z_entry.delete(0, 'end')

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

            img = PIL_Image.fromarray(cv_image)
            img = ImageTk.PhotoImage(image=img)

            # Update only the image, not the entire label
            if self.tk_image is None:
                self.tk_image = img
                self.image_label.config(image=img)
            else:
                self.image_label.configure(image=img)
                self.tk_image = img

        except Exception as e:
            print(f"Error converting image: {e}")

if __name__ == "__main__":
    root = Tk()
    my_gui = ROSGUI(root)
    root.mainloop()