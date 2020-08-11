# GRID STAIR CLIMBER ARENA GAZEBO SIMULATION
![](../images/logo.jpg)

## Prerequisites
- Ubuntu 16.04 or newer (Ubuntu 18.04 recommended)
- [ROS Kinetic ](http://wiki.ros.org/kinetic/Installation/Ubuntu) (Ubuntu 16.04) or [ROS Melodic ](http://wiki.ros.org/melodic/Installation/Ubuntu) (Ubuntu 16.04)
- [Catkin Tools](https://catkin-tools.readthedocs.io/en/latest/installing.html)


## Build
Build all the packages by running this inside your workspace
```sh
$ catkin build grid_stair_arena
$ source devel/setup.bash
```

## Extract model files
Extract models.zip to home/.gazebo/
```sh
$ roscd grid_stair_arena
$ unzip models.zip -d ~/.gazebo/models/
```

## Utilities
Teleop twist keyboard:
```sh
$ https://github.com/ros-teleop/teleop_twist_keyboard.git
```

### Todos

 - Fill the whole arena with obstacles

License
----

MIT

