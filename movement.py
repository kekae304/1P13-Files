ip_address = 'localhost' # Enter your IP Address here
project_identifier = 'P2B' # Enter the project identifier i.e. P2A or P2B
#--------------------------------------------------------------------------------
import random
import sys
sys.path.append('../')
from Common.simulation_project_library import *

hardware = False
QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
arm = qarm(project_identifier,ip_address,QLabs,hardware)
potentiometer = potentiometer_interface()

#preassigned variables needed for the main code
#includes the various autoclaves in lists to be used later
cage_choices = [1, 2, 3, 4, 5, 6]
cage_colours = ["red", "green", "blue", "red", "green", "blue"]
arm.home()
home = arm.effector_position()

#Goes to spawn position and decides how much to close the gripper
def spawn(cage):
    arm.spawn_cage(cage)
    print("Spawning cage...")
    return cage

def remove(cage, choice, colour):
    if cage <= 3:
        size = "small"
    else:
        size = "large"
    print("Removing", size, colour, "cage from list")
    cage_choices.pop(choice)
    cage_colours.pop(choice)
    return

def pick_up(cage):
    arm.move_arm(0.6, 0.05, 0)#pickup location cords 
    time.sleep(2)
    #this function choses how much to open the gripper depending on what autoclave is selected, if it is a small one this function is true
    if cage <= 3:
        print("Picking up small cage...")
        arm.control_gripper(35)
    else:
        print("Picking up large cage...")
        arm.control_gripper(25)
    time.sleep(2)
    #Moves to home position without opening the claw
    arm.move_arm(home[0], home[1], home[2])

def rotate(colour):
    print("Use right potentiometer to rotate to", colour, "autoclave")
    move = 0
    #while loop, countines checking for updated values of the left potentiometer while running
    while True:
        if arm.check_autoclave(colour) == True: #When the arm is in front of the right autoclave, code moves on to the next function
            print("Checking...")
            time.sleep(2)
            print("Correct autoclave")
            break
        rotate = 0
        base_position = move
        move = potentiometer.right() - 0.5
        if (potentiometer.right() - 0.5) < 0: #rotate arm based off potentiometer input
            rotate = (abs(move) - abs(base_position))*348 #the calculatoin done to rotate a number of degrees based off potentiometer input to the right
        if (potentiometer.right() - 0.5) > 0:
            rotate = (abs(base_position) - abs(move)) * 348
        arm.rotate_base(rotate)

def place(colour, cage):
    arm.activate_autoclaves()
    time.sleep(2)
    if cage <= 3:
        print("set left potentiometer to 60%")
    else:
        print("set left potentiometer to 100%")
    while True:
        if cage <= 3:
            if potentiometer.left() == 0.6: #The controls for the arm if the arm is going to the small drop-off point
                if colour == "blue":
                    print("dropping off small blue cage")
                    arm.move_arm(0, -0.63, 0.34)
                elif colour == "red":
                    print("dropping off small red cage")
                    arm.move_arm(-0.01, 0.63, 0.34)
                elif colour == "green":
                    print("dropping off small green cage")
                    arm.move_arm(-0.63, 0.22, 0.34)
                time.sleep(2)
                arm.control_gripper(-10)
                break
        else:
            if potentiometer.left() == 1: #The controls for the arm if the arm is going to the big drop-off point
                arm.open_autoclave(colour, True)
                if colour == "blue":
                    print("dropping off large blue cage")
                    arm.move_arm(0, -0.42, 0.22)
                elif colour == "red":
                    print("dropping off large red cage")
                    arm.move_arm(0.04, 0.42, 0.22)
                elif colour == "green":
                    print("dropping off large green cage")
                    arm.move_arm(-0.42, 0.22, 0.22)
                time.sleep(2)
                arm.control_gripper(-10)
                time.sleep(2)
                arm.open_autoclave(colour, False)
                break
        
def main():
    cages_left = 5
    DELAY = 2
    while cages_left >= 0:
        if potentiometer.left() == 0.5 and potentiometer.right() == 0.5:
            choice = random.randint(0, cages_left)
            cage = cage_choices[choice]
            colour = cage_colours[choice]
            cages_left -= 1
            spawn(cage)
            remove(cage, choice, colour)
            pick_up(cage)
            time.sleep(DELAY)
            rotate(colour)
            time.sleep(DELAY)
            place(colour, cage)
            time.sleep(DELAY)
            arm.home()
            print("set the left and right potentiometers to 50%")
            print("--------------------------------------------")
    print("FINISHED")

'''MAIN EXECUTION'''

if __name__ == '__main__':
    main()
