#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64


def move_group():
    # initiliaze
    rospy.init_node('move_h_beam', anonymous=False)

    # tell user how to stop TurtleBot
    rospy.loginfo("To stop gantry CTRL + C")

    # publisher for moving crane
    pub_h_beam = rospy.Publisher('/gantry_crane/h_beam_controller/command', Float64, queue_size=10)
    pub_trolly = rospy.Publisher('/gantry_crane/trolly_controller/command', Float64, queue_size=10)
    pub_crane = rospy.Publisher('/gantry_crane/crane_controller/command', Float64, queue_size=10)


    #publisher rate
    r = rospy.Rate(10);

    #dictionary for move group
    move_dict = {
    "h_beam": 2.0,
    "trolly": 1.5,
    "crane": -1.0
    }

    while not rospy.is_shutdown():
        # publishes the positions based on the move_dict
        pub_h_beam.publish(move_dict["h_beam"])
        pub_trolly.publish(move_dict["trolly"])
        pub_crane.publish(move_dict["crane"])
        # wait for 0.1 seconds (10 HZ) and publish agai
        r.sleep()

if __name__ == '__main__':
    try:
        move_group()

    except:
        rospy.loginfo("gantry_crane_publisher node terminated.")
