import rospy
import numpy as np
import ray
import roslib
from interbotix_xs_modules.arm import InterbotixManipulatorXS
from std_msgs.msg import Float32
from geometry_msgs.msg import Point
from std_msgs.msg import Int32 
from leap.msg import *

x_coordi = 0.3 
y_coordi = 0.0
z_coordi = 0.2
other =  0.0
otro = 0.0
otroo = 0.0


bot = InterbotixManipulatorXS("rx150","arm","gripper")
#bot.arm.set_ee_pose_components(x=0.3,z=0.2,moving_time = 2)
bot.arm.go_to_home_pose()
#bot.arm.go_to_sleep_pose()
def LeapXYZg(data): 
   
   global x_coordi 
   global y_coordi 
   global z_coordi
   global other
   global otro
   global otroo
   
   x_coordi = data.x
   y_coordi = data.y
   z_coordi = data.z  
   other = data.x
   otro = data.y
   otroo = data.z
   
def listenerr():
  
   rospy.init_node('rx150_robot_manipulation')
   
   #r = rospy.Rate(100)
   
   #pub = rospy.Publisher("/rx150/commands/joint_group", JointGroupCommand, queue_size = 1)
   print("Sending messages to the robot!")
   while not rospy.is_shutdown():
      global otro
      #msg = JointGroupCommand()
         
      rospy.Subscriber("/Leap/XYZ", Point)#, LeapXYZg)
      rospy.Subscriber("/Leap_Hand_OPENorCLOSE", Float32)
      rospy.Subscriber("/WhichHandisit", Float32)
      rospy.Subscriber("/LeapHandAngles", Point)
      rospy.Subscriber("/Stable_Pos", Point, LeapXYZg)
      rospy.Subscriber("/Hand_velocity", Point)
     
      
      #print("x: %f " % x_coordi)
      #print("otro: %f" % otro)
      #print("z: %f " % z_coordi)
      
      #if y_coordi > 0.35:
      #   otro = 0.09

      #elif y_coordi < 0.34 and otro > 0.22:
      #   otro = 0.01
      
      #elif y_coordi < 0.21:
      #   otro = -0.09
      #else:
      #   otro = 0.0
         
      lol = other 
      lool = otro #((-1.00*otro))
      x_ = x_coordi
      y_ = y_coordi
      z_ = z_coordi
      combo = otroo + 0.3
      
     
      if otro == 0:      
         otro = otro + 0.3
          
           
      bot.arm.set_ee_pose_components(x=combo,y=other,z=otro)
      print("x: %f", combo)
      print("y: %f", other)
      print("z: %f", otro)
      #bot.arm.set_ee_cartesian_trajectory(x=combo)
      #bot.arm.set_ee_cartesian_trajectory(z=lool)
      #bot.arm.set_ee_cartesian_trajectory(z = -lool)
      #bot.arm.set_single_joint_position("shoulder", lool)
      #bot.arm.set_single_joint_position("elbow", z_)
      #bot.arm.set_single_joint_position("waist", lol)
      #bot.arm.set_ee_cartesian_trajectory(x=-combo)
      #bot.arm.set_ee_cartesian_trajectory(z= lool)
      #bot.arm.publish_positions(format(x_,'.3f'),format(y_,'.3f'),format(z_,'.3f'))
      #msg.name = 'arm'
      #msg.cmd = [waist,shoulder,elbow,0,0]
      
      #rospy.loginfo(msg)
      #pub.publish(msg)
      rospy.sleep(1)
      #r.sleep()
      #point = Point()
    
     
   
if __name__ == '__main__':
     try:
       listenerr()
     except rospy.ROSInterruptException:
       pass

