import rospy
import numpy as np
import roslib
import time 
import sys
from interbotix_xs_modules.arm import InterbotixManipulatorXS
from interbotix_xs_modules.gripper import InterbotixGripperXS
from std_msgs.msg import Float32
from geometry_msgs.msg import Point
from std_msgs.msg import Int32 
from leap.msg import *

x_coordi_sensor_stable = 0.0
y_coordi_sensor_stable = 0.0
z_coordi_sensor_stable = 0.0

x_coordi_sensor = 0.0
y_coordi_sensor = 0.0
z_coordi_sensor = 0.0

hand_open_or_close = 0.0

hand_id = 0.0

bot = InterbotixManipulatorXS("rx150","arm","gripper")

def LeapXYZ_stable(data): 
   
   global x_coordi_sensor_stable 
   global y_coordi_sensor_stable 
   global z_coordi_sensor_stable

   x_coordi_sensor_stable = data.x
   y_coordi_sensor_stable = data.y
   z_coordi_sensor_stable = data.z  

def LeapXYZ_normal(data):

   global x_coordi_sensor 
   global y_coordi_sensor 
   global z_coordi_sensor

   x_coordi_sensor = data.x
   y_coordi_sensor = data.y
   z_coordi_sensor = data.z

def Hands_ID(data):
   
   global hand_id
   
   hand_id = data.data
   
def hand_OPEN_or_CLOSE(data):

   global hand_open_or_close
   
   hand_open_or_close = data.data
   
def main():
   
   rospy.init_node('rx150_robot_manipulation')
   
   bot.arm.go_to_home_pose()

   bot.gripper.open()

   time.sleep(2)

   bot.arm.set_single_joint_position("waist", -np.pi/2.0)
   
   bot.arm.set_ee_cartesian_trajectory(x=0.05,z=-0.17)

   bot.gripper.close()

   time.sleep(2)

   bot.arm.set_ee_cartesian_trajectory(x=-0.05,z=0.17)

   time.sleep(1)

   bot.arm.set_single_joint_position("waist", 0)

   time.sleep(2)

   count = 0
   
   #rospy.init_node('rx150_robot_manipulation')
   
   r = rospy.Rate(100)
   """Pub can be used whene desired to publish to a topic and control the servo motors directly  via a ros topic
   pub = rospy.Publisher("/rx150/commands/joint_group", JointGroupCommand, queue_size = 1)
   """
   
   print("Ready to Send messages to the robot! Press enter to start.")
   text = input("")
   if text == "":
   
      while not rospy.is_shutdown():
       
         rospy.Subscriber("/Leap/XYZ", Point, LeapXYZ_normal)
         rospy.Subscriber("/Leap_Hand_OPENorCLOSE", Float32, hand_OPEN_or_CLOSE)
         rospy.Subscriber("/WhichHandisit", Float32, Hands_ID)
         rospy.Subscriber("/LeapHandAngles", Point)
         rospy.Subscriber("/Stable_Pos", Point, LeapXYZ_stable)
         rospy.Subscriber("/Hand_velocity", Point)
       
      
         hand_indentification = hand_id
      
         hand_status = hand_open_or_close
      
         x_rob_normal = z_coordi_sensor 
         y_rob_normal = x_coordi_sensor
         z_rob_normal = y_coordi_sensor
      
         x_rob_stable = z_coordi_sensor_stable + 0.3 
         y_rob_stable = x_coordi_sensor_stable
         z_rob_stable = y_coordi_sensor_stable 
      
         if z_rob_stable == 0:
             z_rob_stable = z_rob_stable + 0.3
      
         if z_rob_stable <= 0.2:
             z_rob_stable = z_rob_stable + 0.07
             
         if z_rob_stable > 0.2:
             z_rob_stable = z_rob_stable + 0.04
      
         bot.arm.set_ee_pose_components(x=x_rob_stable,y=y_rob_stable,z=z_rob_stable)
         
         if count >= 10:
             bot.gripper.open()
             bot.arm.go_to_home_pose()
             bot.arm.go_to_sleep_pose()
             break
 
         count += 1
      
         print("hand id: %f" % hand_indentification)
         print("counter is = %i " % count)
      
         time.sleep(1)
     
   
if __name__ == '__main__':
     try:
       main()
     except rospy.ROSInterruptException:
       pass
     
