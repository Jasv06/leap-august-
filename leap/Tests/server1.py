import socket
import sys
import numpy as np
import pickle
import rospy
from std_msgs.msg import Float32

joel = []

print("Do Ctrl+c to exit the program !!")
print("####### Server is listening #######")
#data, address = s.recvfrom(4096)
    
def talkerX():
  
  localIP = "127.0.0.1"
  localPort = 57410
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  s.bind((localIP,localPort))
 
  pub = rospy.Publisher('LeapMotionX',Float32, queue_size=100)
  
  rospy.init_node('Xcoord', anonymous = True)  
  
  rate = rospy.Rate(100)
  
  while not rospy.is_shutdown():
     
     data, address = s.recvfrom(4096)
              
     joel = data.decode('utf-8')
     
     A = float(joel) * 0.001
     #mensaje = print(A) % rospy.getime()
     rospy.loginfo(A)
     pub.publish(A)
     rate.sleep()
     
def talkerY():
  localIP = "127.0.0.1"
  localPort = 57411
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  s.bind((localIP,localPort))
 
  pub = rospy.Publisher('LeapMotionY',Float32, queue_size=100)
  
  rospy.init_node('Ycoord', anonymous = True)  
  
  rate = rospy.Rate(100)
  
  while not rospy.is_shutdown():
     
     data, address = s.recvfrom(4096)
              
     joel = data.decode('utf-8')
     
     B = float(joel) * 0.001
     #mensaje = print(A) % rospy.getime()
     rospy.loginfo(B)
     pub.publish(B)
     rate.sleep()

def talkerZ():

  localIP = "127.0.0.1"
  localPort = 56196
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  s.bind((localIP,localPort))
 
  pub = rospy.Publisher('LeapMotionZ',Float32, queue_size=100)
  
  rospy.init_node('Zcoord', anonymous = True)  
  
  rate = rospy.Rate(100)
  
  while not rospy.is_shutdown():
     
     data, address = s.recvfrom(4096)
              
     joel = data.decode('utf-8')
     
     A = float(joel) * 0.001
     #mensaje = print(A) % rospy.getime()
     rospy.loginfo(A)
     pub.publish(A)
     rate.sleep()

#def main():
   #talkerX()
#   talkerY()
        
#if __name__ == '__main__':
#   try:
      #main()
#      talkerZ()
#      talkerY()
      #talkerZ()
#   except rospy.ROSInterruptException:
#      pass

if __name__ == '__main__':
    Thread()
      
      
