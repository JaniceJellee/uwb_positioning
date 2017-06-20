#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + " I heard %s!! ", data)

def listener():

    rospy.init_node('teleop_subscriber', anonymous=True)

    # global current_distances
    rospy.Subscriber("joy", Joy, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
