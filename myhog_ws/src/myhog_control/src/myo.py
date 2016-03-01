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
    
    global cnt
    msg = "{0:d}ffffffffffffffffff\n".format(cnt)
    xbee.write(msg)
    # for a in msg:
    #     xbee.write(a)
    #     rospy.sleep(0.01)
    print msg
    rospy.sleep(0.2)
    xbee.flushInput()
    xbee.flushOutput()

    cnt += 1
    
    # gest = data.data
    # global cnt
    # # msg = "{0:d}num\r\n".format(cnt)
    # cnt += 1
    # msg = ['1','2','3','\r','\n']
    # # xbee.write('\x31\x32\x33\x0d\x0a')
    # # xbee.write("123\r\n")
    # # xbee.write(''.join(map(chr,msg)))
    # # msg = [49, 50, 51, 13, 10]
    # print msg
    # # xbee.setRTS(level=0)
    # for a in msg:
    #     xbee.write(a)
    #     rospy.sleep(0.01)
    #     xbee.flushInput()
    #     xbee.flushOutput()
    # # xbee.setRTS(level=1)
    # # xbee.write(msg)
    # rospy.sleep(0.2)
    
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", xbee.portstr)
    xbee.close()
 
if __name__ == '__main__':


    rospy.init_node('serial_send', anonymous=True)
 
    rospy.Subscriber("/myo_gest", UInt8, callback)
 
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
