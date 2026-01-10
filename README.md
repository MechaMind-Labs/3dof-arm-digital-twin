# ROS2 3-DOF Robotic Arm Digital Twin

Build a **real-time digital twin** of a robotic arm controlled by potentiometers!  
Learn the complete pipeline from **hardware → ROS 2 → simulation**.

---

## 🎥 Demo

https://github.com/user-attachments/assets/577a7207-6b56-4fc4-a9bd-c0b9d5e58512

---

## ✨ What You'll Build

- 🎮 Control a robot arm with **4 potentiometers**
- 📡 Read sensor data from **ESP32** into ROS 2
- 🎛️ Visualize in **RViz** with real-time sync
- 🌍 Simulate physics in **Gazebo**
- 🤖 Complete **hardware-to-simulation** pipeline

---

## 🛠️ Hardware Required

- **ESP32** Development Board
- **4× Potentiometers** (100kΩ, 3-pin rotary)
- Breadboard & jumper wires
- USB cable

### Wiring Diagram

| Potentiometer | ESP32 Pin |
|---------------|-----------|
| Pot 1 | GPIO 33 | Joint 1 |
| Pot 2 | GPIO 32 | Joint 2 |
| Pot 3 | GPIO 35 | Joint 3 |
| Pot 4 | GPIO 34 | Joint_4 (Gripper) |

**Each potentiometer:**
- Left pin → **3.3V** ⚠️ (NOT 5V!)
- Center pin → **GPIO** (as per table)
- Right pin → **GND**

---

## 📋 Prerequisites

- **Ubuntu 22.04**
- **ROS 2 Humble** installed ([Install Guide](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html))
- **Arduino IDE** ([Download](https://www.arduino.cc/en/software))
- Basic terminal/command line knowledge

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
sudo apt update
sudo apt install -y python3-pip python3-rosdep python3-colcon-common-extensions
pip3 install pyserial
```

### Step 2: Clone Repository

```bash
cd ~
git clone https://github.com/MechaMind-Labs/ROS2_3DOF_Robotic_Arm_Digital_Twin.git
```

### Step 3: Setup Workspace

```bash
# Create workspace
mkdir -p ~/twin_ws/src

# Move packages
mv ~/ROS2_3DOF_Robotic_Arm_Digital_Twin/* ~/twin_ws/src/
rm -rf ~/ROS2_3DOF_Robotic_Arm_Digital_Twin

# Install dependencies
cd ~/twin_ws
source /opt/ros/humble/setup.bash
rosdep update
rosdep install --from-paths src --ignore-src -r -y

# Build
colcon build
source install/setup.bash
```

### Step 4: Flash ESP32

1. Open Arduino IDE
2. Install ESP32 board support:
   - `File` → `Preferences` → Add to "Additional Board Manager URLs":
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
   - `Tools` → `Board` → `Boards Manager` → Install "**esp32**"

3. Open firmware: `~/arm_ws/src/firmware/esp32_potentiometer_reader/esp32_potentiometer_reader.ino`

4. Configure:
   - **Board:** ESP32 Dev Module
   - **Port:** /dev/ttyUSB0 (or your port)
   - **Upload Speed:** 115200

5. Click **Upload** ➜

6. Verify in Serial Monitor (115200 baud) - you should see CSV values

### Step 5: Find USB Port

```bash
ls /dev/ttyUSB*
# or
ls /dev/ttyACM*
```

Note your port (e.g., `/dev/ttyUSB0`)

### Step 6: Give Permission

```bash
sudo usermod -aG dialout $USER
# Log out and log back in
```

---

## 🎮 Run the Project

Add to your `.bashrc` for convenience:

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
echo "source ~/twin_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### Option A: RViz Only (Beginner-Friendly)

Open **2 terminals:**

**Terminal 1 - Serial Reader:**
```bash
ros2 launch twin_firmware firmware.launch.py
```

**Terminal 2 - Launch RViz:**
```bash
ros2 launch twin_description display.launch.py
```

🎉 Rotate your potentiometers and watch the robot move!

---

### Option B: Full Digital Twin Project (Gazebo)

Open **1 terminal:**

**Terminal 1 - Full Project Bringup:**
```bash
ros2 launch twin_bringup bringup.launch.py
```

🚀 Now Gazebo sync's with your movements!

---

## ⚠️ Troubleshooting

### No data in terminal
- Check ESP32 wiring (especially 3.3V, NOT 5V!)
- Verify serial port: `ls /dev/ttyUSB*`
- Press **RESET** button on ESP32

### Permission denied on /dev/ttyUSB0
```bash
sudo chmod 666 /dev/ttyUSB0
# Or permanently:
sudo usermod -aG dialout $USER
# Then log out and back in
```

### Robot not moving
- Check ROS topics: `ros2 topic list`
- Echo data: `ros2 topic echo /joint_commands`
- Verify all nodes running: `ros2 node list`

### Jerky movement
- Increase filter size in ESP32 code (line 9):
  ```cpp
  const int FILTER_SIZE = 20;  // Increase to 30-40
  ```

---

## 🎓 Learning Resources

- [ROS 2 Tutorials](https://docs.ros.org/en/humble/Tutorials.html)
- [URDF Tutorial](http://wiki.ros.org/urdf/Tutorials)
- [Gazebo Tutorial](https://classic.gazebosim.org/tutorials)

---

## 🙌 Credits

Maintained by **[Curious-Utkarsh](https://github.com/Curious-Utkarsh)**  
Inspired by real-world **edge-avoidance robotics** applications.

---

## 🤝 Contributing

Found a bug? Have an idea?
- 🐛 [Report Issues](https://github.com/MechaMind-Labs/ROS2_3DOF_Robotic_Arm_Digital_Twin/issues)
- ⭐ Star the repo if this helped you!
- 🔀 Fork and submit Pull Requests

---

## 📧 Contact

**Kumar Utkarsh** - MechaMind Labs  
🔗 [LinkedIn](linkedin.com/in/kumar-utkarsh-124aab227) | [GitHub](https://github.com/Curious-Utkarsh)

**Workshop Inquiries:** [LinkedIn](https://www.mechamindlabs.com/contact)

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

✨ **Build amazing robots and have fun learning!** 🚀🤖
