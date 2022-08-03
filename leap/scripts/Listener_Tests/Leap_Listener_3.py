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

"""The stable positon refers to the position where the sensor detected the hand stable which usually tends to lag behind for a couple of seconds from the xyz noprmla"""

x_coordi_sensor_stable = 0.0
y_coordi_sensor_stable = 0.0
z_coordi_sensor_stable = 0.0

x_coordi_sensor = 0.0
y_coordi_sensor = 0.0
z_coordi_sensor = 0.0

hand_open_or_close = 0.0

hand_id = 0.0

#pinzas = InterbotixGripperXS("rx150","gripper",gripper_pressure = 0.5, gripper_pressure_lower_limit=150,gripper_pressure_upper_limit=350)
bot = InterbotixManipulatorXS("rx150","arm","gripper")

bot.arm.go_to_home_pose()

bot.gripper.open()

#pub = rospy.Publisher("/rx150/commands/joint_single", JointSingleCommand, queue_size = 1)

time.sleep(3)

#msg = JointSingleCommand()

bot.arm.set_single_joint_position("waist", -np.pi/2.0)
bot.arm.set_ee_cartesian_trajectory(x=0.05,z=-0.17)

bot.gripper.close()
#msg.name = 'gripper'
#msg.cmd = -0.5

#pub.publish(msg)

time.sleep(2)
#pinzas.gripper.set_pressure(pressure=0.5)
#pinzas.gripper.close()

bot.arm.set_ee_cartesian_trajectory(x=-0.05,z=0.17)

time.sleep(1)

bot.arm.set_single_joint_position("waist", 0)
#bot.arm.go_to_home_pose()
time.sleep(2)

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
             z_rob_stable = z_rob_stable + 0.05
             
         #if z_rob_stable > 0.2:
         #    z_rob_stable = z_rob_stable + 0.02
      
         """y_rob_stable is substracted 0.01 since the number is negative so we will get an addition of negative numbers"""
      
         #if y_rob_stable < 0:
         #    y_rob_stable = y_rob_stable - 0.01
      
        
         # elif z_rob_stable > 0.06:
         #    z_rob_stable = z_rob_stable + 0.02
               
         # if z_rob_normal == 0:
         #    z_rob_normal = z_rob_normal + 0.3
      
      
         #text = input()
         #if text == "":
         bot.arm.set_ee_pose_components(x=x_rob_stable,y=y_rob_stable,z=z_rob_stable)
         if count >= 10:
             bot.gripper.open()
             bot.arm.go_to_home_pose()
             bot.arm.go_to_sleep_pose()
             break
             #if z_rob_stable > (z_rob_stable - 0.02) and z_rob_stable < (z_rob_stable + 0.02) and x_rob_stable > (x_rob_stable - 0.02) and x_rob_stable < (x_rob_stable + 0.02)
             #else:
 
         """
      text = input()
      try:
        if text == "":
           bot.arm.set_ee_pose_components(x=x_rob_stable,y=y_rob_stable,z=z_rob_stable)
      except KeyboardInterrupt:
           pass
         """   
         count += 1
      
         #if x_rob_stable < (x_rob_stable + 0.02)and x_rob_stable > (x_rob_stable - 0.02)
         #   print("working perfectly") 
         #if z_rob_stable > (z_coordi_sensor + 0.02) and z_rob
         #print("x: ", x_rob_stable)
         #print("y: ", y_rob_stable)
         #print("z: ", z_rob_stable)
         print("hand id: %f" % hand_indentification)
         print("counter is = %i " % count)
      
         #time.sleep(2)
     
   
if __name__ == '__main__':
     try:
       main()
     except rospy.ROSInterruptException:
       pass
     
