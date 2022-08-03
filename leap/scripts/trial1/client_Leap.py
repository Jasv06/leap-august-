import socket
import sys,thread ,time
sys.path.insert(0,"/home/irobot/Desktop/LeapMotion")
import Leap
import struct

serverAddressPort = ("127.0.0.1", 57410)

bufferSize = 1024

msgFromClient = "Leap Sensor Ready"

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

bytesToSend = str.encode(msgFromClient)
   
UDPClientSocket.sendto(bytesToSend,serverAddressPort)

class LeapMotionListener(Leap.Listener):
    finger_names = ['thumb','Index','Middle','Ring','Pinky']
    bone_names = ['Metacarpal','Proximal','Intermediate','Distal']
    state_names = ['INVALID_STATE','STATE_START','STATE_UPDATE','STATE_END']
    
    def on_init(self,controller):
       print "Initialized"
    
    def on_connect(self,controller):
       print "Motion Sensor Connected!"
       
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
        
        for hand in frame.hands:
            handType = "Left Hand " if hand.is_left else "Right Hand "
            print handType + "Hand ID: " + str(hand.id) + " Palm Position: " + str(hand.palm_position)
            
            strength = hand.grab_strength
            hand_identifier = hand.id
            pitch = hand.direction.pitch
            yaw = hand.direction.yaw
            roll = hand.palm_normal.roll
            filtered_hand = hand.stabilized_palm_position
            hand_speed  = hand.palm_velocity
            
            bytes = [hand.palm_position[0],hand.palm_position[1],hand.palm_position[2], strength,hand_identifier,pitch,yaw,roll,filtered_hand[0],filtered_hand[1],filtered_hand[2],hand_speed[0],hand_speed[1],hand_speed[2],1]
            bytestosend = str(hand.palm_position[0])
            bytestosend2 = str(hand.palm_position[1])
            bytestosend3 = str(hand.palm_position[2])
            myarray = str([bytestosend,bytestosend2,bytestosend3])
            
            info = struct.pack('<15f', *bytes)
              
            UDPClientSocket.sendto(info ,serverAddressPort)
            
            
    
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

