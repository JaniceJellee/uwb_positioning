#!/usr/bin/env python

import roshelper
# import math
import rospy
from sensor_msgs.msg import Joy
from sensor_msgs.msg import Range
import csv
import time

NODE_NAME = "joystick"
n = roshelper.Node(NODE_NAME, anonymous=False)
JOY_TOPIC = "joy"

FILE_PATH = "/home/flyingcar/catkin_ws/src/decawave_localization/nodes/data.csv"
DISTANCES = [.5, 1]
ANGLES = [30, 60, 90]

class Buttons(object):
    A = 1
    B = 2
    X = 0

@n.entry_point()
class JoystickCommandCenter(object):

    def __init__(self):
        # self.planner_enabled = False
        self.last_joy = Joy()
        self.state = False
        self.index = 0
        self.time = time.time()

        self.tests = []
        for distance in DISTANCES:
            for angle in ANGLES:
                self.tests.append((distance, angle))
        self.f = open(FILE_PATH, "wb")
        self.writer = csv.writer(self.f, delimiter=',', quotechar='"')
        self.writer.writerow(['DATA'])
        self.writer.writerow(['seq', 'stamp secs', 'stamp_nsecs', 'frame_id', 
                'radiation_type', 'field_of_view', 'min_range', 'max_range', 'range'])

    def on_button_click(self, joy, btn, func):
        update = abs(self.last_joy.buttons[btn] - joy.buttons[btn]) > 0
        if joy.buttons[btn] > 0 and update:
            func()

    @n.subscriber(JOY_TOPIC, Joy)
    def joy_sub(self, joy):
        if joy.buttons[Buttons.A] > 0:
            distance, angle =  self.tests[self.index]
            rospy.loginfo("======================================")
            rospy.loginfo("DISTANCE: " + str(distance) + "m, ANGLE: " + str(angle) + "")
            self.writer = csv.writer(self.f, delimiter=',', quotechar='"')
            self.writer.writerow(["distance", distance, "angle", angle])
            self.state = True
            self.time = time.time()

        if joy.buttons[Buttons.B] > 0:
            self.state = False
            self.index += 1
            if self.index < len(self.tests):
                distance, angle =  self.tests[self.index]
                rospy.loginfo("DONE! Next: ")
                rospy.loginfo("DISTANCE: " + str(distance) + "m, ANGLE: " + str(angle) + u"\u00b0")
                self.writer = csv.writer(self.f, delimiter=',', quotechar='"')
                self.writer.writerow([])
            else:
                self.f.close()
                rospy.loginfo("======================================")
                rospy.loginfo("FINISHED")

        self.last_joy = joy

    @n.subscriber(JOY_TOPIC, Joy)
    def joy_close(self, joy):
        if joy.buttons[Buttons.X] > 0:
            self.state = False
            self.f.close()
            rospy.loginfo("======================================")
            rospy.loginfo("CLOSED FILE")

    @n.subscriber("chatter", Range)
    def record_and_print_data(self, data):
        info = rospy.get_caller_id() + " : I heard %s" % data
        if self.state and (time.time() - self.time < 3):
            rospy.loginfo(info)
            self.writer = csv.writer(self.f, delimiter=',', quotechar='"')
            self.writer.writerow([data.header.seq, data.header.stamp.secs, data.header.stamp.nsecs, data.header.frame_id, 
                data.radiation_type, data.field_of_view, data.min_range, data.max_range, data.range])

    # @n.subscriber("chatter", Range)
    # def print_all_data(self, data):
    #     info = rospy.get_caller_id() + " : I heard %s" % data
    #     rospy.loginfo(info)

    @n.main_loop(frequency=100)
    def run(self):
        pass

if __name__ == "__main__":
    n.start(spin=True)