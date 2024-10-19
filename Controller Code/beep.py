import time
import socket
import os
import winsound
from threading import Thread


def setIP():
    opt = 0
    count = 0

    while opt > 4 or opt < 1:
        try:  # Tries this code
            # You don't need to enter all IP's below just the ones for the connection method you are using
            opt = int(input('Set Client IP:\n1: Pi Hotspot Laptop (Controller IP On Hotspot)\n2: Laptop Wired LAN (Controller IP On Wired LAN)\n3: Laptop Wireless LAN (Controller IP On Wireless LAN)\n4: Other\n\nChoice: '))
        except ValueError:  # If a value error occurs, sets opt so the while loops again
            opt = 0

        print()

    if opt == 1:
        ip = 'Controller IP On Hotspot'  # Enter the IP of the controller on the hotspot
    elif opt == 2:
        # Enter the IP of the controller on the wired LAN
        ip = 'Controller IP On Wired LAN'
    elif opt == 3:
        # Enter the IP of the controller on the wireless LAN
        ip = 'Controller IP On Wireless LAN'
    else:
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

    return ip


host = setIP()  # Sets IP of host
port = 65433
frequency = 1500  # Set Frequency To 1000 Hertz


def rec():
    loop = True

    while loop:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.2)  # Sets the timeout for a connection to 0.02
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            s.listen()

            conn, addr = s.accept()

            while True:
                data = conn.recv(1024)
                if not data:
                    break
                return data.decode()  # Returns the data sent over in a string format

            loop = False

            s.close()

        except TimeoutError:
            s.close()


def beep():
    while True:
        distance = float(rec())

        if distance <= 0.40 and distance > 0.22:
            beeps = 1
            duration = round((1/beeps) * 1000) - 1
            winsound.Beep(frequency, duration)
        elif distance <= 0.22 and distance > 0.19:
            beeps = 2
            duration = round((1/beeps) * 1000) - 1
            winsound.Beep(frequency, duration)
        elif distance <= 0.19 and distance > 0.17:
            beeps = 3
            duration = round((1/beeps) * 1000) - 1
            winsound.Beep(frequency, duration)
        elif distance <= 0.17 and distance > 0.15:
            beeps = 4
            duration = round((1/beeps) * 1000) - 1
            winsound.Beep(frequency, duration)
        elif distance <= 0.15 and distance >= 0.05:
            beeps = 5
            duration = round((1/beeps) * 1000) - 1
            winsound.Beep(frequency, duration)
        elif distance <= 0.05:
            beeps = 0.5
            duration = round((1/beeps) * 1000) - 1
            winsound.Beep(frequency, duration)


thread = Thread(target=beep)
thread.start()
