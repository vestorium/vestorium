"""
Autonomous Systems vertical — sample repos for analysis.
One repo per sub-category minimum, two for sub-categories with
enough variation to show score differences.
Add or remove URLs here to change which repos get analyzed.

Note on stereolabs/zed-sdk: commercial hardware SDK — may be
partially private. Fallback: PointCloudLibrary/pcl if scrape fails.

Note on opencv/opencv: Intel-maintained, 20+ years old. Expect
PLATFORM_ABSORBED pattern — same as apache/kafka in Data Infrastructure.
Good benchmark setter for score variation within sub-category.

Note on openai/gym: deprecated in 2023 in favor of
Farama-Foundation/Gymnasium. Included deliberately — should score
low and flag correctly. Validates how tool handles deprecated repos.

Note on mit-biomimetics/Cheetah-Software: academic repo but
highly cited in industry. Strong has_hardware_interface signal —
real quadruped robot deployment evidence.
"""

SAMPLE_REPOS = [
    # Robot Middleware & Communication
    "https://github.com/ros2/rclpy",

    # Perception & Computer Vision
    "https://github.com/opencv/opencv",
    "https://github.com/stereolabs/zed-sdk",

    # Motion Planning & Control
    "https://github.com/moveit/moveit2",

    # Simulation & Digital Twins
    "https://github.com/gazebosim/gz-sim",
    "https://github.com/google-deepmind/mujoco",

    # Field Robotics & Navigation
    "https://github.com/PX4/PX4-Autopilot",

    # Robot Manipulation & Dexterous Control
    "https://github.com/huggingface/lerobot",

    # Robot Learning & Reinforcement Learning
    "https://github.com/openai/gym",

    # Foundation Models for Robotics
    "https://github.com/mit-biomimetics/Cheetah-Software",
]