import socket
import sys
import numpy as np
import rospy
import time 
import pickle
from std_msgs.msg import Float32
from geometry_msgs.msg import Point
from std_msgs.msg import Int32
import struct 

localIP = "127.0.0.1"
Port = 57410

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind((localIP, Port))
  
print("Do Ctrl+c to exit the program !!")
print("####### Server is listening and publishing #######")
   
def leap_data():
  
  rospy.init_node('Leap_data', anonymous = False)  
  
  """Number of hands"""
  pub_number_of_hands = rospy.Publisher('HandNumber', Float32, queue_size = 1)
  
  """Hand state"""
  pub_hand_state = rospy.Publisher('hand_state', Float32, queue_size = 1)
  
  """NOTE: the commented out publishers can be used they are already being transferred via the udp"""
  
  """right hand publishers"""
  #pub_palm_position_right = rospy.Publisher('/Leap/XYZ', Point, queue_size=10)
  pub_hand_id = rospy.Publisher('hand_id', Float32, queue_size = 1)
  #pub_hand_angles_right = rospy.Publisher('LeapHandAngles', Point, queue_size = 10)
  pub_palm_position_stable = rospy.Publisher('hand_position_stable', Point, queue_size = 1)
  #pub_hand_velocity_right = rospy.Publisher('Hand_velocity', Point, queue_size = 10)
  
  rate = rospy.Rate(100)
  
  while not rospy.is_shutdown():
  
     coordinates = Point() 
    
     data, address = s.recvfrom(4096)
          
     data = struct.unpack('<7f', data)      
     
     number_of_hand_in_frame = data[0]
     
     strength = data[1]
     
     hand_identifier = data[2]
          
     coordinates.x = data[3]*0.001
     coordinates.y = data[4]*0.001
     coordinates.z = data[5]*0.001
          
     pub_number_of_hands.publish(number_of_hand_in_frame)
     pub_hand_state.publish(strength)
     pub_hand_id.publish(hand_identifier)
     pub_palm_position_stable.publish(coordinates)
     
     rate.sleep()
     
if __name__ == '__main__':
     leap_data()
  

