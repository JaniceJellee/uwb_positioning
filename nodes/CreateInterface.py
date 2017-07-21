from enum import IntEnum
import serial
import struct
from math import *
import sys
import time

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


def main():
    CRC = CreateRobotCmd('/dev/ttyUSB0',Create_OpMode.Full,Create_DriveMode.Direct)
    print CRC.port.isOpen()
    if CRC.port.isOpen() or DEBUG:
        print "starting"
        CRC.start()
        
        # time.sleep(5)
        # CRC.directDrive(-60,-60)
        # time.sleep(10)
        # CRC.directDrive(-70,-70)
        # time.sleep(5)

        time.sleep(5)
        CRC.directDrive(60,60)
        time.sleep(5)
        # uwb
        # CRC.directDrive(-70,70)
        # time.sleep(5)                
        # CRC.stop()
        # return 0
        # for i in range(0,2):
        #     # CRC.directDrive(50,50)
        #     print 1
        #     time.sleep(5)
        #     CRC.directDrive(0,-80)
        #     print 2
        #     time.sleep(5)
        #     CRC.directDrive(-80,0)
        #     print 3
            # time.sleep(5)
            # print 4
            # CRC.directDrive(-50,-50)
            # time.sleep(10)
            # time.sleep(2)
            # CRC.drive(5*pow(10,(i+1)),100)
            # time.sleep(5)
            #CRC.drive(5,100)
        
        CRC.stop()
        #CRC.start()
        print "Done"
        return 0

if __name__ == "__main__":
    sys.exit(int(main() or 0))
