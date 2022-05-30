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
pose_goal.orientation.w = 1.0
pose_goal.orientation.x = -0.5
pose_goal.orientation.y = 0.5
pose_goal.orientation.z = 2.0
pose_goal.position.x = 0.7
pose_goal.position.y = 0.7
pose_goal.position.z = 2
move_group.set_pose_target(pose_goal)

plan1 = move_group.plan()
print("pose target: %s" % pose_goal)
#print("target pose: %s" % )
## Now, we call the planner to compute the plan and execute it.

pose_goal2.orientation.w = 1.0
pose_goal2.orientation.x = -0.5
pose_goal2.orientation.y = 0.5
pose_goal2.orientation.z = 2.0
pose_goal2.position.x = -0.7
pose_goal2.position.y = -0.7
pose_goal2.position.z = 2

move_group.clear_pose_targets()

move_group.set_pose_target(pose_goal2)

plan2 = move_group.plan()

move_group.execute(plan1, wait=True)

move_group.execute(plan2, wait=True)




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


