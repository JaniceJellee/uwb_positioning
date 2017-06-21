#!/usr/bin/env python

import roshelper
# import math
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
DISTANCES = [.5, 1]
ANGLES = [30, 60, 90]

class Buttons(object):
    A = 0
    B = 1
    X = 2

@n.entry_point()
class JoystickCommandCenter(object):

    def __init__(self):
        # self.planner_enabled = False
        self.last_joy = Joy()
        self.state = False
        self.get_position_mochi = False
        self.get_position_home = False
        self.index = 0
        self.time = time.time()
        self.row = []
        self.tag_row = []
        self.home_row = []

        self.f = open(FILE_PATH, "wb")
        self.writer = csv.writer(self.f, delimiter=',', quotechar='"')
        self.writer.writerow(['predicted distance', 'tag transx', 'tag transy', 'tag transz', 'tag rotx', 
                'tag roty', 'tag rotz', 'tag rotw'] + ['home transx', 'home transy',
                'home transz', 'home rotx', 'home roty', 'home rotz', 'home rotw'])
        self.writer.writerow([])

    def empty_rows(self): 
        self.row = []
        self.tag_row = []
        self.home_row = []

    @n.subscriber(JOY_TOPIC, Joy)
    def joy_sub(self, joy):
        if joy.buttons[Buttons.A] > 0:
            rospy.loginfo("======================================")
            self.empty_rows()
            self.writer.writerow([])
            self.state = True
            self.time = time.time()
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
            if len(self.row) > 0 and len(self.tag_row) > 0 and len(self.home_row) > 0:
                self.row.extend(self.tag_row)
                self.row.extend(self.home_row)
                if len(self.row) == 15:
                    self.writer.writerow(self.row)
            self.empty_rows()
            rospy.loginfo(info)
            self.row.append(data.range)
            self.get_position_mochi = True
            self.get_position_home = True

    @n.subscriber("/vicon/mochi_uwb/mochi_uwb", TransformStamped)
    def tag_position(self, data):
        info = rospy.get_caller_id() + " : I heard %s" % data
        if self.state and self.get_position_mochi:
            rospy.loginfo(info)
            self.tag_row.extend([data.transform.translation.x, data.transform.translation.y,
                data.transform.translation.z, data.transform.rotation.x, data.transform.rotation.y,
                data.transform.rotation.z, data.transform.rotation.w])
            self.get_position_mochi = False

    @n.subscriber("/vicon/home_uwb/home_uwb", TransformStamped)
    def home_position(self, data):
        info = rospy.get_caller_id() + " : I heard %s" % data
        if self.state and self.get_position_home:
            rospy.loginfo(info)
            rospy.loginfo("--------------------------------------")
            self.home_row.extend([data.transform.translation.x, data.transform.translation.y,
                data.transform.translation.z, data.transform.rotation.x, data.transform.rotation.y,
                data.transform.rotation.z, data.transform.rotation.w]) 
            self.get_position_home = False       

    @n.main_loop(frequency=100)
    def run(self):
        pass

if __name__ == "__main__":
    n.start(spin=True)
