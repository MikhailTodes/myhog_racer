#!/usr/bin/env python
import rospy
from std_msgs.msg import UInt8
from sensor_msgs.msg import Imu
import tf
import serial

gest = 0
yaw = 3750
pitch = 3750

def xbeeSend(event):
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
    global gest
    global yaw
    global pitch
        
    msg = "{:d},{:d},{:d}\n".format(gest,pitch,yaw)
    print msg
    xbee.write(msg)

    rospy.sleep(0.2)
    xbee.flushInput()
    xbee.flushOutput()
    
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", msg)
    xbee.close()


def gestCallback(data):
#    xbee = serial.Serial(
#        port='/dev/ttyUSB0', 
#        baudrate=57600, 
#        timeout=1,
#        parity=serial.PARITY_NONE,
#        stopbits=serial.STOPBITS_ONE,
#        bytesize=serial.EIGHTBITS,
#        rtscts=False,
#        dsrdtr=False
#    )
#
#    xbee.flushInput()
#    xbee.flushOutput()
#    rospy.sleep(0.2)    
    global gest
    global yaw
    global pitch
    
    if (data.data == 1):
        gest = 3800
    else:
        gest = 0
    
#    msg = "{:d},{:d},{:d}\n".format(gest,pitch,yaw)
#    print msg
#    xbee.write(msg)


 #   rospy.sleep(0.2)
 #   xbee.flushInput()
 #   xbee.flushOutput()
    
 #   rospy.loginfo(rospy.get_caller_id() + "I heard %s", msg)
 #   xbee.close()


def imuCallback(data):
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
    global gest
    global yaw
    global pitch
    
    (roll, pitch, yaw) = tf.transformations.euler_from_quaternion([data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w])
    
    msg = "{:d},{:d},{:d}\n".format(gest,pitch,yaw)
    print msg
    xbee.write(msg)
    rospy.sleep(0.2)
    xbee.flushInput()
    xbee.flushOutput()
    
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", msg)
    xbee.close()    




if __name__ == '__main__':


    rospy.init_node('serial_send', anonymous=True)

    rospy.Timer(rospy.Duration(0.5), xbeeSend)
    
    rospy.Subscriber("/myo_gest", UInt8, gestCallback)
    #rospy.Subscriber("/myo_imu", Imu, imuCallback)
    
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
