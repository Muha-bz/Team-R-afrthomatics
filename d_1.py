import zenoh
import json5
import time
import struct

import rospy
from clover import srv
from std_srvs.srv import Trigger
import math
from std_msgs.msg import Bool

rospy.init_node('flight')


config = {}
zenoh_config = zenoh.Config.from_json5(json5.dumps(config))
zenoh_session = zenoh.open(zenoh_config)

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_altitude = rospy.ServiceProxy('set_altitude', srv.SetAltitude)
set_yaw = rospy.ServiceProxy('set_yaw', srv.SetYaw)
set_yaw_rate = rospy.ServiceProxy('set_yaw_rate', srv.SetYawRate)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)
pub = rospy.Publisher("/spray", Bool, queue_size=1)

numDrone = 0


def navigate_wait(x=0, y=0.35, z=0.5,  yaw=float('nan'), speed=0.5, frame_id='', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z,yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)
    rospy.sleep(0.5)

def balon():
    navigate_wait(x=-0.05,z=1.1,frame_id='aruco_map')#start pose
    pub.publish(Bool(data=True))
    navigate_wait(x=-0.05,z=1.3,frame_id='aruco_map')
    navigate_wait(x=0.05,z=1.3,frame_id='aruco_map')
    navigate_wait(x=0.05,z=1.1,frame_id='aruco_map')
    navigate_wait(x=-0.05,z=1.1,frame_id='aruco_map')
    pub.publish(Bool(data=False))
    #pisky
    navigate_wait(x=0,z=1.3,frame_id='aruco_map')
    pub.publish(Bool(data=True))
    navigate_wait(x=0,z=1.35,frame_id='aruco_map')
    rospy.sleep(1)#for more spray from pshikalka
    pub.publish(Bool(data=False))
    return 0

def copter_vint():#po 30 cm
    navigate_wait(x=-0.5,z=1,frame_id='aruco_map')#start pose
    rospy.sleep(1)
    #first
    pub.publish(Bool(data=True))
    navigate_wait(x=-0.2,z=1,frame_id='aruco_map')
    pub.publish(Bool(data=False))
    navigate_wait(x=0.2,z=1,frame_id='aruco_map')
    #second
    pub.publish(Bool(data=True))
    navigate_wait(x=0.5,z=1,frame_id='aruco_map')
    pub.publish(Bool(data=False))
    return 0

def body(): #40 cm * 20 cm
    navigate_wait(x=-0.2,z=0.8,frame_id='aruco_map')#start pose
    pub.publish(Bool(data=True))
    navigate_wait(x=0.2,z=0.8,frame_id='aruco_map')
    navigate_wait(x=0.2,z=0.6,frame_id='aruco_map')
    navigate_wait(x=-0.2,z=0.6,frame_id='aruco_map')
    navigate_wait(x=-0.2,z=0.8,frame_id='aruco_map')
    pub.publish(Bool(data=False))
    return 0

def kvadrat():
    navigate_wait(x=-0.5,frame_id='aruco_map')
    rospy.sleep(2)
    pub.publish(Bool(data=True))
    navigate_wait(x=-0.5, z=1,frame_id='aruco_map')
    navigate_wait(x=0, z=1,frame_id='aruco_map')
    navigate_wait(x=0, z=0.5,frame_id='aruco_map')
    navigate_wait(x=-0.5,frame_id='aruco_map')
    pub.publish(Bool(data=False))
    return 0


def vistupi():
    navigate_wait(x=-0.4,z=0.9,frame_id='aruco_map')#start pose
    #first
    pub.publish(Bool(data=True))
    navigate_wait(x=-0.4,z=0.7,frame_id='aruco_map')
    navigate_wait(x=-0.2,z=0.7,frame_id='aruco_map')
    pub.publish(Bool(data=False))
    navigate_wait(x=-0.25,z=0.6,frame_id='aruco_map')
    pub.publish(Bool(data=True))
    #rospy.sleep(?)
    navigate_wait(x=-0.4,z=0.5,frame_id='aruco_map')
    pub.publish(Bool(data=False))
    #end first
    navigate_wait(x=0.8,z=0.5,frame_id='aruco_map')
    navigate_wait(x=0.4,z=0.9,frame_id='aruco_map')
    #second
    pub.publish(Bool(data=True))
    navigate_wait(x=0.4,z=0.7,frame_id='aruco_map')
    navigate_wait(x=0.2,z=0.7,frame_id='aruco_map')
    pub.publish(Bool(data=False))
    navigate_wait(x=0.25,z=0.6,frame_id='aruco_map')
    pub.publish(Bool(data=True))
    #rospy.sleep(?)
    navigate_wait(x=0.4,z=0.5,frame_id='aruco_map')
    pub.publish(Bool(data=False))
    return 0


def liveliness_callback(sample: zenoh.Sample):
    print(sample)
    global numDrone
    if sample.kind == zenoh.SampleKind.PUT:
        numDrone += 1
        print("New alive token", sample.key_expr)
    elif sample.kind == zenoh.SampleKind.DELETE:
        numDrone -= 1
        print("Dropped alive token", sample.key)


liveliness_token = zenoh_session.liveliness().declare_token("liveliness/drone/1")
liveliness_sub = zenoh_session.liveliness().declare_subscriber(
    "liveliness/drone/*", liveliness_callback, history=True
)

def main():
    tochka_st='aruco_32' #rename
    navigate_wait(y=-0.1, z=0.5, frame_id='body',auto_arm=True)
    #vzlet
#    balon()#1
    # copter_vint()#1
    # vistupi()#2 or 3

    kvadrat()

    """ in while cicle
    if numdrone: continue
    fall()
    """
    navigate_wait(y=0, z=0.4,frame_id=tochka_st)
    navigate_wait(y=0, z=0.3,frame_id=tochka_st)
    rospy.sleep(1)
    land()
    return 0


try:
    while numDrone < 2:
        print("waiting for other dromes")
        rospy.sleep(1)
    main()
    print("all Drone Connection!")
except BaseException as e:
    print(e)
    zenoh_session.close()
