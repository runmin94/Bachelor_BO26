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
rospy.init_node('move_group_test', anonymous=False)

robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
group = moveit_commander.MoveGroupCommander("UR10_group")
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=1)

group_variable_values = group.get_current_joint_values()

print group_variable_values

group_variable_values[0] = 0
group_variable_values[1] = 0
group_variable_values[2] = 0
group_variable_values[3] = 0
group_variable_values[4] = 0
group_variable_values[5] = 0

group.set_joint_value_target(group_variable_values)

plan2 = group.plan()


rospy.sleep(1)
group.go(wait=True)
rospy.sleep(5)


# group.set_joint_value_target(group_variable_values)

# plan2 = group.plan()

# rospy.sleep(5)
# group.go(wait=True)
# rospy.sleep(5)

moveit_commander.roscpp_shutdown()


