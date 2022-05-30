#!/usr/bin/env python

from shutil import move
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial', anonymous=True)

robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
group_name = "UR10_group"    
move_group = moveit_commander.MoveGroupCommander(group_name)
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=1)

scale = 1
waypoints = []

state = robot.get_current_state()
print(state)
wpose = move_group.get_current_pose().pose
print(wpose)
wpose.position.x += scale * -0.5  # First move up (z)
wpose.position.y += scale * -0.2  # and sideways (y)
waypoints.append(copy.deepcopy(wpose))

wpose.position.x += scale * 0.3  # Second move forward/backwards in (x)
waypoints.append(copy.deepcopy(wpose))

wpose.position.z -= scale * 0.4  # Third move sideways (y)
waypoints.append(copy.deepcopy(wpose))


(fraction, plan) = move_group.compute_cartesian_path(waypoints, 0.01, 0.0)

move_group.execute(plan, wait=True)






# Calling `stop()` ensures that there is no residual movement
move_group.stop()
# It is always good to clear your targets after planning with poses.
# Note: there is no equivalent function for clear_joint_value_targets()
move_group.clear_pose_targets()

## END_SUB_TUTORIAL

# For testing:
# Note that since this section of code will not be included in the tutorials
# we use the class variable rather than the copied state variable
current_pose = move_group.get_current_pose()
print("current pose: %s" % current_pose)
moveit_commander.roscpp_shutdown()


