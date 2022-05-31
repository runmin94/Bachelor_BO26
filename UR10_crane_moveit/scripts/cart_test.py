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
display_trajectory = moveit_msgs.msg.DisplayTrajectory()
display_robot = moveit_msgs.msg.DisplayRobotState()
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=1)

display_trajectory.trajectory_start = robot.get_current_state()



def plan_cartesian_path(scale=1):

    waypoints = []

    wpose = group.get_current_pose().pose
    wpose.position.z -= scale * 1  # First move up (z)
    wpose.position.y -= scale * 0.5  # and sideways (y)
    waypoints.append(copy.deepcopy(wpose))

    wpose.position.x -= scale * 0.5  # Second move forward/backwards in (x)
    waypoints.append(copy.deepcopy(wpose))

    wpose.position.y -= scale * 0.1  # Third move sideways (y)
    waypoints.append(copy.deepcopy(wpose))

    
    wpose.position.y -= scale * 0.5  # and sideways (y)
    waypoints.append(copy.deepcopy(wpose))



    (plan, fraction) = group.compute_cartesian_path(
                                        waypoints,   # waypoints to follow
                                        0.01,        # eef_step
                                        0.0)         # jump_threshold

  
    return plan, fraction



def display_trajectory(plan):

    display_trajectory = moveit_msgs.msg.DisplayTrajectory()
    display_trajectory.trajectory_start = robot.get_current_state()
    display_trajectory.trajectory.append(plan)

    display_trajectory_publisher.publish(display_trajectory);



def execute_plan(plan):

    group.execute(plan, wait=True)

    print("___________Current pose_____________:  %s" % group.get_current_pose().pose)


def main():
  try:

    print "============ Press `Enter` to plan and display a Cartesian path ..."
    raw_input()
    cartesian_plan, fraction = plan_cartesian_path()

    print "============ Press `Enter` to display a saved trajectory (this will replay the Cartesian path)  ..."
    raw_input()
    display_trajectory(cartesian_plan)

    print "============ Press `Enter` to execute a saved path ..."
    raw_input()
    execute_plan(cartesian_plan)



    print "============ Python tutorial demo complete!"
  except rospy.ROSInterruptException:
    return
  except KeyboardInterrupt:
    return

if __name__ == '__main__':
  main()




rospy.sleep(5)

moveit_commander.roscpp_shutdown()


