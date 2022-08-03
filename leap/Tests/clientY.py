import socket
import sys,thread ,time
sys.path.insert(0,"/home/irobot/Desktop/LeapMotion")
import Leap
import pickle


x = 0.0
y = 0.0
z = 0.0
handnummer = 0
serverAddressPort = ("127.0.0.1",57411)
bufferSize = 1024
msgFromClient = "Leap Sensor Ready"
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

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
            handType = "Left Hand" if hand.is_left else "Right Hand"
            print handType + "Hand ID:" + str(hand.id) + "Palm Position:" + str(hand.palm_position)
            x = hand.palm_position[0]
            y = hand.palm_position[1]
            z = hand.palm_position[2]
            #global msgFromClient
            #msgFromClient = hand.palm_position[1]
            #joel = hand.palm_positiom * 0.001
            #bytestosend = str(hand.palm_position)
            bytestosend = str(hand.palm_position[0])
            bytestosend2 = str(hand.palm_position[1])
            bytestosend3 = str(hand.palm_position[2])
            myarray = str([bytestosend,bytestosend2,bytestosend3])
            #UDPClientSocket.sendto(pickle.dumps(bytestosend),serverAddressPort)
            #pickled_string = pickle.dumps(bytestosend)
            UDPClientSocket.sendto(bytestosend2,serverAddressPort)
            #UDPClientSocket.sendto(bytestosend2,serverAddressPort)
            #UDPClientSocket.sendto(bytestosend3,serverAddressPort)   
    
def main():

   listener = LeapMotionListener()
   controller = Leap.Controller()
   
   controller.add_listener(listener)
   
   #frome = controller.frame()
  
   #bytesToSend = str.encode(msgFromClient)
   
   #UDPClientSocket.sendto(bytesToSend,serverAddressPort)

   msgFromServer = UDPClientSocket.recvfrom(bufferSize)

   msg = "Server says {}".format(msgFromServer[0])
   print(msg)
   
   print "Press enter to quit..."
   try:
     sys.stdin.readline()
   except KeyboardInterrupt:
     pass 
   finally:
     controller.remove_listener(listener)
     
if __name__ == "__main__":
  main()

