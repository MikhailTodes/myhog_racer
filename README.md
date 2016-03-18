# MYHOG RACER

MYHOG racer stands for Myo Controlled Hemispherical Omni-directional Gimbaled Racer. It uses just one hemisphere as a drive force. With the hemisphere constantly being spun and making contact with the ground, the gimbal's tilt allows drive in any direction. The Myo is an armband worn just below the elbow of the driver. It uses a combination of EMG, IMU, and accelerometer signals to achieve machine trained gesture recognition that allows the driver speed and direction control of the MYHOG. 

This is a repository to store all the software and design of the MYHOG RACER.

##In this repo:
 * Model - This folder contains the Solid Work files for 3D printing and laser cutting the frame and gimble.
 * The SRC folder of the ROS workspace I used to send the serial signals to the MYHOG
 * A folder called xbee containing the C code used to program the PIC32