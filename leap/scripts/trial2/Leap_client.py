import socket
import sys,thread ,time
import pickle

#The path can be changed based on the directory or folder were the leap motion files are located
sys.path.insert(0,"/home/irobot/Desktop/LeapMotion")

import Leap
import struct
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
 
AddressPort = ("127.0.0.1", 57410)

HOST = '127.0.0.1'
PORT = 57410

UDPSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)

#UDPSocket.connect((HOST,PORT))

class LeapMotionListener(Leap.Listener):
    finger_names = ['thumb','Index','Middle','Ring','Pinky']
    bone_names = ['Metacarpal','Proximal','Intermediate','Distal']
    state_names = ['INVALID_STATE','STATE_START','STATE_UPDATE','STATE_END']
    
    def on_init(self,controller):
       print "Initialized"
    
    def on_connect(self,controller):
       print "Motion Sensor Connected!"
       #Enable gestures 
       controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
       controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
       controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
       controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);
       
    def on_disconnect(self,controller):
        print "Motion sensor disconnected!"

    def on_exit(self,controller):
        print "Exited"

    def on_frame(self,controller):
        frame = controller.frame() 
     
        handnummer  = len(frame.hands)
        if handnummer > 0:
            print "Hands: %d" % (handnummer)
        if handnummer < 1:
            handnummer = 0
            #print "Hands: %d" % (handnummer)
            strength = 1
            hand_identifier = 0
            pitch = 0
            yaw = 0
            roll = 0
            filtered_hand = [0,0,0]
            hand_speed  = [0,0,0] 
            
            #bytes = [len(frame.hands), 0, 0, 0,strength,hand_identifier,pitch,yaw,roll,filtered_hand[0],filtered_hand[1],filtered_hand[2],hand_speed[0],hand_speed[1],hand_speed[2],1]
            
            bytes = [len(frame.hands),strength,hand_identifier,filtered_hand[0],filtered_hand[1],filtered_hand[2],1]
            
            """For the other one use 16f"""
            
            info = struct.pack('<7f', *bytes)
              
            UDPSocket.sendto(info ,AddressPort)
            
            
            
        for hand in frame.hands:
            handType = " Left Hand " if hand.is_left else " Right Hand "
            print handType + "Hand ID: " + str(hand.id) + " Palm Position: " + str(hand.palm_position)
            
            strength = hand.grab_strength
            hand_identifier = hand.id
            pitch = hand.direction.pitch
            yaw = hand.direction.yaw
            roll = hand.palm_normal.roll
            filtered_hand = hand.stabilized_palm_position
            hand_speed  = hand.palm_velocity
            
            #bytes = [len(frame.hands), hand.palm_position[0], hand.palm_position[1], hand.palm_position[2],strength,hand_identifier,pitch,yaw,roll,filtered_hand[0],filtered_hand[1],filtered_hand[2],hand_speed[0],hand_speed[1],hand_speed[2],1]
            
            bytes = [len(frame.hands),strength,hand_identifier,filtered_hand[0],filtered_hand[1],filtered_hand[2],1]
            
            info = struct.pack('<7f', *bytes)
              
            UDPSocket.sendto(info ,AddressPort)
            
  
         
    
def main():

   listener = LeapMotionListener()
   controller = Leap.Controller()
   
   controller.add_listener(listener)
   
   print "Press enter to quit..."
   try:
     sys.stdin.readline()
   except KeyboardInterrupt:
     pass   
   finally:
     controller.remove_listener(listener)
     
if __name__ == "__main__":
  main()   

