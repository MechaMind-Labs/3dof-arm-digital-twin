#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class ArmController(Node):
    def __init__(self):
        super().__init__("arm_controller")
        
        # Publishers for RViz and Gazebo
        self.joint_state_pub = self.create_publisher(JointState, "joint_states", 10)
        self.arm_pub = self.create_publisher(JointTrajectory, "arm_controller/joint_trajectory", 10)
        self.gripper_pub = self.create_publisher(JointTrajectory, "gripper_controller/joint_trajectory", 10)
        
        # Subscriber
        self.sub = self.create_subscription(JointState, "joint_commands", self.joint_callback, 10)
        
        self.get_logger().info("Arm Controller started")
    
    def joint_callback(self, msg):
        # Publish to RViz (joint_states)
        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = msg.name
        joint_state.position = msg.position
        self.joint_state_pub.publish(joint_state)
        
        # Publish to Gazebo (arm_controller)
        arm_traj = JointTrajectory()
        arm_traj.joint_names = ["joint_1", "joint_2", "joint_3"]
        
        arm_point = JointTrajectoryPoint()
        arm_point.positions = msg.position[:3]
        arm_traj.points.append(arm_point)
        
        self.arm_pub.publish(arm_traj)
        
        # Publish to Gazebo (gripper_controller)
        gripper_traj = JointTrajectory()
        gripper_traj.joint_names = ["joint_4"]
        
        gripper_point = JointTrajectoryPoint()
        gripper_point.positions = [msg.position[3]]
        gripper_traj.points.append(gripper_point)
        
        self.gripper_pub.publish(gripper_traj)

def main():
    rclpy.init()
    node = ArmController()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()