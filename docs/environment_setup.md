# Environment Setup

Follow these steps to set up the environment for the ROS Printing Station:

## Prerequisites

1. **Operating System**: Ensure you are using a compatible OS (e.g., Ubuntu 20.04).
2. **ROS Installation**: Follow the [official ROS installation guide](http://wiki.ros.org/noetic/Installation/Ubuntu).

## Step-by-Step Setup

### 1. Update and Upgrade System

```bash
sudo apt update
sudo apt upgrade
```

### 2. Initialize rosdep

```bash
sudo rosdep init
rosdep update
```

### 3. Setup Environment

Add the following line to your `.bashrc` file:

```bash
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### 4. Install Dependencies

```bash
sudo apt install python3-rosinstall python3-rosinstall-generator python3-wstool build-essential
```

### 5. Verify Installation

```bash
roscore
```

If `roscore` starts without errors, your environment is set up correctly.

## Additional Resources

- [ROS Tutorials](http://wiki.ros.org/ROS/Tutorials)
- [ROS Documentation](http://wiki.ros.org/Documentation)

