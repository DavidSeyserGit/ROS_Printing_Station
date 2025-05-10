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
        master.geometry('1400x600')
        master.title("ROS Printing Station")
        master.configure(bg="#292929")  # Dark background for the entire app

        # Initialize ROS node (if not already initialized)
        rospy.init_node('gui', anonymous=True)

        rospy.Subscriber("/response", String, self.callback)
        rospy.Subscriber("/error", String, self.error_callback)
        rospy.Subscriber("/image_raw", Image, self.image_callback)
        self.test_publisher = rospy.Publisher("/chatter", String, queue_size=10)
        self.bridge = CvBridge()
        self.tk_image1 = None
        self.tk_image2 = None
        
        # Track which camera view is active (1 or 2)
        self.active_camera = 1

        self.create_widgets()

    def create_widgets(self):
        self.left_frame = Frame(self.master, bg="#232323", highlightbackground="#3d3d3d", highlightthickness=1)
        self.image_frame = Frame(self.master, bg="#333333", highlightbackground="#3d3d3d", highlightthickness=1)

        # Create layout
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=3)  # Give more weight to image frame
        self.master.grid_rowconfigure(0, weight=1)

        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.image_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.left_frame.grid_rowconfigure(0, weight=0)
        self.left_frame.grid_rowconfigure(1, weight=0)
        self.left_frame.grid_rowconfigure(2, weight=0)  # Changed to 0 to keep elements tight
        self.left_frame.grid_columnconfigure(0, weight=1)

        # Configure image frame for camera views and controls
        self.image_frame.grid_rowconfigure(0, weight=1)  # For camera view
        self.image_frame.grid_rowconfigure(1, weight=0)  # For camera controls
        self.image_frame.grid_columnconfigure(0, weight=1)

        self.left_frame.grid_propagate(False)
        self.image_frame.grid_propagate(False)

        # Status section - grouped together with minimal spacing
        status_section = Frame(self.left_frame, bg="#232323")
        status_section.grid(row=0, column=0, sticky="n", pady=(10, 0))
        
        self.status_label = Label(
            status_section, 
            text="Status Indicator", 
            bg="#232323", 
            fg="#e0e0e0", 
            font=("Helvetica", 14, "bold")
        )
        self.status_label.pack(pady=(0, 2))
        
        self.ros_label = Canvas(status_section, width=100, height=100, bg="#232323", highlightthickness=0)
        self.ros_label.create_oval(10, 10, 90, 90, fill="#e0e0e0", outline="#555555", width=2)
        self.ros_label.pack(pady=(0, 2))
        
        self.error_label = Label(
            status_section, 
            text="Error: None", 
            bg="#232323", 
            fg="#e0e0e0", 
            font=("Helvetica", 11),
            wraplength=300
        )
        self.error_label.pack(pady=(0, 5))

        # Rest of the controls
        self.start_button = Button(
            self.left_frame, 
            text="Start Robot Operation", 
            command=self.start_robot,
            bg="#4caf50",  
            fg="white",    
            font=("Helvetica", 12, "bold"),
            relief=RAISED,
            borderwidth=2,
            padx=25,
            pady=12,
            activebackground="#45a049",
            cursor="hand2"
        )
        self.start_button.grid(row=1, column=0, padx=20, pady=10, sticky="n")

        self.start_description = Label(
            self.left_frame, 
            text="Press to begin the automated printing operation",
            bg="#232323", 
            fg="#aaaaaa",
            font=("Helvetica", 9, "italic")
        )
        self.start_description.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="n")

        self.entry_frame = Frame(self.left_frame, bg="#232323", pady=5)
        self.entry_frame.grid(row=3, column=0, sticky="n", pady=5)
        self.entry_frame.grid_columnconfigure(0, weight=1)
        self.entry_frame.grid_columnconfigure(1, weight=1)
        self.entry_frame.grid_columnconfigure(2, weight=1)

        # Add labels above entries
        Label(self.entry_frame, text="X", bg="#232323", fg="#e0e0e0", font=("Helvetica", 10)).grid(row=0, column=0)
        Label(self.entry_frame, text="Y", bg="#232323", fg="#e0e0e0", font=("Helvetica", 10)).grid(row=0, column=1)
        Label(self.entry_frame, text="Z", bg="#232323", fg="#e0e0e0", font=("Helvetica", 10)).grid(row=0, column=2)

        entry_style = {"font": ("Helvetica", 11), "borderwidth": 2, "relief": SUNKEN}
        self.x_entry = Entry(self.entry_frame, width=15, bg="#f54242", **entry_style)
        self.y_entry = Entry(self.entry_frame, width=15, bg="#75f542", **entry_style)
        self.z_entry = Entry(self.entry_frame, width=15, bg="#4278f5", **entry_style)
        self.x_entry.grid(row=1, column=0, sticky="ew", padx=5)
        self.y_entry.grid(row=1, column=1, sticky="ew", padx=5)
        self.z_entry.grid(row=1, column=2, sticky="ew", padx=5)

        self.send_button = Button(
            self.left_frame, 
            text="Send Joint Values", 
            command=self.publish_on_topic,
            bg="#3498db", 
            fg="white",
            font=("Helvetica", 11),
            padx=10,
            pady=5,
            relief=RAISED,
            borderwidth=2,
            cursor="hand2"
        )
        self.send_button.grid(row=4, column=0, padx=10, pady=10, sticky="n")

        # Camera views - both initially created but only one shown at a time
        self.image_label1 = Label(self.image_frame, bg="#333333", bd=2, relief=SUNKEN)
        self.image_label1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.image_label2 = Label(self.image_frame, bg="#333333", bd=2, relief=SUNKEN)
        # Initially hide the second view
        
        # Camera controls frame
        camera_controls = Frame(self.image_frame, bg="#333333")
        camera_controls.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        # Camera toggle button
        self.camera_toggle = Button(
            camera_controls,
            text="Switch Camera View",
            command=self.toggle_camera_view,
            bg="#555555",
            fg="white",
            font=("Helvetica", 10),
            padx=10,
            pady=5,
            relief=RAISED,
            cursor="hand2"
        )
        self.camera_toggle.pack(pady=5)
        
        # Camera labels
        self.camera1_label = Label(
            camera_controls,
            text="Camera 1: Main View",
            bg="#333333",
            fg="#e0e0e0",
            font=("Helvetica", 10, "bold")
        )
        self.camera1_label.pack(side=LEFT, padx=(20, 10))
        
        self.camera2_label = Label(
            camera_controls,
            text="Camera 2: Secondary View",
            bg="#333333",
            fg="#aaaaaa",
            font=("Helvetica", 10)
        )
        self.camera2_label.pack(side=RIGHT, padx=(10, 20))

    def toggle_camera_view(self):
        if self.active_camera == 1:
            # Switch to camera 2
            self.image_label1.grid_remove()
            self.image_label2.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            self.active_camera = 2
            
            # Update labels to show which camera is active
            self.camera1_label.config(fg="#aaaaaa", font=("Helvetica", 10))
            self.camera2_label.config(fg="#e0e0e0", font=("Helvetica", 10, "bold"))
        else:
            # Switch to camera 1
            self.image_label2.grid_remove()
            self.image_label1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            self.active_camera = 1
            
            # Update labels to show which camera is active
            self.camera1_label.config(fg="#e0e0e0", font=("Helvetica", 10, "bold"))
            self.camera2_label.config(fg="#aaaaaa", font=("Helvetica", 10))

    def callback(self, msg):
        # Update the status label
        color = msg.data.lower()
        self.ros_label.delete("all")
        self.ros_label.create_oval(10, 10, 90, 90, fill=color, outline="#555555", width=2)

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
        
    def error_callback(self, msg):
        # Update the error label with the received error message
        self.error_label.config(text=f"Error: {msg.data}", fg="#ff6b6b", font=("Helvetica", 12, "bold"))

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            # Convert from BGR to RGB for display
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            img = PIL_Image.fromarray(cv_image)
            
            # Update both camera views with the same image (for now)
            img1 = ImageTk.PhotoImage(image=img)
            img2 = ImageTk.PhotoImage(image=img)
            
            self.image_label1.configure(image=img1)
            self.image_label2.configure(image=img2)
            
            # Keep references to avoid garbage collection
            self.tk_image1 = img1
            self.tk_image2 = img2
            
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
