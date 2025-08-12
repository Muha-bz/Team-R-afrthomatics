import rospy
from clover import srv
from std_srvs.srv import Trigger
import math

rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)


def navigate_wait(x=0, y=0, z=.5, speed=0.5, frame_id='', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)
    rospy.sleep(2)
#-1 ~ 1 hight 0.5 ~ 1.5
def street():
    navigate_wait(x=-1,frame_id='aruco_map')
    navigate_wait(x=1,frame_id='aruco_map')
    navigate_wait(x=0,frame_id='aruco_map')
    return 0

def kvadrat():
    navigate_wait(x=-0.5,frame_id='aruco_map')
    navigate_wait(x=-0.5, z=1.5,frame_id='aruco_map')
    navigate_wait(x=.5, z=1.5,frame_id='aruco_map')
    navigate_wait(x=.5, z=.5,frame_id='aruco_map')
    navigate_wait(x=0,frame_id='aruco_map')
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
    s=9
    navigate_wait(frame_id='body',auto_arm=True,speed=1)
    print('press 1 to 5 and 0 to exit')
    s=int(input())
    kvadrat()
    navigate_wait(z=.35,frame_id=tochka_st)
    land()
    return 0
    


if __name__=='__main__': 
    main()
