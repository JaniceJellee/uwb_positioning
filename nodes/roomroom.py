#!/usr/bin/env python

import roshelper
import rospy
from sensor_msgs.msg import Joy
from sensor_msgs.msg import Range
from geometry_msgs.msg import TransformStamped
import time

from enum import IntEnum
import serial
import struct
from math import *
import sys
import time

NODE_NAME = "roomroom"
n = roshelper.Node(NODE_NAME, anonymous=False)
JOY_TOPIC = "joy"

class Buttons(object):
    A = 0
    B = 1
    X = 2
    Y = 3
    LB = 4
    RB = 5

###################################################

DEBUG = False#True
NO_SERIAL = False

class Create_OpMode(IntEnum):
    Passive = 130
    Safe = 131
    Full = 132

class Create_DriveMode(IntEnum):
    Drive = 137
    Direct = 145

class Create_Commands(IntEnum):
    Start = 128

def minMax(min_val,max_val,val):
    return max(min_val,min(val,max_val))

class CreateRobotCmd(object):
    def __init__(self,port,OpMode,DriveMode):
        '''Opens Serial Port'''
        # These are hard limits in the create which are hard coded in
        self.rmin = -2000.0
        self.rmax = 2000.0
        self.vmin = -500.0
        self.vmax = 500.0
        # opp mode is either Pasisve, safe, or full. Always use full 
        self.opmode = OpMode
        #information on drive mode is bellow and in documentation
        self.drivemode = DriveMode
        #Serial port baud is currently hard coded
        if NO_SERIAL:
            self.port = serial.Serial()
        else:
            self.port = serial.Serial(port,57600,parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE,xonxoff=False,timeout=10.0)

    def start(self):
        self._writeCommand(Create_Commands.Start)
        self._writeCommand(self.opmode)

    def stop(self):
        '''Stops movement and sets the device to passive'''
        self.directDrive(0,0)
        self.opmode = Create_OpMode.Passive
        self._writeCommand(Create_OpMode.Passive)
        #self.port.close()



    def _writeCommand(self,cmd):
        '''the input type should be a string, int, or Create_ value
           int is converted to a char string,
           strings are passed through'''
        if (type(cmd) == type(Create_Commands.Start) or 
            type(cmd) == type(Create_OpMode.Full) or 
            type(cmd) == type(Create_DriveMode.Direct) ):
            cmd = int(cmd)

        if type(cmd) == int:
            cmd = str(chr(cmd))
        elif type(cmd) == type(None):
            print "huh"
            return

        nb = len(cmd)
        if not NO_SERIAL:
            nb_written = self.port.write(cmd)
            if (nb != nb_written):print "Error only wrote %i not %i bytes"%(nb_written,nb)
        if DEBUG:
            int_form = []
            for i in range(0,nb):
                int_form.append(int(ord(cmd[i])))
            print cmd
            print int_form


    def demo(self):
        cmd = struct.pack('B',136)+struct.pack('B',2)
        self._writeCommand(cmd)

    def _makecmd(self,head,one,two):
        return struct.pack('B',head)+struct.pack('>h',one)+struct.pack('>h',two)


    def drive(self,Radius,Velocity):
        '''This mode uses radii and velocity for turning
            straight requires R=None
            Clockwise and Counterclockwise in place are R=0
        '''
        if (self.drivemode != Create_DriveMode.Drive): self.self.drivemode =Create_DriveMode.Drive

        Velocity =  minMax(self.vmin,self.vmax,Velocity)

        if Radius == None:
            Radius = 32767
        elif Radius ==0 and Velocity >0:
            Radius =int('0xFFFF',0)
        elif Radius ==0 and Velocity <0:
            Radius =int('0x0001',0)
        else:
            Radius = minMax(self.rmin,self.rmax,Radius)
        cmd = self._makecmd(int(self.drivemode),int(Velocity),int(Radius))
        self._writeCommand(cmd)

    def directDrive(self,V1,V2):
        '''The direct drive mode allows control over right and left wheels directly. This uses v1 for R and V2 for L'''
        if (self.drivemode != Create_DriveMode.Direct): self.drivemode = Create_DriveMode.Direct

        V1 = minMax(self.vmin,self.vmax,V1)
        V2 = minMax(self.vmin,self.vmax,V2)

        cmd = self._makecmd(int(self.drivemode),int(V1),int(V2))
        self._writeCommand(cmd)

####################################################

@n.entry_point()
class JoystickCommandCenter(object):

    def __init__(self):
        self.last_joy = Joy()
        self.time = time.time()
        self.CRC = CreateRobotCmd('/dev/ttyUSB0',Create_OpMode.Full,Create_DriveMode.Direct)
        if self.CRC.port.isOpen():
            print "starting"
        self.CRC.start()

    # def on_button_click(self, joy, btn, func):
    #     update = abs(self.last_joy.buttons[btn] - joy.buttons[btn]) > 0
    #     if joy.buttons[btn] > 0 and update:
    #         func()

    # @n.subscriber(JOY_TOPIC, Joy)
    # def joy_sub(self, joy):
    #   if joy.buttons[Buttons.Y] > 0:
    #       self.on_button_click(joy, Buttons.Y, self.forward())
    #   if joy.buttons[Buttons.A] > 0:
    #       self.on_button_click(joy, Buttons.A, self.backward())
    #   if joy.buttons[Buttons.B] > 0:
    #       self.on_button_click(joy, Buttons.B, self.turn_left())
    #   if joy.buttons[Buttons.X] > 0:
    #       self.on_button_click(joy, Buttons.X, self.turn_right())
    #   self.last_joy = joy

    # def turn_left(self):
    #     rospy.loginfo("turning left")
    #     self.CRC.directDrive(60,0)

    # def turn_right(self):
    #     rospy.loginfo("turning right")
    #     self.CRC.directDrive(0,60)

    # def forward(self):
    #     rospy.loginfo("forwards")
    #     self.CRC.directDrive(20,20)

    # def backward(self):
    #     rospy.loginfo("backwards")
    #     self.CRC.directDrive(-60,-60)

    @n.subscriber(JOY_TOPIC, Joy)
    def turning(self, joy):
        if joy.buttons[Buttons.X] > 0:
            rospy.loginfo("turning left")
            self.CRC.directDrive(60,0)
        elif joy.buttons[Buttons.B] > 0:
            rospy.loginfo("turning right")
            self.CRC.directDrive(0,60)
        self.last_joy = joy

    @n.subscriber(JOY_TOPIC, Joy)
    def straight(self, joy):
        if joy.buttons[Buttons.Y] > 0:
            rospy.loginfo("moving forward")
            self.CRC.directDrive(60,60)
        elif joy.buttons[Buttons.A] > 0:
            rospy.loginfo("moving backward")
            self.CRC.directDrive(-60,-60)
        self.last_joy = joy

    @n.subscriber(JOY_TOPIC, Joy)
    def done(self, joy):
        if joy.buttons[Buttons.RB] > 0:
            rospy.loginfo("stopped")
            self.CRC.stop()


    @n.main_loop(frequency=100)
    def run(self):
        pass

if __name__ == "__main__":
    n.start(spin=True)
