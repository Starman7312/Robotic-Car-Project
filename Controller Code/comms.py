import socket
import time
import csv
import os
import copy
from threading import Thread

global s

# Allows for quick setting of IP address


def setIP():
    opt = 0
    asc = 0
    count = 0

    while asc < 49 or asc > 52:  # Validates input to numbers between 1-4
        opt = input('Set Host IP:\n1: Pi Hotspot (Raspberry Pi Hotspot IP)\n2: Pi Wireless LAN (Raspberry Pi Wireless LAN IP)\n3: Pi Wired LAN (Raspberry Pi Wired LAN IP)\n4: Other\n\nChoice: ')

        # Validates that input is 1 character
        if len(opt) == 1:
            asc = ord(opt)
        else:
            asc = 0
        print()

    opt = int(opt)  # Converts validates input to integer
    if opt == 1:
        ip = 'Raspberry Pi Hotspot IP'  # IP of raspberry pi on hotspot
    elif opt == 2:
        ip = 'Raspberry Pi Wireless LAN IP'  # IP of raspberry pi on home LAN
    elif opt == 3:
        ip = 'Raspberry Pi Wired LAN IP'  # IP of raspberry pi on wired LAN
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

    return ip  # Returns IP set


host = setIP()  # Sets IP of host
port = 65432  # This sets the port to be used
s = '1.00'
moves = []
store = False


def LAN(host, port, message):
    # This initiates the socket object
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.settimeout(0.3)
    try:
        # This initiates the TCP/IP connection to the server (rec function on rasperry pi)
        connection.connect((host, port))
        connection.sendall(message.encode())  # This sends the message
        connection.close()  # This closes the connection
    except TimeoutError:
        connection.close()
        print('Connection Timeout')

# Sets the speed at which to run the motors


def setSpeed(num):
    global s
    s = str(num/100)

    if len(s) != 4:  # Checks the data is to 2 d.p
        s += '0'

# This defines each function which is imported and run upon a button press on the GUI
# Each makes use of the LAN function to actuate the motors correctly


def NW():
    global store
    global moves

    if store:
        moves.append('NW' + s)
    else:
        LAN(host, port, ('NW' + s))


def forwards():
    global store
    global moves

    if store:
        moves.append('F' + s)
    else:
        LAN(host, port, ('F' + s))


def NE():
    global store
    global moves

    if store:
        moves.append('NE' + s)
    else:
        LAN(host, port, ('NE' + s))


def left():
    global store
    global moves

    if store:
        moves.append('L' + s)
    else:
        LAN(host, port, ('L' + s))


def stop():
    global store
    global moves

    if store:
        moves.append('S' + s)
    else:
        LAN(host, port, ('S' + s))


def right():
    global store
    global moves

    if store:
        moves.append('R' + s)
    else:
        LAN(host, port, ('R' + s))


def SW():
    global store
    global moves

    if store:
        moves.append('SW' + s)
    else:
        LAN(host, port, ('SW' + s))


def backwards():
    global store
    global moves

    if store:
        moves.append('B' + s)
    else:
        LAN(host, port, ('B' + s))


def SE():
    global store
    global moves

    # Stores movements if record mode is active
    if store:
        moves.append('SE' + s)
    # Actuates motors if record mode isn't active
    else:
        LAN(host, port, ('SE' + s))

# Activates recording of movements (directions selected by user)


def rec():
    global store
    global moves

    store = True
    moves = []

# Plays the movement sequence


def play():
    global store
    global moves
    global s

    for i in moves:  # Plays each move in the sequence
        LAN(host, port, i)
        time.sleep(1)

    store = False  # Stops recoding movement sequence

# Threads the play function, so it can be run in parallel with the GUI (avoiding freezing)


def playThread():
    thread = Thread(target=play)
    thread.start()


def autoFilePath():  # Sets standard folder for accessing data files and returns filepath of this
    directory = os.getcwd() + '\\Program Data Files'

    if 'Program Data Files' not in os.listdir():  # Checks if folder already exists
        os.mkdir(directory)  # Makes the folder if it doesn't

    return directory + '\\'  # Returns filepath of data file

# Saves a recorded movement sequence


def save():
    global moves

    path = autoFilePath()  # Gets the file path for the csv file
    num = 1

    try:  # Checks if the file exists
        filePath = open(path + 'Moves.csv', 'r')
        filePath.close()
        csv = '\n'  # Sets up new record to be on a new line in the csv file
    except:
        csv = ''  # Sets up CSV to store its first record

    filePath = open(path + 'Moves.csv', 'a')  # Opens the file in write mode

    for i in moves:  # Encodes the moves data into csv format
        if num == len(moves):
            csv += (i + '')
        else:
            csv += (i + ',')

        num += 1

    filePath.write(csv)  # Writes the moves to the csv file

    filePath.close()  # Closes the file once all the data has been added

# Removes Speed Control number from the movement sequence


def readable(lis):
    num = 0
    moves = ['F', 'B', 'L', 'R', 'NE', 'NW', 'SW', 'SE', 'S']  # Acronym list
    direction = ['Forwards', 'Backwards', 'Left', 'Right', 'Curve Right', 'Curve Left',
                 'Reverse Curve Right', 'Reverse Curve Left', 'Stop']  # Plain text list
    for i in lis:  # Runs for each record in the list
        no = 0
        for x in i:  # Runs for each element in the record
            plain = ''
            number = 0
            for l in x:  # Runs for each character in the record element
                code = ord(l)  # Gets charcter ascii value
                # Checks the ascii value corresponds to a number of decimal point
                if (code < 48 or code > 57) and (not code == 46):
                    plain += l  # Adds to the plain text variable

            lis[num].pop(no)  # Removes the edited element from the list

            for i in moves:  # Converts acronyms to plain text equivalents
                if plain == moves[number]:
                    # Inserts the plain text version into the list
                    lis[num].insert(no, direction[number])
                    break
                else:
                    number += 1

            no += 1  # Increments to the next list element

        num += 1

    return lis  # Returns plain text movement sequence data

# Loads the movement preset selected and runs it


def load():
    global moves

    pos = 0
    opt = 0
    asc = 0
    # List of nums that cause run again
    nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    path = autoFilePath()  # Gets file path

    filePath = open(path + 'Moves.csv', 'r')  # Opens the file in read mode
    # Defines the csv file reader and tells it which file to read
    reader = csv.reader(filePath)
    # Converts the csv file reader to a list for each record - with each record split into elements
    rows = list(reader)
    filePath.close()  # Closes the file as it is no longer needed

    # Creates copy of original movement sequence (so it doesn't get overridden by the readable version)
    original = copy.deepcopy(rows)
    # Converts the rows to a readable version, removing the speed control numbers
    presets = readable(rows)

    # Prints the plain text presets csv file
    for i in range(len(presets)):  # Runs the code below for the number of lists there are stored in presets (Each list is one line of the csv file) - this is done so it reads each line
        # Prints the list from rows that possition tells it to without any [] or ''
        print(f'Preset {pos + 1}: ' + (', '.join(map(str, (presets[pos])))))
        pos += 1

    # Allows the user to select a preset
    while opt < 1 or opt > len(presets):  # Validates input
        try:
            opt = int(input('Choice: '))
        # Sets input to loop if causes an error (e.g. as char is entered not integer)
        except ValueError:
            opt = 0
        print()

    # Sets the moves to be played to those selected via the preset
    moves = original[opt-1]
    play()  # Runs the preset

    # Asks the user if they want to run another preset
    run = input('Run another preset (Y/N): ')

    # Runs another preset if yes is entered or a preset number
    if run == 'Y' or run == 'y' or run == 'yes' or run == 'Yes' or run == 'YES' or run in nums:
        print()
        loadThread()  # Runs the preset function again

# Threads the load function, so it can be run in parallel with the GUI (avoiding freezing)


def loadThread():
    thread = Thread(target=load)
    thread.start()
