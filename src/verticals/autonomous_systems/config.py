"""
Autonomous Systems vertical configuration.
All vertical-specific settings live here — keywords, benchmarks,
flag thresholds, AI framework maps, and repo lists.
Shared code (scraper, scorer, tracker) reads from this config.

Sub-categories covered:
  Robot Middleware & Communication,
  Perception & Computer Vision,
  Motion Planning & Control,
  Simulation & Digital Twins,
  Field Robotics & Navigation,
  Robot Manipulation & Dexterous Control,
  Fleet Management & Multi-Agent Systems,
  Foundation Models for Robotics,
  Robot Learning & Reinforcement Learning

Moat framing:
  Primary moat = deployment data advantage.
  Software that improves with real-world robot operation data
  builds a compounding moat competitors cannot replicate without
  the same deployment base.
  GitHub proxy: evidence of real-world hardware integration —
  URDF files, hardware interface definitions, calibration scripts,
  sensor driver configs.

Benchmark philosophy:
  Robotics GitHub communities are structurally smaller than every
  other vertical. Hardware dependency limits casual adoption —
  you cannot clone and run a robotics repo without the hardware.
  All benchmarks are the lowest of any vertical. A robotics repo
  with 300 stars and 40 commits/month may be more impressive than
  a DevTools repo with 2000 stars and 100 commits/month.

Vertical-unique parameter:
  has_hardware_interface — checks for URDF files, hardware interface
  definitions, calibration scripts, sensor driver configs.
  Signals software has been tested on real robots, not just in
  simulation. Directly proxies the deployment data advantage moat.
  Weighted at 40% of Engineering Discipline.

Key weight difference from other verticals:
  Technical Moat: 35pts (vs 30pts elsewhere) — deployment data
  advantage is the defining moat, uniquely hard for PE/VCs to assess.
  Community Traction: 15pts (vs 20pts elsewhere) — small community
  is structural in robotics, not a quality signal.

Autonomous Systems-specific flags (beyond standard 13):
  SIMULATION_ONLY        — software never validated on real hardware
  HARDWARE_DEPENDENT_LOCK — tool locked to single robot manufacturer
"""

VERTICAL_NAME = "Autonomous Systems"
VERTICAL_SLUG = "autonomous_systems"

# ── Sub-category detection ─────────────────────────────────────────────
SUBCATEGORY_KEYWORDS = {
    "Robot Middleware & Communication": [
        "ros", "ros2", "robot-operating-system", "middleware",
        "dds", "micro-ros", "robot-framework", "ros-humble",
        "ros-noetic", "robot-communication",
    ],
    "Perception & Computer Vision": [
        "robot-perception", "lidar", "point-cloud", "object-detection",
        "semantic-segmentation", "depth-estimation", "slam",
        "sensor-fusion", "3d-perception", "computer-vision-robotics",
    ],
    "Motion Planning & Control": [
        "motion-planning", "path-planning", "trajectory-optimization",
        "control", "moveit", "ompl", "mpc", "pid-control",
        "robot-control", "trajectory-planning",
    ],
    "Simulation & Digital Twins": [
        "robot-simulation", "gazebo", "isaac-sim", "mujoco",
        "digital-twin", "sim-to-real", "physics-simulation",
        "urdf", "robot-simulator", "virtual-environment",
    ],
    "Field Robotics & Navigation": [
        "autonomous-navigation", "slam", "localization", "mapping",
        "autonomous-driving", "drone", "uav", "agv", "amr",
        "autonomous-mobile-robot", "self-driving",
    ],
    "Robot Manipulation & Dexterous Control": [
        "robot-arm", "manipulation", "grasping", "pick-and-place",
        "dexterous", "end-effector", "force-control",
        "robotic-manipulation", "tactile", "cobot",
    ],
    "Fleet Management & Multi-Agent Systems": [
        "fleet-management", "multi-robot", "swarm", "multi-agent",
        "robot-coordination", "task-allocation", "robot-fleet",
        "collaborative-robots", "distributed-robotics",
    ],
    "Foundation Models for Robotics": [
        "robot-foundation-model", "vision-language-action", "vla",
        "robot-transformer", "embodied-ai", "generalist-robot",
        "robot-llm", "robot-gpt", "lerobot", "octo",
    ],
    "Robot Learning & Reinforcement Learning": [
        "robot-learning", "sim-to-real", "reinforcement-learning-robotics",
        "imitation-learning", "policy-learning", "robot-rl",
        "safe-rl", "contact-rich", "robosuite",
    ],
}

# ── Flat keyword list for vertical detection ───────────────────────────
KEYWORDS = [kw for kws in SUBCATEGORY_KEYWORDS.values() for kw in kws] + [
    "robotics", "autonomous-systems", "autonomous-robot",
    "robot-software", "embodied-ai", "robot-ai", "intelligent-robot",
    "autonomous-mobile-robot", "robotic-arm", "autonomous-vehicle",
    "robot", "automation", "actuator", "servo", "kinematics",
]

# ── Dependency detection ───────────────────────────────────────────────
DEPENDENCIES = [
    # Robot Middleware
    "rclpy", "rclcpp", "rospy", "roscpp", "fastdds", "cyclonedds",
    # Perception & Computer Vision
    "open3d", "pcl", "opencv-python", "ultralytics", "mmdetection",
    "detectron2", "pointnet",
    # Motion Planning & Control
    "moveit", "ompl", "casadi", "drake", "pinocchio",
    "robotics-toolbox",
    # Simulation
    "mujoco", "gymnasium", "pybullet", "isaacgym", "gym",
    "robosuite",
    # Navigation
    "nav2", "cartographer", "mavros", "pymavlink",
    # Manipulation
    "pinocchio", "pybullet", "roboticstoolbox-python",
    # Fleet / Multi-agent
    "ray", "networkx", "pymavlink",
    # Foundation Models
    "torch", "transformers", "diffusers", "timm",
    # Robot Learning
    "stable-baselines3", "sb3", "d3rlpy", "imitation",
]

# ── Scoring benchmarks ─────────────────────────────────────────────────
# Lowest benchmarks of all verticals — hardware dependency is structural.
# A robotics repo with 300 stars and 40 commits/month may be more
# impressive than a DevTools repo with 2000 stars and 100 commits/month.
# Hardware testing cycles slow commits — each change requires physical
# robot validation.
BENCHMARKS = {
    "stars_seed"            : 300,   # lowest of all verticals — hardware limits casual adoption
    "commit_velocity"       : 40,    # lowest of all verticals — hardware testing slows iteration
    "releases_per_year"     : 6,     # lower — hardware-gated releases take longer
    "days_since_update"     : 90,    # same staleness threshold across all verticals
    "issue_resolution_rate" : 60,    # lowest of all verticals — hardware bugs are harder to reproduce remotely
    "pr_merge_rate_min"     : 35,    # rigorous review — safety-critical systems
    "pr_merge_rate_max"     : 65,    # same upper ceiling
    "contributors_per_year" : 4,     # lowest of all verticals — robotics expertise is scarce
}

# ── Flag thresholds ────────────────────────────────────────────────────
FLAG_THRESHOLDS = {
    "LOW_ISSUE_RESOLUTION"          : 60,    # matches benchmark — lowest of all verticals
    "LOW_COMMIT_VELOCITY"           : 40,    # matches benchmark
    "STALE_REPO"                    : 90,    # same across all verticals
    "INFRASTRUCTURE_PLAY"           : 1000,  # lower than other verticals — robotics stars are harder to accumulate
    "LOW_PR_MERGE_RATE"             : 35,    # safety-critical — rigorous review expected
    # Autonomous Systems-specific flag thresholds
    "PLATFORM_ABSORBED_STARS"       : 5000,  # same as MLOps and Data Infra
    "SIMULATION_ONLY_STARS"         : 500,   # above this + no hardware interface = flag
    "HARDWARE_LOCK_CONTRIBUTORS"    : 15,    # below this + single platform = flag
}

# ── Scoring dimension weights ──────────────────────────────────────────
# KEY DIFFERENCE from all other verticals:
# Technical Moat raised to 35 — deployment data advantage is the
# defining moat in robotics, uniquely hard for PE/VCs to assess.
# Community Traction lowered to 15 — small robotics communities
# are structural, not a quality signal. Penalizing for small star
# counts vs DevTools would be analytically incorrect.
DIMENSION_WEIGHTS = {
    "technical_execution"   : 30,
    "technical_moat"        : 35,
    "community_traction"    : 15,
    "team_strength"         : 10,
    "engineering_discipline": 10,
}

# ── Investment recommendation thresholds ───────────────────────────────
RECOMMENDATION_THRESHOLDS = {
    "strong_buy" : 80,
    "buy"        : 50,
}

# ── Autonomous Systems-specific vertical parameters ───────────────────
# has_hardware_interface: checks for hardware abstraction layer files.
# URDF robot description files, hardware interface definitions,
# calibration scripts, sensor driver configs.
# Signals software has been tested on real robots — not just simulation.
# Directly proxies the deployment data advantage moat.
# Weighted at 40% of Engineering Discipline — same logic as
# has_security_policy in Cybersecurity and has_sdk in MLOps.
VERTICAL_PARAMS = {
    "has_hardware_interface": {
        "weight_in_engineering_discipline": 0.40,
        "detection_dirs": [
            "urdf/", "hardware_interface/", "calibration/",
            "drivers/", "bringup/", "description/",
        ],
        "detection_files": [
            "*.urdf", "*.xacro", "*.launch", "package.xml",
        ],
        "detection_keywords": [
            "hardware_interface", "urdf", "xacro", "ros_control",
            "joint_state", "robot_description",
        ],
    },
}

# ── Autonomous Systems-specific flag definitions ───────────────────────
AUTONOMOUS_SYSTEMS_FLAGS = {
    "SIMULATION_ONLY": {
        "severity"   : "High",
        "description": "Custom model or AI code present but no hardware interface "
                       "files detected. Software has not been validated on real robots. "
                       "The sim-to-real gap is the graveyard of robotics startups — "
                       "algorithms that work perfectly in simulation frequently fail "
                       "on real hardware due to sensor noise, actuator limits, and "
                       "contact physics that simulators approximate imperfectly.",
        "threshold"  : "has_custom_model=True + has_hardware_interface=False + stars > 500",
        "action"     : "Ask founder: how many real robot hours has this software accumulated? "
                       "What is the sim-to-real transfer success rate? "
                       "Which physical robot platforms has this been validated on?",
    },
    "HARDWARE_DEPENDENT_LOCK": {
        "severity"   : "Medium",
        "description": "Strong ROS integration detected but contributor count is low "
                       "and repo shows signs of single-platform dependency. "
                       "Tool may only work with one robot manufacturer's hardware, "
                       "capping TAM at that manufacturer's installed base. "
                       "PE/VC sees 'robotics software' — specialist sees "
                       "'ABB-only or Fanuc-only = narrow addressable market.'",
        "threshold"  : "has_hardware_interface=True + contributors < 15 + stars < 1000",
        "action"     : "Verify supported robot platforms. "
                       "Check documentation for hardware compatibility list. "
                       "Single-platform tools can still be investable if that "
                       "platform has large installed base (e.g., Universal Robots).",
    },
}

# ── Info tooltip text (for UI "i" buttons) ────────────────────────────
METRIC_INFO = {
    "commit_velocity": {
        "label"      : "Commit Velocity",
        "explanation": "Number of code commits per month, normalized by repo age.",
        "benchmark"  : "Autonomous Systems benchmark: >40 commits/month — "
                       "lowest of all verticals",
        "note"       : "Hardware testing cycles slow down commits significantly. "
                       "Each software change may require physical robot validation "
                       "before the next commit. A robotics repo at 40 commits/month "
                       "is executing as fast as a DevTools repo at 100 commits/month.",
    },
    "issue_resolution_rate": {
        "label"      : "Issue Resolution Rate",
        "explanation": "Percentage of GitHub issues that have been closed.",
        "benchmark"  : "Autonomous Systems benchmark: >60% resolved — "
                       "lowest of all verticals",
        "note"       : "Hardware-specific bugs are harder to reproduce and fix remotely. "
                       "A bug that only occurs on a specific robot configuration "
                       "requires physical access to diagnose. Lower resolution rate "
                       "is structurally expected — not necessarily a maintenance failure.",
    },
    "has_hardware_interface": {
        "label"      : "Hardware Interface",
        "explanation": "Checks for URDF robot description files, hardware interface "
                       "definitions, calibration scripts, and sensor driver configs.",
        "benchmark"  : "Presence expected for any robotics tool claiming real-world deployment",
        "note"       : "The most important signal in this vertical. Software with no "
                       "hardware interface files has only been run in simulation. "
                       "The sim-to-real gap is the graveyard of robotics startups — "
                       "algorithms that work in simulation frequently fail on real hardware. "
                       "Proxy signal only — does not verify deployment scale or success rate. "
                       "Always ask the founder: how many real robot hours has this accumulated?",
    },
    "has_custom_model": {
        "label"      : "Custom Model",
        "explanation": "Checks for model training code anywhere in the repo.",
        "benchmark"  : "Presence signals AI-native robotics with proprietary perception "
                       "or control models.",
        "note"       : "Combined with has_hardware_interface, this is the strongest "
                       "possible moat signal in robotics — proprietary AI that has been "
                       "validated on real hardware. Either signal alone is weaker. "
                       "Custom model without hardware interface = simulation-only risk. "
                       "Hardware interface without custom model = rules-based control, "
                       "lower AI moat.",
    },
    "stars": {
        "label"      : "Stars",
        "explanation": "GitHub stars in robotics indicate adoption from robotics "
                       "engineers and researchers.",
        "benchmark"  : "Autonomous Systems seed benchmark: >300 stars — "
                       "lowest of all verticals",
        "note"       : "Robotics GitHub communities are structurally smaller than "
                       "software-only verticals. Hardware dependency limits casual "
                       "adoption — you cannot clone and run a robotics repo without "
                       "the physical hardware. 300 stars from robotics engineers "
                       "carries more signal than 3000 stars from general developers.",
    },
    "technical_moat": {
        "label"      : "Technical Moat",
        "explanation": "Weighted at 35 points — higher than all other verticals (30pts).",
        "benchmark"  : "Primary moat signal: deployment data advantage",
        "note"       : "The deployment data advantage is the defining moat in robotics. "
                       "Every hour a robot operates in the real world generates sensor "
                       "data — camera feeds, LiDAR scans, force measurements, failure "
                       "cases — that competitors without deployed robots cannot access. "
                       "This compounding moat is why Boston Dynamics, Waymo, and Figure "
                       "AI are so hard to compete with. GitHub signals approximate "
                       "but do not directly measure deployment scale.",
    },
    "community_traction": {
        "label"      : "Community Traction",
        "explanation": "Weighted at 15 points — lower than all other verticals (20pts).",
        "benchmark"  : "Stars, forks, issue resolution, PR merge rate",
        "note"       : "Deliberately down-weighted for robotics. Small community size "
                       "is structural — hardware dependency limits GitHub adoption. "
                       "Penalizing robotics repos for small star counts versus DevTools "
                       "would produce analytically incorrect investment signals. "
                       "Focus on moat signals over vanity metrics in this vertical.",
    },
    "simulation_only_note": {
        "label"      : "Simulation-Only Risk",
        "explanation": "SIMULATION_ONLY flag fires when AI code is present but no "
                       "hardware interface files are detected.",
        "benchmark"  : "Flag fires at: has_custom_model=True + has_hardware_interface=False",
        "note"       : "The sim-to-real gap is the most common failure mode for "
                       "robotics AI startups. Algorithms that achieve 99% success "
                       "in simulation may achieve 60% on real hardware due to sensor "
                       "noise, actuator backlash, and contact physics approximation. "
                       "Always verify real-world deployment before investing.",
    },
    "moat_note": {
        "label"      : "Autonomous Systems Moat Assessment Note",
        "explanation": "Primary moat: deployment data advantage. "
                       "GitHub proxy: evidence of real-world hardware integration.",
        "benchmark"  : "N/A — GitHub signals approximate deployment scale.",
        "note"       : "Three questions every robotics investor should ask: "
                       "(1) How many real robot hours has this software accumulated? "
                       "(2) What is the sim-to-real transfer success rate? "
                       "(3) Which physical platforms has this been validated on? "
                       "None of these are answerable from GitHub — they require "
                       "direct founder conversation. GitHub screening narrows the "
                       "field; hardware validation closes the deal.",
    },
}
# ── LLM Moat Analyzer context ─────────────────────────────────────────
LLM_MOAT_CONTEXT = (
    "For Autonomous Systems AI startups, the key moat question is whether the team "
    "has real-world deployment data improving their algorithms — or whether they are "
    "simulation-only. Software trained only in simulation frequently fails on real "
    "hardware. Look for hardware interface code, real deployment references in README, "
    "and custom model code trained on proprietary operational data."
)