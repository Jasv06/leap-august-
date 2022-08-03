import socket
import sys
import numpy as np
import pickle
import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import Point
from std_msgs.msg import Int32
import struct 

localIP = "127.0.0.1"
localPort = 57410

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind((localIP,localPort))
  
print("Do Ctrl+c to exit the program !!")
print("####### Server is listening and publishing #######")
   
def talker():
  
  rospy.init_node('Leap', anonymous = False)  
  
  pub = rospy.Publisher('Leap/XYZ', Point, queue_size=10)
  publi = rospy.Publisher('Leap_Hand_OPENorCLOSE', Float32, queue_size = 10) 
  public = rospy.Publisher('WhichHandisit', Float32, queue_size = 10)
  publicc = rospy.Publisher('LeapHandAngles', Point, queue_size = 10)
  publiccc = rospy.Publisher('Stable_Pos', Point, queue_size = 10)
  publicccc = rospy.Publisher('Hand_velocity', Point, queue_size = 10)
  
  rate = rospy.Rate(100)
  
  while not rospy.is_shutdown():
  
     point = Point() 
     po = Point()
     p = Point()
     j = Point()
     
     data, address = s.recvfrom(4096)
     
     data = struct.unpack('<15f', data)      
     #joel = data.decode('utf-8')
     point.x = data[0]*0.001
     point.y = data[1]*0.001
     point.z = data[2]*0.001
     strength =  data[3]
     hand_id = data[4]*1.0
     #around x axis
     po.x = data[5]
     #around y axis
     po.y = data[6]
     #around z axis
     po.z = data[7]
     
     #stabilized palm position lags by a variable amount depending on the speed
     p.x = data[8]*0.001
     p.y = data[9]*0.001
     p.z = data[10]*0.001
     
     #velocity
     j.x = data[11]*0.001
     j.y = data[12]*0.001
     j.z = data[13]*0.001
     
     #print(strength)
     #A = float(joel) * 0.001
     #mensaje = print(A) % rospy.getime()
     #rospy.loginfo(point)
     pub.publish(point)
     publi.publish(strength)
     public.publish(hand_id)
     publicc.publish(po)
     publiccc.publish(p)
     publicccc.publish(j)
     #data, address = s.recvfrom(4096)
     #data_to_send = "Message received"
     #s.sendto(data_to_send.encode('utf-8'), address)
     
     
if __name__ == '__main__':
     talker()


