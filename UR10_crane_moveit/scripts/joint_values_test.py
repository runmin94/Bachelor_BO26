#!/usr/bin/env python

import sys
import copy
import rospy
import moveit_commander
import moveit_commander.move_group
import moveit_msgs.msg
from sensor_msgs.msg import JointState
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



def plan_cartesian_path(scale=1):
    

    waypoints = []

    state = robot.get_current_state()
    
    print("robot state before editing wpose.y: %s" %state)
    wpose = group.get_current_pose().pose
    
    print( "print out current pose:  %s"% wpose)
    wpose.position.y += 0.5  

    waypoints.append(copy.deepcopy(wpose))
    print("waypoints: %s"%waypoints)

    wpose.position.x += scale * 0.3  
    waypoints.append(copy.deepcopy(wpose))

    wpose.position.x -= scale * 0.4  
    waypoints.append(copy.deepcopy(wpose))

    (plan, fraction) = group.compute_cartesian_path(
                                       waypoints,   # waypoints to follow
                                       0.01,        # eef_step
                                       0.0)         # jump_threshold


    print("cart plan:  %s"%plan)
    return plan


def display_trajectory(plan):

    
    display_trajectory_publisher = display_trajectory_publisher


    display_trajectory = moveit_msgs.msg.DisplayTrajectory()
    display_trajectory.trajectory_start = robot.get_current_state()
    display_trajectory.trajectory.append(plan)
    # Publish
    display_trajectory_publisher.publish(display_trajectory);

    ## END_SUB_TUTORIAL

def execute_plan(plan):

    group.execute(plan, wait=True)


group_variable_values = group.get_current_joint_values()

print("startpose %s:" % group.get_current_pose().pose)

print("joint values: %s" % group_variable_values)

group_variable_values[0] = -pi/2
group_variable_values[1] = -pi/2
group_variable_values[2] = pi/2
group_variable_values[4] = pi/2

print("joint values after move: %s" % group_variable_values)


group.set_joint_value_target(group_variable_values)

print("pose after move:  %s" % group.get_current_pose().pose)

plan2 = group.plan()
group.set_start_state_to_current_state()


rospy.sleep(1)



plan_cart = plan_cartesian_path()
group.go(wait=False)
execute_plan(plan_cart)



rospy.sleep(5)

moveit_commander.roscpp_shutdown()


