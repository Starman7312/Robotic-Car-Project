# Imports libraries and modules
from gpiozero import CamJamKitRobot
import time
import socket
import os
import sensor
import comms

# Some code reproduced under the MIT License (Inherited BSD-2-Clause License) from: https://github.com/CamJam-EduKit/EduKit3

previous = ''  # Sets the previous command


def setIP():  # Allows for quick and easy setting of the IP address of my raspberry pi
    opt = 0
    count = 0

    while opt > 4 or opt < 1:  # Validates input range
        try:
            opt = int(input('Set Host IP:\n1: Pi Hotspot (Raspberry Pi Hotspot IP)\n2: Pi Wireless LAN (Raspberry Pi Wireless LAN IP)\n3: Pi Wired LAN (Raspberry Pi Wired LAN IP)\n4: Other\n\nChoice: '))
        except ValueError:  # Handles input that not a number, by looping the input statement above
            opt = 0
    if opt == 1:
        ip = 'Raspberry Pi Hotspot IP'  # IP of my raspberry pi hotspot
        # IP of my laptop when connected to my rasperry pi hotspot
        ip2 = 'Controller Device IP'
    elif opt == 2:
        ip = 'Raspberry Pi Wireless LAN IP'  # IP of my raspberry pi when on my home wifi
    elif opt == 3:
        ip = 'Raspberry Pi Wired LAN IP'  # IP of my raspberry pi when on my home LAN
    else:
        print()
        while count != 3:  # Validates IP contains 3 decimal points and only numbers
            count = 0
            ip = input('Enter IP: ')

            for i in ip:  # Checks each character in the IP address
                skip = False

                if i == '.':
                    count += 1  # Logs how many decimal points exist

                # Sets the above to loop if non numeric or decimal point character found
                if (ord(i) < 48 or ord(i) > 57) and ord(i) != 46:
                    count = 0
                    # Outputs error info
                    print(
                        '\n*Error: IP address must only contain numbers and decimal points*\n')
                    skip = True
                    break  # Breaks for loop as issue found with input

            if count != 3 and not skip:
                # Outputs error info
                print('\n*Error: IP address must contain 3 decimal places*\n')
    print()

    if opt != 1:
        opt = 0

        while opt > 3 or opt < 1:  # Allows client IP to be set, when not on hostpot
            try:
                opt = int(input(
                    'Set Client IP:\n1: Laptop Wired LAN (Controller IP Wired LAN)\n2: Laptop Wireless LAN (Controller IP Wireless LAN)\n3: Other\n\nChoice: '))
            except:
                opt = 0
        if opt == 1:
            ip2 = 'Controller IP Wired LAN'  # Sets IP of my laptop on my home LAN
        elif opt == 2:
            ip2 = 'Controller IP Wireless LAN'  # Sets IP of my laptop on my home Wifi
        else:
            print()
            count = 0

            while count != 3:  # Validates IP contains 3 decimal points and only numbers
                count = 0
                ip2 = input('Enter IP: ')

                for i in ip2:  # Checks each character in the IP address
                    skip = False

                    if i == '.':
                        count += 1  # Logs how many decimal points exist

                    # Sets the above to loop if non numeric or decimal point character found
                    if (ord(i) < 48 or ord(i) > 57) and ord(i) != 46:
                        count = 0
                        # Outputs error info
                        print(
                            '\n*Error: IP address must only contain numbers and decimal points*\n')
                        skip = True
                        break  # Breaks for loop as issue found with input

                if count != 3 and not skip:
                    # Outputs error info
                    print('\n*Error: IP address must contain 3 decimal places*\n')

    print()

    return ip, ip2  # Returns IP's set


host, host2 = setIP()  # Sets host IP address
port = 65432  # Port number to use

# Defines the drive function


def drive(direction, s):
    loop = True  # Sets the distance sensor loop to run
    robot = CamJamKitRobot()  # Instantiates the robot object from library
    previous = direction  # Stores the previous direction

    if direction == 'F':
        robot.forward(speed=s)
        # Listens for next command while still running motors
        direction = rec(previous)
    elif direction == 'B':
        robot.backward(speed=s)
        direction = rec(previous)
    elif direction == 'L':
        robot.left(speed=s)
        direction = rec(previous)
    elif direction == 'R':
        robot.right(speed=s)
        direction = rec(previous)
    elif direction == 'NE':
        robot.forward(curve_right=0.5, speed=s)
        direction = rec(previous)
    elif direction == 'NW':
        robot.forward(curve_left=0.5, speed=s)
        direction = rec(previous)
    elif direction == 'SE':
        robot.backward(curve_right=0.5, speed=s)
        direction = rec(previous)
    elif direction == 'SW':
        robot.backward(curve_left=0.5, speed=s)
        direction = rec(previous)
    elif direction == 'ESP':
        robot.backward()
        time.sleep(0.1)
        robot.stop()
        direction = rec(previous)
    else:
        robot.stop()
        direction = rec(previous)

    return direction

# Defines the TCP/IP communciations listening software


def rec(previous):
    skip = False
    loop = True

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.02)  # Sets the timeout for a connection to 0.02
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen()

    # Very quickly switches between listening for drive commands and checking the distance sensor
    while loop:  # Loops until a drive command is recieved or the sensor triggers a stop command
        # start = time.time()
        try:  # Checks for a drive command and exits after 0.02 secs if one isn't recieved
            loop = False
            conn, addr = s.accept()
        except:  # Checks the distance sensor
            # Sets the robot to stop if an object is detected 25 cm away (which accounts for stopping distance)
            if sensor.distance() <= 0.25 and (previous == 'F' or previous == 'NE' or previous == 'NW') or sensor.value() == 1:
                direction = 'ESP1.00'  # Sets the robot to stop
                skip = True  # Skips the code below
            else:
                loop = True  # Runs the loop again if not below stopping distance

        comms.LAN(host2, 65433, str(sensor.distance()))

# end = time.time()
# print(end-start)

    # Skips the loop if robot stopped due to distance sensor (as in this scenario, the code isn't required)
    if not skip:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            return data.decode()  # Returns the data sent over in a string format
    else:
        return direction  # Returns the direction to run the motors in

    s.close()


# Initiates the distance sensor (run now to warm it up, so it's clock speed is high)
sensor.distance()

# Initites listening for the first drive command
direction = rec(previous)
s = float(direction[-4] + direction[-3] + direction[-2] +
          direction[-1])  # Decodes speed from data transmitted
direction = direction[0:-4]  # Decodes direction from data transmitted

# Loops drive sequence
while True:
    direction = drive(direction, s)
    # Decodes speed from data transmitted
    s = float(direction[-4] + direction[-3] + direction[-2] + direction[-1])
    direction = direction[0:-4]  # Decodes direction from data transmitted
