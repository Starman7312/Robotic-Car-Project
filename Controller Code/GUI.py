## Imports the tkinter library and communications software code
import tkinter as tk
import comms
import beep
import os

## This function keybinds key presses to motor actuation / function activation
def keyBind(event):
    key = event.keysym

    if key == 'Up' or key == 'w' or key == 'W' or key == '8':
        comms.forwards()
    elif key == 'e' or key == 'E' or key == '9' or key == 'Prior':
        comms.NE()
    elif key == 'q' or key == 'Q' or key == '7' or key == 'Home':
        comms.NW()
    elif key == 'Right' or key == 'd' or key == 'D' or key == '6':
        comms.right()
    elif key == 'Left' or key == 'a' or key == 'A' or key == '4':
        comms.left()
    elif key == 'Down' or key == 's' or key == 'S' or key == '2':
        comms.backwards()
    elif key == 'c' or key == 'C' or key == '3' or key == 'Next':
        comms.SE()
    elif key == 'backslash' or key == 'z' or key == 'Z' or key == '1' or key == 'End':
        comms.SW()
    elif key == 'r' or key == 'R':
        comms.rec()
    elif key == 'p' or key == 'P':
        comms.play()
    else:
        comms.stop()

def autoFilePath(): ## Sets standard folder for accessing data files and returns filepath of this
    directory = os.getcwd() + '\\Image Repository'
    
    if 'Image Repository' not in os.listdir(): ## Checks if folder already exists
        os.mkdir(directory) ## Makes the folder if it doesn't

    return directory + '\\' ## Returns filepath of data file

## This function is used to import the icons for the buttons
def icon(file):
    directory = autoFilePath()
    try:
        image = tk.PhotoImage(file = r'' + directory + file) ## Loads image from specifed file path
        image = image.subsample(2, 2) ## Resizes the image
        
    except:
        print('Image Respository file missing') ## Error message if image file missing
        image = '' ## Sets image to blank if missing

    return image ## Returns image

## Creates the function GUI
def GUI():
    window = tk.Tk()## Creates the tkinter window
    window.state('zoomed') ## Sets the window size to fill the screen
    window.title('Robotic Car Control Interface') ## Give the window a title
    window.bind('<Key>', keyBind) ## Allows for key bind features

    window.update()
    h = window.winfo_height() ## Defines the middle of the window in pixels
    hCentre = h/2 - 48
    w = window.winfo_width()
    wCentre = w/2 - 55 ## Defines the centre of the window in pixels

    wGap = 115 ## Defines the horizontal gap necessary between buttons
    hGap = 115 ## Defines the vertical gap necessary between buttons

    ## Imports button images and resizes them appropriately
    global upArrow
    upArrow = icon('Up Arrow.png')
    global NWArrow
    NWArrow = icon('NW Arrow.png')
    global NEArrow
    NEArrow = icon('NE Arrow.png')
    global leftArrow
    leftArrow = icon('Left Arrow.png')
    global stopIcon
    stopIcon = icon('Stop Icon.png')
    global rightArrow
    rightArrow = icon('Right Arrow.png')
    global SWArrow
    SWArrow = icon('SW Arrow.png')
    global downArrow
    downArrow = icon('Down Arrow.png')
    global SEArrow
    SEArrow = icon('SE Arrow.png')
    global Record
    Record = icon('Record.png')
    global Play
    Play = icon('Play.png')
    global Save
    Save = icon('Save.png')
    global Load
    Load = icon('Load.png')
    
    ## Creates the interface buttons and arranges them on the interface screen
    northWest = tk.Button(window, image = NWArrow, bg = 'black', width = 110, height = 110, command = comms.NW).place(x = (wCentre - wGap), y = (hCentre - hGap))
    f = tk.Button(window, image = upArrow, bg = 'black', width = 110, height = 110, command = comms.forwards).place(x = (wCentre), y = (hCentre - hGap))
    northEast = tk.Button(window, image = NEArrow, bg = 'black', width = 110, height = 110, command = comms.NE).place(x = (wCentre + wGap), y = (hCentre - hGap))
    
    l = tk.Button(window, image = leftArrow, bg = 'black', width = 110, height = 110, command = comms.left).place(x = (wCentre - wGap) , y = (hCentre))
    s = tk.Button(window, image = stopIcon, bg = 'black', width = 110, height = 110, command = comms.stop).place(x = (wCentre) , y = (hCentre))
    r = tk.Button(window, image = rightArrow, bg = 'black', width = 110, height = 110, command = comms.right).place(x = (wCentre + wGap) , y = (hCentre))
    
    southWest = tk.Button(window, image = SWArrow, bg = 'black', width = 110, height = 110, command = comms.SW).place(x = (wCentre - wGap) , y = (hCentre + hGap))
    b = tk.Button(window, image = downArrow, bg = 'black', width = 110, height = 110, command = comms.backwards).place(x = (wCentre) , y = (hCentre + hGap))
    southEast = tk.Button(window, image = SEArrow, bg = 'black', width = 110, height = 110, command = comms.SE).place(x = (wCentre + wGap) , y = (hCentre + hGap))

    ## This function sets the speed at which to actuate the robot's motors upon button press
    def speed(event):
        comms.setSpeed(slider.get())
    
    ## This creates the slider and positions it on the interface
    slider = tk.Scale(from_ = 100, to = 0, orient = 'vertical', command = speed, width = 80, bg = 'black', fg = 'white', troughcolor = 'grey50', label = 'Speed Control')
    slider.place(x = (wCentre + 3 * wGap), y = (hCentre + 5))
    slider.set(100) ## Sets speed to 100% when the interface starts up

    ## Creates record, play, save and load movement sequence buttons
    r = tk.Button(window, image = Record, bg = 'black', width = 110, height = 110, command = comms.rec).place(x = (wCentre - (3.15 * wGap) - 10) , y = (hCentre))
    p = tk.Button(window, image = Play, bg = 'black', width = 110, height = 110, command = comms.playThread).place(x = (wCentre - (2.15 * wGap) - 5) , y = (hCentre))
    save = tk.Button(window, image = Save, bg = 'black', width = 110, height = 110, command = comms.save).place(x = (wCentre - (4.15 * wGap) - 15) , y = (hCentre))
    load = tk.Button(window, image = Load, bg = 'black', width = 110, height = 110, command = comms.loadThread).place(x = (wCentre - (5.15 * wGap) - 20) , y = (hCentre))
    label = tk.Button(window, text = 'Custom Movement Sequence Buttons', bg = 'black', fg = 'white', width = 66, height = 1).place(x = (wCentre - (5.15 * wGap) - 18) , y = (hCentre - 30))

GUI() ## Calls the procedure
