from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
                                 QPushButton, QTextEdit)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QPainter, QColor
import rospy
from std_msgs.msg import String

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Printing GUI")
        self.setGeometry(0, 0, 800, 500)  # Widened window for two systems

        rospy.init_node("GUI", anonymous=True)

        # ROS Publishers
        self.inspector_pub = rospy.Publisher("/chatter", String, queue_size=10)
        self.picker_pub = rospy.Publisher("/chatter", String, queue_size=10)
        rospy.Subscriber("/response", String, self.update_inspector_status)  # New subscriber
        
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main Horizontal Layout
        main_layout = QHBoxLayout()

        # System 1 Layout (Left Side)
        inspector = QVBoxLayout()
        self.inspector_status_label = QLabel()
        self.set_status_color("yellow")  # Initial color
        self.inspector_send = QPushButton("Send Inspetor")
        self.inspector_send.clicked.connect(self.send_move_command_inspector)
        
        
        inspector.addWidget(QLabel("Inspector Robot"))
        inspector.addWidget(QLabel(""))
        inspector.addWidget(self.inspector_status_label)
        inspector.addWidget(self.inspector_send)


        # System 2 Layout (Right Side)
        picker = QVBoxLayout()
        self.picker_send = QPushButton("Send Picker")
        self.picker_send.clicked.connect(self.send_move_command_picker)
        
        picker.addWidget(QLabel("Picker Robot"))
        picker.addWidget(QLabel(""))
        picker.addWidget(QLabel(""))
        picker.addWidget(self.picker_send)

        # Add both systems to main layout
        main_layout.addLayout(inspector)
        main_layout.addLayout(picker)
        self.central_widget.setLayout(main_layout)

    def send_move_command_inspector(self):
        msg = String()
        msg.data = "Hello from Inspector"
        self.inspector_pub.publish(msg)

    def send_move_command_picker(self):
        msg = String()
        msg.data = "Hello from Picker"
        self.picker_pub.publish(msg)

    def update_inspector_status(self, msg):
        status = msg.data
        self.set_status_color(status)

    def set_status_color(self, color_name):
        size = QSize(50, 50)  # Size of the dot
        pixmap = QPixmap(size)
        pixmap.fill(Qt.transparent)  # Make background transparent

        painter = QPainter(pixmap)
        if color_name.lower() == "green":
            color = QColor(0, 255, 0)  # Green
        elif color_name.lower() == "red":
            color = QColor(255, 0, 0)  # Red
        elif color_name.lower() == "yellow":
            color = QColor(255, 255, 0)  # Yellow
        else:
            color = QColor(128, 128, 128) # Gray (Default/Unknown)

        painter.setBrush(color)
        painter.drawEllipse(10, 10, 30, 30)  # Draw the filled circle
        painter.end()

        self.inspector_status_label.setPixmap(pixmap)
if __name__ == "__main__":
    app = QApplication()
    window = GUI()
    window.show()
    app.exec()
