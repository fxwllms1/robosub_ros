# RoboSub ROS 

This document has instructions to get you started. Reach each section carefully.

## Setup (All Platforms)

If you have a Windows, Mac or Linux on your desktop you can use Docker and Development Containers in vscode to do local development. This is the fastest and easiest way to get setup and enables you to run the simulator and control the ROV on your computer. This is the recommended setup for everyone.

1. [Install vscode](https://code.visualstudio.com/)
1. [Install Docker Desktop](https://www.docker.com/products/docker-desktop/) 
    * Docker command line is sufficient on Linux
1. Follow the [Dev Containers Tutorial](https://code.visualstudio.com/docs/devcontainers/tutorial)
1. Follow the linked instructions on how to [clone a repository locally](https://code.visualstudio.com/docs/sourcecontrol/intro-to-git#_open-a-git-repository), login to GitHub and when prompted, put in the repository URL:

    ```
    https://github.com/CabrilloRoboticsClub/robosub_ros.git    
    ```
1. You will be prompted to re-open the folder in a **development container**. Select yes.
1. Create a Terminal in your vscode window with the `Terminal -> New Terminal` menu. 
1. Build the software in your dev container: 

    **Run this command in the dev container terminal.**

    ```sh 
    make 
    ```

## Tutorials 

Ardupilot has official tutorials here:

* [Install ROS2](https://ardupilot.org/dev/docs/ros2.html)
* [ROS 2 with SITL in Gazebo](https://ardupilot.org/dev/docs/ros2-gazebo.html)
* [ROS 2 waypoint goal inerface](https://ardupilot.org/dev/docs/ros2-waypoint-goal-interface.html)
* [Cartographer SLAM with ROS 2 in SITL](https://ardupilot.org/dev/docs/ros2-cartographer-slam.html)

None of the tutorial's setup steps are necessary. The development container is fully setup. 
