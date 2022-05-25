#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64


def move_group(h_beam,trolly,crane):
    # initiliaze
    rospy.init_node('move_h_beam', anonymous=False)

    # tell user how to stop TurtleBot
    rospy.loginfo("To stop gantry CTRL + C")



    # Create a publisher which can "talk" to TurtleBot and tell it to move
    pub_h_beam = rospy.Publisher('/gantry_crane/h_beam_controller/command', Float64, queue_size=10)
    pub_trolly = rospy.Publisher('/gantry_crane/trolly_controller/command', Float64, queue_size=10)
    pub_crane = rospy.Publisher('/gantry_crane/crane_controller/command', Float64, queue_size=10)


    #TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
    r = rospy.Rate(10);

    move_dict = {
    "h_beam": 0.0,
    "trolly": 0.0,
    "crane": 0.0
    }


    while not rospy.is_shutdown():
        # publish the velocity
        pub_h_beam.publish(h_beam)
        pub_trolly.publish(trolly)
        pub_crane.publish(crane)
        # wait for 0.1 seconds (10 HZ) and publish again
        r.sleep()

if __name__ == '__main__':
    try:
        print("please enter h_beam position: ")
        h_beam_input = float(raw_input())
        print("please enter trolly position: ")
        trolly_input = float(raw_input())
        print("please enter crane position: ")
        crane_input = float(raw_input())
        move_group(h_beam_input,trolly_input,crane_input)

    except:
        rospy.loginfo("gantry_crane_publisher node terminated.")
