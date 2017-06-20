#!/usr/bin/env python
import rospy
import numpy as np
from sensor_msgs.msg import Range

current_distances = []
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s!", data)
    current_distances.append(data.range)
    print (current_distances)

def listener():

    rospy.init_node('tag_subscriber', anonymous=True)

    rospy.Subscriber("chatter", Range, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
