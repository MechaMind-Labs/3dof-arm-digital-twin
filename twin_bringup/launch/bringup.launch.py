from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription
import os


def generate_launch_description():

    twin_description = get_package_share_directory("twin_description")
    twin_controller  = get_package_share_directory("twin_controller")
    twin_firmware    = get_package_share_directory("twin_firmware")

    display_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(twin_description, 'launch', 'display.launch.py')
        )
    )

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(twin_description, 'launch', 'gazebo.launch.py')
        )
    )

    controller_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(twin_controller, 'launch', 'controller.launch.py')
        )
    )

    firmware_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(twin_firmware, 'launch', 'firmware.launch.py')
        )
    )

    return LaunchDescription([
        # display_launch,
        gazebo_launch,
        controller_launch,
        firmware_launch
    ])
