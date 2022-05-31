#!/usr/bin/env python

import sys
import copy
import rospy
from math import pi
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

eef_link = move_group.get_end_effector_link()
print "============ End effector link: %s" % eef_link

pose_frame = move_group.get_pose_reference_frame()
print "============ pose reference frame: %s" % pose_frame

planning_frame = move_group.get_planning_frame()
print "============ planning frame: %s" % planning_frame

pose_goals = []

pose_goal = geometry_msgs.msg.Pose()
pose_goal2 = geometry_msgs.msg.Pose()
print("pose target: %s" % pose_goal)
print("pose %s" % move_group.get_current_pose())
print("current pose typ %s" % type(move_group.get_current_pose()))
print( "pose target type %s" % type(pose_goal))
move_group.set_start_state_to_current_state()
pose_goal.orientation.w = -5
pose_goal.orientation.x = -10
pose_goal.orientation.y = -10
pose_goal.orientation.z = 1
pose_goal.position.x = 0.7
pose_goal.position.y = 0.7
pose_goal.position.z = 2
move_group.set_pose_target(pose_goal)

plan1 = move_group.plan()
move_group.execute(plan1, wait=True)
print("pose target: %s" % pose_goal)
#print("target pose: %s" % )
## Now, we call the planner to compute the plan and execute it.

group_variable_values = move_group.get_current_joint_values()

print("startpose %s:" % move_group.get_current_pose().pose)

print("joint values: %s" % group_variable_values)

group_variable_values[0] = -pi/2
group_variable_values[1] = -pi/2
group_variable_values[2] = pi/2
group_variable_values[4] = pi/2

print("joint values after move: %s" % group_variable_values)


move_group.set_joint_value_target(group_variable_values)

print("pose after move:  %s" % move_group.get_current_pose().pose)

plan2 = move_group.plan()
move_group.set_start_state_to_current_state()

print("pose after move:  %s" % move_group.get_current_pose().pose)



rospy.sleep(1)




move_group.go(wait=False)


# pose_goal2.orientation.w = -1.0
# pose_goal2.orientation.x = pi/2
# pose_goal2.orientation.y = pi/2
# pose_goal2.orientation.z = pi/2
# pose_goal2.position.x = -0.5
# pose_goal2.position.y = -0.5
# pose_goal2.position.z = 1.7



# move_group.clear_pose_targets()

#move_group.set_pose_target([-0.5, 0.5, 1.7, 0, -pi/2, 0])
# move_group.set_start_state_to_current_state()
# plan2 = move_group.plan()




#move_group.execute(plan2, wait=True)

#move_group.set_position_target(0.2 0.2 1.5)




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


