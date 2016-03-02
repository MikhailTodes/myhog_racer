#!/usr/bin/env python
import rospy
from std_msgs.msg import UInt8
import serial

gest = 0

cnt = 0


def callback(data):
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

    xbee.flushInput()
    xbee.flushOutput()

    rospy.sleep(0.2)
    
    #global cnt
    #msg = "{0:d}test\n".format(cnt)
    global gest
    
    if (data.data ==1):
        gest = 1501
    elif(data.data==2):
        gest = 2000
    elif(data.data==3):
        gest = 4000
    elif(data.data==4):
        gest = 5000
    elif(data.data==5):
        gest = 5999
    else:
        gest = 3750
    
    msg = "{0:d},{0:d},{0:d}\n".format(gest,gest,gest)
    print msg
    xbee.write(msg)
    rospy.sleep(0.2)
    xbee.flushInput()
    xbee.flushOutput()

    #cnt += 1
    
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", msg)
    xbee.close()
    
if __name__ == '__main__':


    rospy.init_node('serial_send', anonymous=True)
    
    rospy.Subscriber("/myo_gest", UInt8, callback)
    
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
