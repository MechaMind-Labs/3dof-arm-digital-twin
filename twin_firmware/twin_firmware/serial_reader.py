#!/usr/bin/env python3
import serial
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class PotSerialReader(Node):
    def __init__(self):
        super().__init__("pot_serial_reader")
        
        # Parameters
        self.declare_parameter("port", "/dev/ttyUSB0")
        self.declare_parameter("baudrate", 115200)
        self.declare_parameter("min_angle", -2.356)
        self.declare_parameter("max_angle", 2.356)
        
        port = self.get_parameter("port").value
        baudrate = self.get_parameter("baudrate").value
        self.min_angle = self.get_parameter("min_angle").value
        self.max_angle = self.get_parameter("max_angle").value
        
        # Publisher
        self.pub = self.create_publisher(JointState, "joint_commands", 10)
        
        # Serial connection
        self.arduino = serial.Serial(port=port, baudrate=baudrate, timeout=0.1)
        self.get_logger().info(f"Connected to {port}")
        
        # Timer for reading (100Hz)
        self.timer = self.create_timer(0.01, self.timer_callback)
        
    def map_value(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
    def timer_callback(self):
        if rclpy.ok() and self.arduino.is_open:
            data = self.arduino.readline()
            
            try:
                # Decode and parse
                line = data.decode("utf-8").strip()
                if not line or "," not in line:
                    return
                
                # Split CSV values
                values = line.split(",")
                if len(values) != 4:
                    return
                
                raw_1 = int(values[0])
                raw_2 = int(values[1])
                raw_3 = int(values[2])
                raw_4 = int(values[3])
                
                # Map to angles
                angle_1 = self.map_value(raw_1, 0, 4095, self.min_angle, self.max_angle)
                angle_2 = self.map_value(raw_2, 0, 4095, self.min_angle, self.max_angle)
                angle_3 = self.map_value(raw_3, 0, 4095, self.max_angle, self.min_angle)
                angle_4 = self.map_value(raw_4, 0, 4095, self.min_angle, self.max_angle)
                
                # Publish as JointState
                msg = JointState()
                msg.name = ["joint_1", "joint_2", "joint_3", "joint_4"]
                msg.position = [angle_1, angle_2, angle_3, angle_4]
                
                self.pub.publish(msg)
                
            except:
                return

def main():
    rclpy.init()
    node = PotSerialReader()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()