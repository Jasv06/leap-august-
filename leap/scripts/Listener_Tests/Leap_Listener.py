import rospy
import numpy as np
import ray
import roslib
from std_msgs.msg import Float32
from geometry_msgs.msg import Point
from std_msgs.msg import Int32 
from leap.msg import *

x_coord = 0.0 
y_coord = 0.0
z_coord = 0.0

def LeapXYZ(data): 
   
   global x_coord 
   global y_coord 
   global z_coord
   
   x_coord = data.x
   y_coord = data.y
   z_coord = data.z
   #rospy.loginfo(x_coord)
   
#def Leap(data):
#   rospy.loginfo(rospy.get_caller_id() + " Y: %f", data.data)
      
      
def listener():
  
   rospy.init_node('Leap_ros_data')
   
   r = rospy.Rate(100)
   
   pub = rospy.Publisher("/rx150/commands/joint_group", JointGroupCommand, queue_size = 1)
   print("Sending messages to the robot!")
   while not rospy.is_shutdown():
      
      msg = JointGroupCommand()
         
      rospy.Subscriber("/Leap/XYZ", Point)
      rospy.Subscriber("/Leap_Hand_OPENorCLOSE", Float32)
      rospy.Subscriber("/WhichHandisit", Float32)
      rospy.Subscriber("/LeapHandAngles", Point)
      rospy.Subscriber("/Stable_Pos", Point, LeapXYZ)
      rospy.Subscriber("/Hand_velocity", Point)
     
      
      print(x_coord)
      print(y_coord)
      print(z_coord)
     
        
      waist = x_coord
      shoulder = -1*y_coord
      elbow = z_coord
      
      msg.name = 'arm'
      msg.cmd = [waist,shoulder,elbow,0,0]
      
      #rospy.loginfo(msg)
      pub.publish(msg)
      rospy.sleep(2)
      #r.sleep()
      #point = Point()
    
     
   
if __name__ == '__main__':
     try:
       listener()
     except rospy.ROSInterruptException:
       pass

