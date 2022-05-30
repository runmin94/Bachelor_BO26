#!/usr/bin/env python

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_test', anonymous=True)

robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
group = moveit_commander.MoveGroupCommander("UR10_group")
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=1)


pose_target = geometry_msgs.msg.Pose()

print("pose_target:")
print(pose_target)
print("current joint values: ")
print(group.get_current_joint_values())
pose_target.orientation.w = 1.0
pose_target.position.x = 0.9
pose_target.position.y = 0.5
pose_target.position.z = 1.2
group.set_pose_target(pose_target)

print(pose_target)
plan1 = group.plan()


rospy.sleep(5)

moveit_commander.roscpp_shutdown()


