#! /usr/bin/env python

import rospy
import random
from std_msgs.msg import Int64
from communication_tutorial.msg import rand_num

def callback(data):
   rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

def listener():

   # In ROS, nodes are uniquely named. If two nodes with the same
   # name are launched, the previous one is kicked off. The
   # anonymous=True flag means that rospy will choose a unique
   # name for our 'listener' node so that multiple listeners can
   # run simultaneously.
   rospy.init_node('tf_listener_check', anonymous=True)

   rospy.Subscriber("gantry_crane/crane_link", String, callback)

   # spin() simply keeps python from exiting until this node is stopped
   rospy.spin()

# def talker():
#    pub = rospy.Publisher('chatter', String, queue_size=10)
#    rospy.init_node('talker', anonymous=True)
#    rate = rospy.Rate(10) # 10hz
#    while not rospy.is_shutdown():
#       hello_str = "hello world %s" % rospy.get_time()
#       rospy.loginfo(hello_str)
#       pub.publish(hello_str)
#       rate.sleep()


if __name__ == '__main__':
   listener()
