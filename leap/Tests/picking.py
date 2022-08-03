from interbotix_xs_modules.arm import InterbotixManipulatorXS
from interbotix_xs_modules.gripper import InterbotixGripperXS
import numpy as np
import time
# This script makes the end-effector perform pick, pour, and place tasks
#
# To get started, open a terminal and type 'roslaunch interbotix_xsarm_control xsarm_control.launch robot_model:=wx250'
# Then change to this directory and type 'python bartender.py'

def main():
    bot = InterbotixManipulatorXS("rx150", "arm", "gripper", moving_time = 2)
    pinzas = InterbotixGripperXS("rx150","gripper")
    #,gripper_pressure = 0.3, gripper_pressure_lower_limit=150,gripper_pressure_upper_limit=350)
    bot.arm.set_ee_pose_components(x=0.3, z=0.2)
    bot.arm.go_to_home_pose()
    #pinzas.gripper.set_pressure(0.1)
    #bot.arm.set_single_joint_position("waist", np.pi/2.0)
    #pinzas.gripper.open()
    #time.sleep(5)
    #bot.arm.set_ee_cartesian_trajectory(x=0.1, z=-0.16)
    #pinzas.gripper.close()
    bot.arm.set_single_joint_position(joint_name = "left_finger", position = -0.015)
    #bot.dxl.robot_write_joint_command("gripper",command=25)
    #bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.16)
    #bot.arm.set_single_joint_position("waist", -np.pi/2.0)
    #bot.arm.set_ee_cartesian_trajectory(pitch=0.5)
    #bot.arm.set_ee_cartesian_trajectory(pitch=-0.5)
    #bot.arm.set_single_joint_position("waist", np.pi/2.0)
    #bot.arm.set_ee_cartesian_trajectory(x=0.1, z=-0.16)
    #time.sleep(5)
    #pinzas.gripper.open()
    #bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.16)
    bot.arm.go_to_home_pose()
    bot.arm.go_to_sleep_pose()

if __name__=='__main__':
    main()

