#!/usr/bin/env python

import sys
import copy
import rospy
import time
import moveit_commander
from std_msgs.msg import Float64
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
pub_crane = rospy.Publisher('/gantry_crane/crane_controller/command', Float64, queue_size=10)

r = rospy.Rate(10)
scale = 1

t_end = time.time() + 1
while time.time() < t_end:
    pub_crane.publish(-0.25)
    # do whatever you do


group_variable_values = group.get_current_joint_values()

group_variable_values[0] = -pi/2
group_variable_values[1] = -pi/2
group_variable_values[2] = pi/2
group_variable_values[4] = pi/2

group.set_joint_value_target(group_variable_values)

plan2 = group.plan()

rospy.sleep(1)
group.go(wait=False)
rospy.sleep(1)

print("Reference frame: %s" % group.get_planning_frame())
print("End effector: %s" % group.get_end_effector_link())
print("Robot Groups:")
print(robot.get_group_names())
print("Current Joint Values:")
print(group.get_current_joint_values())
print("Current Pose:")
print(group.get_current_pose())
print("Robot State:")
print(robot.get_current_state())





waypoints = []

wpose = group.get_current_pose().pose


wpose.position.x += scale * 0.3  # First move up (z)
#wpose.position.y += scale * 0.2  # and sideways (y)
waypoints.append(copy.deepcopy(wpose))

# wpose.position.x += scale * 0.1  # Second move forward/backwards in (x)
# waypoints.append(copy.deepcopy(wpose))

# wpose.position.y -= scale * 0.1  # Third move sideways (y)
# waypoints.append(copy.deepcopy(wpose))

# We want the Cartesian path to be interpolated at a resolution of 1 cm
# which is why we will specify 0.01 as the eef_step in Cartesian
# translation.  We will disable the jump threshold by setting it to 0.0 disabling:
(plan, fraction) = group.compute_cartesian_path(
                                   waypoints,   # waypoints to follow
                                   0.01,        # eef_step
                                   0.0)         # jump_threshold


group.execute(plan, wait=True)

moveit_commander.roscpp_shutdown()


