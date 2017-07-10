#!/usr/bin/env python

import roshelper
import rospy
from sensor_msgs.msg import Joy
from sensor_msgs.msg import Range
from geometry_msgs.msg import TransformStamped
import csv
import time

NODE_NAME = "joystick_record"
n = roshelper.Node(NODE_NAME, anonymous=False)
JOY_TOPIC = "joy"

FILE_PATH = "/home/rcac/foresight_ws/src/uwb_variance/nodes/data.csv"

class Buttons(object):
    A = 0
    B = 1
    X = 2

@n.entry_point()
class JoystickCommandCenter(object):

    def __init__(self):
        self.last_joy = Joy()
        self.state = False
        self.time = time.time()
        self.msg = False
        self.f = open(FILE_PATH, "wb")
        self.writer = csv.writer(self.f, delimiter=',', quotechar='"')

    @n.subscriber(JOY_TOPIC, Joy)
    def joy_sub(self, joy):
        if joy.buttons[Buttons.A] > 0:
            rospy.loginfo("======================================")
            self.writer.writerow([])
            self.state = True
            self.time = time.time()
            self.msg = True
        if joy.buttons[Buttons.B] > 0:
            self.state = False
        self.last_joy = joy

    @n.subscriber(JOY_TOPIC, Joy)
    def joy_close(self, joy):
        if joy.buttons[Buttons.X] > 0:
            self.state = False
            self.f.close()
            rospy.loginfo("======================================")
            rospy.loginfo("CLOSED FILE")

    @n.subscriber("/mochi_uwb/range", Range)
    def uwb_range(self, data):
        info = rospy.get_caller_id() + " : I heard %s" % data
        if self.state and (time.time() - self.time < 5):
            rospy.loginfo(info)
            self.writer.writerow([data.range])
        elif self.msg:
            rospy.loginfo("DDDD\n \
                           D   D\n \
                           D   D\n \
                           D   D\n \
                           DDDD\n \
                           \n\
                            OOOOO\n \
                           O   O\n \
                           O   O\n \
                           O   O\n \
                           OOOOO\n \
                           \n\
                            N   N\n \
                           NN  N\n \
                           N N N\n \
                           N  NN\n \
                           N   N\n \
                           \n\
                            EEEEE\n \
                           E\n \
                           EEEEE\n \
                           E\n \
                           EEEEE\n")
            self.msg = False

    @n.main_loop(frequency=100)
    def run(self):
        pass

if __name__ == "__main__":
    n.start(spin=True)
