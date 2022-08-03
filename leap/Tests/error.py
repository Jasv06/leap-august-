from interbotix_sdk.robot_manipulation import InterbotixRobot
from interbotix_descriptions import interbotix_mr_descriptions as mrd


def main():
    #joint_positions = [-1.0, 0.5 , 0.5, 0, -0.5, 1.57]
    arm = InterbotixRobot(robot_name="rx150", mrd=mrd)
    arm.go_to_home_pose()
    #arm.set_joint_positions(joint_positions)
    #arm.go_to_home_pose()
    arm.open_gripper()
    arm.go_to_sleep_pose()

if __name__=='__main__':
    main()
