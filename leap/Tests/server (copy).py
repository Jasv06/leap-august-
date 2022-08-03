import socket
import sys
import numpy as np
import pickle
import rospy
from std_msgs.msg import Float32

localIP = "127.0.0.1"
localPort = 57410

joel = []

#if len(sys.argv) == 3:
    # Get "IP address of Server" and also the "port number" from argument 1 and argument 2
#    ip = sys.argv[1]
#    port = int(sys.argv[2])
#else:
#    print("Run like : python3 server.py <arg1:server ip:this system IP 192.168.1.6> <arg2:server port:4444 >")
#    exit(1)

# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
#server_address = (ip, port)
#s.bind(server_address)
s.bind((localIP,localPort))

print("Do Ctrl+c to exit the program !!")
print("####### Server is listening #######")
#data, address = s.recvfrom(4096)

while True:
    data, address = s.recvfrom(4096)
    #l = [data.decode('utf-8') for data in array1]
    joel = data.decode('utf-8')
    A = float(joel)
    #pickled_string = joel.split()
    #pickled_string[1]
    #joel = np.char.decode()
    #a = pickle.loads(joel)
    print("\nServer received: ", A , "\n")
    #send_data = input("Confirm to send data => ")
    #s.sendto(send_data.encode('utf-8'), address)
    #print("\n 2. Server sent : ", send_data,"\n")
    
def talker():
  pub = rospy.Publisher('LeapMotionX',Float64, queue_size=100)
  rospy.init_node('Xcoord', anonymous = True)  
  rate = rospy.Rate(10)
  while not rospy.is_shutdown():
     data, address = s.recvfrom(4096)
     joel = data.decode('utf-8')
     A = float(joel)
     mensaje = print(A) % rospy.getime()
     rospy.loginfo(A)
     pub.publish(A)
     rate.sleep()
     
if __name__ == '__main__':
   try:
      talker()
   except rospy.ROSInterruptException:
      pass
