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
hand_status = 2.0

hand_life = 0.0


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
   
   
def Leap_life_of_hand(data): 
   
   global hand_life
   
   hand_life = data.data
   
   
def main():
   
   bot = InterbotixManipulatorXS("rx150","arm","gripper", gripper_pressure = 0.5)
   
   rospy.init_node('rx150_robot_manipulation')
   
   print("Ready to control the robot!!")
      
   r = rospy.Rate(100)
   
   id_falso = 0
   
   while not rospy.is_shutdown():
      
      rospy.Subscriber("/hand_life_in_sensor", Float32, Leap_life_of_hand)
      rospy.Subscriber("/Robot_coordinates", Point, xyz)
      rospy.Subscriber("/hand_status", handstatus, hand)
                     
      x_robot_control = x
      y_robot_control = y
      z_robot_control = z
      
      identification_id = id_
      number_of_hands = hands_number
      status_of_hands = hand_status
      

      if number_of_hands > 0 and identification_id != id_falso and hand_life >= 4: 
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
         id_falso = identification_id
         continue
         
      """dont forget to update the line below"""
      
      robot_position = bot.arm.get_joint_commands() 
      
      if hand_status > 0.5 and hand_status <= 1 and hand_life >= 4 or number_of_hands == 0 and robot_position == [0.0, -0.00033543302359544114, 0.00047924695847695667, -0.00014381393488124145, -5.3723151317487e-18]:
         
         if robot_position[0] == 0 and robot_position[1] <= -1.7 and robot_position[2] >= 1.5 and robot_position[3] >= 0.8 and robot_position[4] == 0:
            exit()
         
         bot.arm.set_single_joint_position("waist", -np.pi/2.0)    
         bot.arm.set_ee_cartesian_trajectory(x=0.05,z=-0.17)
         bot.gripper.open()
         time.sleep(1)
         bot.arm.set_ee_cartesian_trajectory(x=-0.05,z=0.17)
         time.sleep(1)
         bot.arm.set_single_joint_position("waist", 0)  
         bot.arm.go_to_sleep_pose()        
                           
      if hand_status < 0.5 and hand_life >= 4:
      
         #if robot_position[0] == 0 and robot_position[1] <= -1.7 and robot_position[2] >= 1.5 and robot_position[3] >= 0.8 and robot_position[4] == 0:
            #exit()
            
         bot.arm.set_ee_pose_components(x=x_robot_control,y=y_robot_control,z=z_robot_control)       
         bot.gripper.open()
         bot.arm.go_to_home_pose()
         bot.arm.go_to_sleep_pose()
      
      time.sleep(1)             
   

if __name__ == '__main__': 
    main()  
