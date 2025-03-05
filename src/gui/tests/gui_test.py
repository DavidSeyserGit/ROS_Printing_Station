import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
import rospy
from std_msgs.msg import String
import sys
import os
# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gui import ROSGUI # import the class from gui.py
class TestROSGUI(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        with patch('rospy.init_node'), \
             patch('rospy.Subscriber'), \
             patch('rospy.Publisher'):
            self.gui = ROSGUI(self.root)
            self.gui.test_publisher = MagicMock() # Mock the publisher

    def tearDown(self):
        self.root.destroy()

    def test_create_widgets(self):
        self.assertIsInstance(self.gui.left_frame, tk.Frame)
        self.assertIsInstance(self.gui.right_frame, tk.Frame)
        self.assertIsInstance(self.gui.ros_label, tk.Label)
        self.assertIsInstance(self.gui.send_button, tk.Button)
        self.assertIsInstance(self.gui.entry_frame, tk.Frame)
        self.assertIsInstance(self.gui.x_entry, tk.Entry)
        self.assertIsInstance(self.gui.y_entry, tk.Entry)
        self.assertIsInstance(self.gui.z_entry, tk.Entry)
        self.assertIsInstance(self.gui.right_label, tk.Label)
        self.assertIsInstance(self.gui.test_button, tk.Button)

    def test_callback(self):
        msg = String(data="Test Message")
        self.gui.callback(msg)
        self.assertEqual(self.gui.ros_label['text'], "Test Message")

    def test_publish_on_topic(self):
        self.gui.x_entry.insert(0, "1")
        self.gui.y_entry.insert(0, "2")
        self.gui.z_entry.insert(0, "3")
        self.gui.publish_on_topic()
        self.gui.test_publisher.publish.assert_called_once_with("x: 1 y: 2 z: 3")
        self.assertEqual(self.gui.x_entry.get(), "")
        self.assertEqual(self.gui.y_entry.get(), "")
        self.assertEqual(self.gui.z_entry.get(), "")

    @patch('rospy.init_node')
    @patch('rospy.Subscriber')
    @patch('rospy.Publisher')
    def test_ros_initialization(self, mock_publisher, mock_subscriber, mock_init_node):
        root = tk.Tk()
        ROSGUI(root)
        mock_init_node.assert_called_once_with('gui', anonymous=True)
        mock_subscriber.assert_called_once()
        mock_publisher.assert_called_once()
        root.destroy()

if __name__ == '__main__':
    unittest.main()