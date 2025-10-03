import os
import time
import tkinter as tk
from tkinter import messagebox
from robodk.robolink import *
from robodk.robomath import *

# Define relative path to the .rdk file
relative_path = "src/roboDK/Custom_Assistive_UR5e.rdk"
absolute_path = os.path.abspath(relative_path)

# Start RoboDK with the project fileS
RDK = Robolink()
print("Loading RoboDK...")
time.sleep(5)
RDK.AddFile(absolute_path)
print("Loading RoboDK Project...")
time.sleep(3)

# Retrieve items from the RoboDK station
robot = RDK.Item("UR5e")
base = RDK.Item("UR5e Base")
tool = RDK.Item('Hand')
Init_target = RDK.Item('Init')
Bajada_target = RDK.Item('Bajada')
Subida_target = RDK.Item('Subida')
Bajada2_target = RDK.Item('Bajada2')
Dab5_target = RDK.Item('Dab5')
Stop_target = RDK.Item('Stop')
Go1_target = RDK.Item('Go1')
Go2_target = RDK.Item('Go2')
Go3_target = RDK.Item('Go3')
RCP_up_target = RDK.Item('RCP_up')
RCP_down_target = RDK.Item('RCP_down')
Out_target = RDK.Item('Out')
In_target = RDK.Item('In')


# Set robot frame, tool and speed
robot.setPoseFrame(base)
robot.setPoseTool(tool)
robot.setSpeed(50)

# Connect to real robot or simulate
def robot_online(online):
    print("Connecting to UR5e...")
    if online:
        robot.setConnectionParams('192.168.1.5', 30000, '/', 'anonymous', '')
        time.sleep(5)
        success = robot.ConnectSafe('192.168.1.5')
        time.sleep(5)
        status, status_msg = robot.ConnectedState()
        if status != ROBOTCOM_READY:
            raise Exception("Failed to connect: " + status_msg)
        RDK.setRunMode(RUNMODE_RUN_ROBOT)
        print("Connection to UR5e Successful!")
    else:
        RDK.setRunMode(RUNMODE_SIMULATE)
        print("Simulation mode activated.")

# Robot movements
def Init():
    print("Init")
    robot.setSpeed(20)
    robot.MoveL(Init_target, True)
    print("Init_target REACHED")
    

def Hand_wave():
    print("Hand Wave")
    robot.setSpeed(30)
    robot.MoveL(Bajada_target, True)
    robot.MoveL(Subida_target, True)
    robot.MoveL(Bajada2_target, True)
    print("Hand Wave FINISHED")
    
def Dab():
    robot.setSpeed(30)
    robot.MoveL(Dab5_target, True)
    print("Dab! FINISHED")

def Stop_and_go():
    print("Stop and go")
    robot.MoveL(Stop_target, True)
    time.sleep(2)
    robot.MoveL(Go1_target, True)
    robot.setSpeed(50)
    robot.MoveL(Go2_target, True)
    robot.MoveL(Go3_target, True)
    robot.MoveL(Go2_target, True)
    robot.MoveL(Go3_target, True)
    print("Stop and go FINISHED")

def RCP():
    print("Starting RCP...")
    robot.setSpeed(20)
    robot.MoveL(RCP_up_target, True)
    robot.setSpeed(100)
    cycles = 6
    for i in range(cycles):
        print(f"Compression {i+1}")
        robot.MoveL(RCP_down_target, True)
        robot.MoveL(RCP_up_target, True)
    print("RCP FINISHED")

# Confirmation dialog to close RoboDK
def confirm_close():
    root = tk.Tk()
    root.withdraw()
    response = messagebox.askquestion(
        "Close RoboDK",
        "Do you want to save changes before closing RoboDK?",
        icon='question'
    )
    if response == 'yes':
        RDK.Save()
        RDK.CloseRoboDK()
        print("RoboDK saved and closed.")
    else:
        RDK.CloseRoboDK()
        print("RoboDK closed without saving.")

# Main function
def main():
    robot_online(False)  # True for real robot, False for simulation
    Init()
    time.sleep(1)
    Hand_wave()
    time.sleep(1)
    Stop_and_go()
    time.sleep(1)
    RCP()
    time.sleep(1)
    Dab()
    time.sleep(1)
    Init()

# Run main and handle closing
if __name__ == "__main__":
    main()
    #confirm_close()

