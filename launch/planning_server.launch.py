from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory

from launch_ros.substitutions import FindPackageShare
from launch.substitutions import Command, PathJoinSubstitution,TextSubstitution
def generate_launch_description():

    ### SRDF URDF ###

    #### Define the robot description file ####
    # robot_description_file = ParameterValue(
    #     Command(['xacro ', PathJoinSubstitution([FindPackageShare('robot_description'), 'urdf/robot_description.xacro'])]),
    #     value_type=str
    # )
    robot_description_file = ParameterValue(
    Command(['xacro ', PathJoinSubstitution([FindPackageShare('cogniman_scene_description'), 'urdf/cogniman_description.xacro'])]),
    value_type=str
    )
    
    #### Define the kinematic plugin ####
    # path_to_plugins_arg = DeclareLaunchArgument(
    #     'path_to_kinematic_plugins',
    #     default_value=PathJoinSubstitution([FindPackageShare('robot_description'), 'config/robot_description_plugins.yaml']),
    #     description='Path to the kinematics plugins configuration file')

    path_to_plugins_arg = DeclareLaunchArgument(
    'path_to_kinematic_plugins',
    default_value=PathJoinSubstitution([FindPackageShare('cogniman_scene_description'), 'config/IK_plugin.yaml']),
    description='Path to the kinematics plugins configuration file')


    # Define the robot description semantic file    
    # robot_description_semantic_file = ParameterValue(
    #     Command([
    #         'xacro ', 
    #         PathJoinSubstitution([
    #             FindPackageShare('robot_description'), 
    #             'config/robot_description_srdf.xacro'
    #         ]),
    #         # pass the kinematic plugin as xacro param
    #         TextSubstitution(text=' path_to_kinematic_plugins:='),
    #         LaunchConfiguration('path_to_kinematic_plugins')
    #     ]),
    #     value_type=str
    # )
    robot_description_semantic_file = ParameterValue(
        Command([
            'xacro ', 
            PathJoinSubstitution([
                FindPackageShare('cogniman_scene_description'), 
                'config/srdf.xacro'
            ]),
            # pass the kinematic plugin as xacro param
            TextSubstitution(text=' path_to_kinematic_plugins:='),
            LaunchConfiguration('path_to_kinematic_plugins')
        ]),
        value_type=str
    )

    ###  ###


    return LaunchDescription([
        path_to_plugins_arg,
        
        DeclareLaunchArgument(
            'monitor_namespace',
            default_value='jesaispas',
            description='Namespace to monitor'
        ),
        DeclareLaunchArgument(
            'monitored_namespace',
            default_value='',
            description='Namespace being monitored'
        ),
         DeclareLaunchArgument(
            'path_to_plugins_arg',
            default_value='path_to_plugins_arg',
            description='path_to_plugins_arg'
        ),
        DeclareLaunchArgument(
            'robot_description',
            default_value='robot_description_file',
            description='Robot description parameter name'
        ),
           DeclareLaunchArgument(
            'robot_description_semantic',
            default_value='robot_description_semantic_file',
            description='Robot description semantic parameter name'
        ),

        DeclareLaunchArgument(
            'discrete_plugin',
            default_value='BulletDiscreteBVHManager',
            description='Discrete plugin name'
        ),
        DeclareLaunchArgument(
            'continuous_plugin',
            default_value='BulletCastBVHManager',
            description='Continuous plugin name'
        ),
        DeclareLaunchArgument(
            'publish_environment',
            default_value='false',
            description='Publish environment flag'
        ),
        DeclareLaunchArgument(
            'cache_size',
            default_value='5',
            description='Cache size'
        ),
        DeclareLaunchArgument(
            'cache_refresh_rate',
            default_value='0.1',
            description='Cache refresh rate'
        ),
        DeclareLaunchArgument(
            'task_composer_config',
            default_value=[get_package_share_directory('tesseract_task_composer'), '/config/task_composer_plugins.yaml'],
            description='Task composer config file'
        ),
        Node(
            package='planning_server',
            executable='planning_server_node',
            name='planning_server',
            output='screen',
            parameters=[{
                'robot_description': robot_description_file,
                'robot_description_semantic':robot_description_semantic_file,
                'discrete_plugin': LaunchConfiguration('discrete_plugin'),
                'continuous_plugin': LaunchConfiguration('continuous_plugin'),
                'monitor_namespace': LaunchConfiguration('monitor_namespace'),
                'monitored_namespace': LaunchConfiguration('monitored_namespace'),
                'publish_environment': LaunchConfiguration('publish_environment'),
                'cache_size': LaunchConfiguration('cache_size'),
                'cache_refresh_rate': LaunchConfiguration('cache_refresh_rate'),
                'task_composer_config': LaunchConfiguration('task_composer_config')
            }]
        )
    ])