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
    #msg = "{0:d}\n".format(cnt)
    global gest
    
    if (data.data ==1){
        gest = 151
    }else if(data.data==2){
        gest = 200
    }else if(data.data==3){
        gest = 400
    }else if(data.data==4){
        gest = 500
    }else if(data.data==5){
        gest = 599
    }else{
        gest = 375
    }

    msg = "" + str(gest) + "," + str(gest) + "," + str(gest)
    #print msg
    xbee.write(msg.encode())
    print msg
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
