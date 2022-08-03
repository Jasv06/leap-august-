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

x = 0.3
y = 0.0
z = 0.3

id_ = 0.0
hands_number = 0.0
hand_status = 1.0

bot = InterbotixManipulatorXS("rx150","arm","gripper", gripper_pressure = 0.5)

bot.arm.go_to_home_pose()
bot.gripper.open()
time.sleep(1)
bot.arm.set_single_joint_position("waist", -np.pi/2.0)    
bot.arm.set_ee_cartesian_trajectory(x=0.05,z=-0.17)
bot.gripper.close()
time.sleep(1)
bot.arm.set_ee_cartesian_trajectory(x=-0.05,z=0.17)
time.sleep(1)
bot.arm.set_single_joint_position("waist", 0)
time.sleep(1)

def xyz(data):

   global x
   global y
   global z
   
   x = data.x
   y = data.y
   z = data.z

def hand(data):

   global id_
   global hands_number
   global hand_status
   
   id_ = data.handID
   hands_number = data.handnummer
   hand_status = data.handstates
   
def main():
   
   rospy.init_node('rx150_robot_manipulation')
   
   print("Ready to control the robot!!")
      
   r = rospy.Rate(100)
   
   while not rospy.is_shutdown():
      
      rospy.Subscriber("/Robot_coordinates", Point, xyz)
      rospy.Subscriber("/hand_status", handstatus, hand)
      print(x)
      print(y)
      print(z)
         
      x_robot_control = x
      y_robot_control = y
      z_robot_control = z
      
      identification_id = id_
      number_of_hands = hands_number
      status_of_hands = hand_status
      
      #print("id :", identification_id)
      #print("number of hands: ", number_of_hands)
      #print("status of hands :", status_of_hands)
      
      #print(number_of_hands)
      #print(hand_status)
      
      if number_of_hands == 0 and hand_status == 1:
         time.sleep(0.5)
         print("sleeping")
         continue 
        
      elif number_of_hands == 1 and hand_status < 0.7:
        print("moving")
        bot.arm.set_ee_pose_components(x=x_robot_control,y=y_robot_control,z=z_robot_control)
        if hand_status < 0.5:
             bot.gripper.open()
             bot.arm.go_to_home_pose()
             bot.arm.go_to_sleep_pose()
             break
        else: 
             pass
      else: 
          pass
      time.sleep(1)             
   

if __name__ == '__main__': 
    main()  
