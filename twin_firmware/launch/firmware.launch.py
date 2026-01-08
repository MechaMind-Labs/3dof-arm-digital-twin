#!/usr/bin/env python3
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Declare launch arguments
    serial_port_arg = DeclareLaunchArgument(
        'serial_port',
        default_value='/dev/ttyUSB0',
        description='Serial port for ESP32'
    )
    
    baudrate_arg = DeclareLaunchArgument(
        'baudrate',
        default_value='115200',
        description='Serial baudrate'
    )
    
    min_angle_arg = DeclareLaunchArgument(
        'min_angle',
        default_value='-2.356',
        description='Minimum joint angle in radians (-270 degrees)'
    )
    
    max_angle_arg = DeclareLaunchArgument(
        'max_angle',
        default_value='2.356',
        description='Maximum joint angle in radians (270 degrees)'
    )
    
    # Serial reader node
    serial_reader_node = Node(
        package='twin_firmware',  
        executable='serial_reader.py',
        name='pot_serial_reader',
        output='screen',
        parameters=[{
            'port': LaunchConfiguration('serial_port'),
            'baudrate': LaunchConfiguration('baudrate'),
            'min_angle': LaunchConfiguration('min_angle'),
            'max_angle': LaunchConfiguration('max_angle')
        }]
    )
    
    # Arm controller node
    arm_controller_node = Node(
        package='twin_firmware', 
        executable='arm_controller.py',
        name='arm_controller',
        output='screen'
    )
    
    return LaunchDescription([
        serial_port_arg,
        baudrate_arg,
        min_angle_arg,
        max_angle_arg,
        serial_reader_node,
        arm_controller_node
    ])