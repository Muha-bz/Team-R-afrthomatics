import rospy
from clover import srv
from std_srvs.srv import Trigger
import math
from std_msgs.msg import Bool

rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)
pub = rospy.Publisher("/spray", Bool, queue_size=1)
# Издатель скорректированной позы

def navigate_wait(x=0, y=0.35, z=0.5,  yaw=float('nan'), speed=0.5, frame_id='', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z,yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)
    rospy.sleep(0.5)
#-1 ~ 1 hight 0.5 ~ 1.5
def street():
    navigate_wait(x=-1,frame_id='aruco_map')
    navigate_wait(x=1,frame_id='aruco_map')
    navigate_wait(x=0,frame_id='aruco_map')
    return 0

def kvadrat():
    navigate_wait(x=-0.25,frame_id='aruco_map')
    navigate_wait(x=-0.25, z=1,frame_id='aruco_map')
    navigate_wait(x=0.25, z=1,frame_id='aruco_map')
    navigate_wait(x=0.25, z=0.5,frame_id='aruco_map')
    navigate_wait(x=-0.25,frame_id='aruco_map')
    return 0
def angl():
    navigate_wait(x=-1,z=1.5,frame_id='aruco_map')
    navigate_wait(x=1, z=1.5,frame_id='aruco_map')
    navigate_wait(frame_id='aruco_map')
    return 0

def circul():
    for x in range(0,1,0.1): pass
    return 0
def oval(): return 0

def main():
    tochka_st='aruco_32'
    navigate_wait(y=-0.1, frame_id='body',auto_arm=True)
    print("1")
    #navigate(yaw=math.radians(90), frame_id='body')
    pub.publish(Bool(data=True))
    print("2")

    kvadrat()
    print("3")
    pub.publish(Bool(data=False))
    navigate_wait(y=0, z=0.4,frame_id=tochka_st)
    navigate_wait(y=0, z=0.3,frame_id=tochka_st)
    rospy.sleep(1)
    land()
    return 0



if __name__=='__main__':
    main()

