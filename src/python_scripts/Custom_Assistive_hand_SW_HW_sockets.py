import os
import time
import socket
import tkinter as tk
from tkinter import messagebox
from math import radians, degrees, pi
import numpy as np
from robodk.robolink import *
from robodk.robomath import *

#Load the RoboDK project
relative_path = "src/roboDK/Custom_Assistive_UR5e.rdk"
absolute_path = os.path.abspath(relative_path)
RDK = Robolink()
RDK.AddFile(absolute_path)
# Robot setup
RDK = Robolink()
robot = RDK.Item("UR5e")
base = RDK.Item("UR5e Base")
tool = RDK.Item('Hand')

Init_target = RDK.Item('Init')
Bajada_target = RDK.Item('Bajada')
Subida_target = RDK.Item('Subida')
Bajada2_target = RDK.Item('Bajada2')
Stop_target = RDK.Item('Stop')
Go1_target = RDK.Item('Go1')
Go2_target = RDK.Item('Go2')
Go3_target = RDK.Item('Go3')
RCP_up_target = RDK.Item('RCP_up')
RCP_down_target = RDK.Item('RCP_down')
Dab5_target = RDK.Item('Dab5')

robot.setPoseFrame(base)
robot.setPoseTool(tool)
robot.setSpeed(20)

# Robot Constants setup
ROBOT_IP = '192.168.1.5'
ROBOT_PORT = 30002 # Default port for UR robots
accel_mss = 1.2
speed_ms = 0.75
blend_r = 0.0
timej = 6 # seconds to finish movej
timel = 4 # seconds to finish movel

# Define robot movement commands as URScript strings
set_tcp="set_tcp(p[0.000000, 0.000000, 0.050000, 0.000000, 0.000000, 0.000000])"

j1, j2, j3, j4, j5, j6 = np.radians(Init_target.Joints()).tolist()[0]
movej_init = f"movej([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],1.20000,0.75000,{timel},0.0000)"

j1, j2, j3, j4, j5, j6 = np.radians(Bajada_target.Joints()).tolist()[0]
movel_bajada = f"movel([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],{accel_mss},{speed_ms},{timel},0.000)"

j1, j2, j3, j4, j5, j6 = np.radians(Subida_target.Joints()).tolist()[0]
movel_subida = f"movel([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],{accel_mss},{speed_ms},{timel},0.000)"

j1, j2, j3, j4, j5, j6 = np.radians(Bajada2_target.Joints()).tolist()[0]
movel_bajada2 = f"movel([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],{accel_mss},{speed_ms},{timel},0.000)"

j1, j2, j3, j4, j5, j6 = np.radians(Dab5_target.Joints()).tolist()[0]
movel_Dab5 = f"movel([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],{accel_mss},{speed_ms},{timel},{blend_r})"

j1, j2, j3, j4, j5, j6 = np.radians(Stop_target.Joints()).tolist()[0]
movel_Stop = f"movel([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],{accel_mss},{speed_ms},{timel},{blend_r})"

j1, j2, j3, j4, j5, j6 = np.radians(Go1_target.Joints()).tolist()[0]
movel_Go1 = f"movel([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],{accel_mss},{speed_ms},{timel},{blend_r})"

j1, j2, j3, j4, j5, j6 = np.radians(Go2_target.Joints()).tolist()[0]
movel_Go2 = f"movel([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],{accel_mss},{speed_ms},{timel},{blend_r})"

j1, j2, j3, j4, j5, j6 = np.radians(Go3_target.Joints()).tolist()[0]
movel_Go3 = f"movel([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],{accel_mss},{speed_ms},{timel},{blend_r})"

j1, j2, j3, j4, j5, j6 = np.radians(RCP_up_target.Joints()).tolist()[0]
movel_RCP_up = f"movel([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],{accel_mss},{speed_ms},{timel},{blend_r})"

j1, j2, j3, j4, j5, j6 = np.radians(RCP_down_target.Joints()).tolist()[0]
movel_RCP_down = f"movel([{j1},{j2}, {j3}, {j4}, {j5}, {j6}],{accel_mss},{speed_ms},{timel},{blend_r})"

# Check robot connection
def check_robot_port(ROBOT_IP, ROBOT_PORT):
    global robot_socket
    try:
        robot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        robot_socket.settimeout(1)  # Tiempo de espera de 1 segundo
        robot_socket.connect((ROBOT_IP, ROBOT_PORT)) 
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False
# Send URScript command
def send_ur_script(command):
    robot_socket.send((command + "\n").encode())

# Wait for robot response
def receive_response(t):
    try:
        print("Waiting time: " + str(t))
        time.sleep(t)       
    except socket.error as e:
        print(f"Error receiving data from the robot: {e}")
        exit(1) #Non-zero exit status code to indicate the error

# Movements
def Init():
    print("Init")
    robot.setSpeed(20)
    robot.MoveL(Init_target, True)
    print("Init_target REACHED")
    if robot_is_connected:
        # Set the TCP pose
        print("Init REAL UR5e")
        send_ur_script(set_tcp)
        receive_response(1)
        send_ur_script(movej_init)
        receive_response(timej)
    else:
        print("UR5e is not connected. Only simulation will take place")

def Hand_wave():
    print("Hand Wave")
    robot.setSpeed(30)
    robot.MoveL(Bajada_target, True)
    robot.MoveL(Subida_target, True)
    robot.MoveL(Bajada2_target, True)
    print("Hand Wave FINISHED")
    if robot_is_connected:
        # Set the TCP pose
        print("Hand_wave REAL UR5e")
        send_ur_script(set_tcp)
        receive_response(1)
        send_ur_script(movel_bajada)
        receive_response(timel)
        send_ur_script(movel_subida)
        receive_response(timel)
        send_ur_script(movel_bajada2)
        receive_response(timel)
    else:
        print("UR5e is not connected. Only simulation will take place")

def Dab():
    print("Dab!")
    robot.setSpeed(30)
    robot.MoveJ(Dab5_target, True)
    print("Dab! FINISHED")
    if robot_is_connected:
        print("Dab REAL UR5e")
        send_ur_script(set_tcp)
        receive_response(1)
        send_ur_script(movel_Dab1)
        receive_response(timel)
        send_ur_script(movel_Dab2)
        receive_response(timel)
        send_ur_script(movel_Dab3)
        receive_response(timel)
        send_ur_script(movel_Dab4)
        receive_response(timel)
        send_ur_script(movel_Dab5)
        receive_response(timel)

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
    if robot_is_connected:
        print("Stop_and_go REAL UR5e")
        send_ur_script(set_tcp)
        receive_response(1)
        send_ur_script(movel_Stop)
        receive_response(timel)
        send_ur_script(movel_Go1)
        receive_response(timel)
        send_ur_script(movel_Go2)
        receive_response(timel)
        send_ur_script(movel_Go3)
        receive_response(timel)
        send_ur_script(movel_Go2)
        receive_response(timel)
        send_ur_script(movel_Go3)
        receive_response(timel)

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
    if robot_is_connected:
        print("RCP REAL UR5e")
        send_ur_script(set_tcp)
        receive_response(1)
        send_ur_script(movel_RCP_up)
        receive_response(timel)
        for i in range(cycles):
            send_ur_script(movel_RCP_down)
            receive_response(timel)
            send_ur_script(movel_RCP_up)
            receive_response(timel)

# Main function
def main():
    global robot_is_connected
    robot_is_connected=check_robot_port(ROBOT_IP, ROBOT_PORT)
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
    if robot_is_connected:
        robot_socket.close()   

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

# Run and close
if __name__ == "__main__":
    main()
    #confirm_close()