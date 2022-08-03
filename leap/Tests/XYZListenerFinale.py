import rospy
import numpy as np
import ray
from interbotix_sdk.robot_manipulation import InterbotixRobot
from interbotix_descriptions import interbotix_mr_descriptions as mrd
from std_msgs.msg import Float32

x_coord = 0.0  
y_coord = 0.0
z_coord = 0.0 

def callbackX(data):
    global x_coord
   #rospy.loginfo(rospy.get_caller_id() + " X: %f", data.data)
    x_coord = data
   
def callbackY(data):
    global y_coord
   #rospy.loginfo(rospy.get_caller_id() + " Y: %f", data.data)
    y_coord = data
   
def callbackZ(data):
    global z_coord
   #rospy.loginfo(rospy.get_caller_id() + " Z: %f", data.data)
    z_coord = data
   
#@ray.remote
#def listener():
arm = InterbotixRobot(robot_name="rx150", mrd=mrd)
arm.set_ee_pose_components(x=0.3, z=0.2, moving_time=2)
arm.close_gripper()
arm.set_single_joint_position("waist", np.pi/2.0,moving_time=2)

#rospy.init_node('RX150coord2')
def main():
  
  rospy.init_node('RX150coord2')
  
  while not rospy.is_shutdown():
      
    rospy.Subscriber("LeapMotionX", Float32, callbackX)
    rospy.Subscriber("LeapMotionY", Float32, callbackY)
    rospy.Subscriber("LeapMotionZ", Float32, callbackZ)
    rospy.sleep(0.05)
  
    x = np.float32(str(x_coord))
    y = np.float32(str(y_coord))
    z = np.float32(str(z_coord))
  
  #print("Variable List:\n")
  #print("X = %f" % x.item())
  #print("Y = %f" % y.item())
  #print("Z = %f\n" % z.item()) 
  #print("x: " + str(x_coord) +", y: "+ str(y_coord) + ", z: " + str(z_coord))
  
    if x_coord > 0 and z_coord > 0:
        arm.set_ee_cartesian_trajectory(x= x_coord, z= z_coord)
        arm.open_gripper()
     
    if x_coord < 0 and z_coord > 0:
        arm.set_ee_cartesian_trajectory(x= x_coord, z= z_coord)
        arm.open_gripper()
     
    if x_coord > 0 and z_coord < 0:
        arm.set_ee_cartesian_trajectory(x= x_coord, z= z_coord)
        arm.open_gripper()
  
    if x_coord < 0 and z_coord < 0:
        arm.set_ee_cartesian_trajectory(x= x_coord, z= z_coord)
        arm.open_gripper()
     
    else:
        arm.open_gripper()
        arm.go_to_home_pose()
        arm.go_to_sleep_pose()
      
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass 
     
"""Block of comment to add to robot coordinates in case in doesnt work adequately """

"""
#@ray.remote
def main():
    #defines which robot arm we are using 
    #Note: if a different robot name is used other than the one connected the robot wont perfom any action 
    arm = InterbotixRobot(robot_name="rx150", mrd=mrd)
   
    #makes arm leave sleep position 
    arm.set_ee_pose_components(x=0.3, z=0.2, moving_time=2)
        
    #turn the arm 90 degrees counterclockwise
    arm.set_single_joint_position("waist", np.pi/2.0,moving_time=2)
    #opens the gripper
    #arm.open_gripper()
    arm.set_ee_cartesian_trajectory(x=0.1, z=0.05)
    arm.close_gripper()
    arm.set_ee_cartesian_trajectory(x=-0.1, z=-0.05)
    arm.set_single_joint_position("waist", -np.pi/2.0,moving_time=3)
    #arm.set_ee_pose_components(x=0.1,z=-0.5)
    arm.open_gripper()
    #arm.set_ee_cartesian_trajectory(x=-0.1,z=0.5)
    arm.set_ee_cartesian_trajectory(pitch=1.5)
    arm.set_ee_cartesian_trajectory(pitch=-1.5)
    arm.set_single_joint_position("waist", np.pi/2.0)
    arm.set_ee_cartesian_trajectory(x=0.1, z=-0.10)
    arm.close_gripper()
    arm.set_ee_cartesian_trajectory(x=-0.1, z=0.10)
    arm.open_gripper()
    arm.go_to_home_pose()
    arm.go_to_sleep_pose()
"""
#ray.get([listener.remote()])
   
#ray.get([listener.remote(), main.remote()])
 
 

        

