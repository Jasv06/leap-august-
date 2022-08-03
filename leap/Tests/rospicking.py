import rospy
import time 
from time import sleep 
from interbotix_sdk.robot_manipulation import InterbotixRobot
from interbotix_descriptions import interbotix_mr_descriptions as mrd
import numpy as np



def talker():
    run_once = 0
    
    arm = InterbotixRobot(robot_name="rx150", mrd=mrd)
    
    topics = rospy.get_published_topics()
    
    #defines which robot arm we are using 
    #Note: if a different robot name is used other than the one connected the robot wont perfom any action 
    numero = len(topics)
    
    while not rospy.is_shutdown():
 
     # if numero < 10:
      arm.go_to_home_pose(moving_time = 2)
         
       #while rospy.getname     
      #if topics[] > 1 and topics[] < 11:
       #arm.go_to_home_pose()
      sleep(4) 
     # else:
    #makes arm leave sleep position 
      arm.set_ee_pose_components(x=0.3, z=0.2, moving_time=2)
    
    #turn the arm 90 degrees counterclockwise
      arm.set_single_joint_position("waist", np.pi/2.0,moving_time=2)
    #opens the gripper
    #arm.open_gripper()
    
      arm.close_gripper()
      
      arm.set_ee_cartesian_trajectory(x=0.4, z=0.03, moving_time = 1)
      
      arm.open_gripper()
       
      arm.set_ee_cartesian_trajectory(x=-0.4, z=-0.03, moving_time =1)
      
      #arm.set_single_joint_position("waist", -np.pi/2.0,moving_time=3)
    #arm.set_ee_pose_components(x=0.1,z=-0.5)
      #arm.open_gripper()
    #arm.set_ee_cartesian_trajectory(x=-0.1,z=0.5)
      #arm.set_ee_cartesian_trajectory(pitch=1.5)
      #arm.set_ee_cartesian_trajectory(pitch=-1.5)
      #arm.set_single_joint_position("waist", np.pi/2.0)
      #arm.set_ee_cartesian_trajectory(x=0.1, z=-0.10)
      #arm.close_gripper()
      #arm.set_ee_cartesian_trajectory(x=-0.1, z=0.10)
      #arm.open_gripper()
      arm.go_to_home_pose()
      arm.go_to_sleep_pose()
    
      rate.sleep()
        
      if topics is None:
         return

if __name__=='__main__':
    try:
       talker()
    except rospy.ROSInterruptExecption:
       pass
