# Robotic-Car-Project
This is a project containing my A-Level Robotic Car Software, compatible with the CamJamEdukit#3 robotic car kit for Raspberry Pi:

Check out videos of the project here:
https://www.youtube.com/playlist?list=PLHoIQlim7XeMg7k2U5ViysfKgm1ALXoZM

    • The code allows the robot to be controlled remotely using TCP/IP communication (or more simply: using a network / the internet)
    • It provides a graphical user interface with buttons to control the car and other features
    • Provides common key binds for quicker control of the robot (e.g. W, A, S, D)
    • Provides access to a remote camera streaming webpage (via the webpage: http://Pi IP Address:8000/index.html) PS. Enter The Pi IP Into The URL
    • Provides auditory distance alerts (like a car reversing sensor)
    • Provides the car with collision avoidance capabilities

The Controller Code folder contains the code and dependancies that needs to be run on the controller device (e.g. laptop, pc, other raspberry pi etc.)

The Robot Code folder contains the code and dependancies that need to be run on the raspberry pi controlling the robot

------------------------------------------------------------------------------------------------------------------------

Please note:

  • The controller device and Raspberry Pi robot must be connected to the same network for the code to work:
  
      ➤ You can do this using any LAN (e.g. home network)
      ➤ Or by setting up a hotspot on your Raspberry Pi and connecting the host device to this
      
      
  • You will need to edit the code to enter the correct IP addresses:
  
      ➤ These can be found by connecting to the network being used then:
          ⇨ Getting the IP address of each device (e.g. Windows: ipconfig/all or Raspberry Pi OS: ifconfig/all)
          ⇨ And entering it into the appropriate IP variable (comments in the code explain which IP to enter and where)
          ⇨ E.g. ip = 'Raspberry Pi Wireless LAN IP'  # IP of raspberry pi on home LAN
          ⇨ So here you enter the appropriate IP replacing the string

-----------------------------------------------------------------------------------------------------------------------

**To run:**

On Controller Device (PC/Laptop):

    • Run the file named GUI

On Raspberry Pi:

    • Run the file named Drive Software (Sticky)
    • And Camera Streaming Software (if you want to use the cam feed)
