#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
import serial

gest = 0
yaw = 3750
pitch = 3750

def xbeeSend(event):
   
    xbee.flushInput()
    xbee.flushOutput()
    
    global gest
    global yaw
    global pitch
    
    msg = "{:d},{:d},{:d}\n".format(gest,pitch,yaw)
    xbee.write(msg)
    print msg
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", msg)


def joyCB(data):

    global yaw
    global pitch
    global gest
    
    #if (data.data == 1):#Turn the motor on
    #    gest = 3100
    #else:
    #    gest = 1800
    
    y = 100*data.axes[0]
    p = 100*data.axes[1]

    #y = (y*57.3065)
    #if (y>0): #positive y
    #    y = (((-180+y)+90)*(25))+1500
    #else: #negative y
    #    y = (((180+y)+90)*(25))+1500
    #p = (((p*57.3065)+90)*(25))+1500

    yaw = int(y)
    pitch = int(p)
  
    
def closingStatements():
    xbee.close()
    print "Thank you for playing!"


if __name__ == '__main__':

    xbee = serial.Serial(
        port='/dev/ttyUSB0', 
        baudrate=57600, 
        timeout=1,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        rtscts=False,
        dsrdtr=False
    )

    rospy.init_node('serial_send', anonymous=True)

    rospy.Timer(rospy.Duration(0.1), xbeeSend)#Every tenth of a second - edit later to push for speed
    
    rospy.Subscriber("/joy", Joy, joyCB)
    
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

    rospy.on_shutdown(closingStatements)
    
