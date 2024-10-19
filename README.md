# Robotic-Car-Project
This is a project containing my A-Level robotic car software, compatible with the CamJamEdukit#3 robotic car kit for Raspberry Pi

The Controller Code folder contains the code and dependancies that needs to be run on the controller device (e.g. laptop, pc, other raspberry pi etc.)
The Robot Code golder contains the code and dependancies that need to be run on the raspberry pi controlling the robot

Please note:\n
  • The controller device and Raspberry Pi robot must be connected to the same network for the code to work:
      • You can do this using any LAN (e.g. home network)
      • Or by setting up a hotspot on your Raspberry Pi and connecting the host device to this
  • You will need to edit the code to enter the correct IP addresses:
      • These can be found by connecting to the network being used then:
          • Getting the IP address of each device (e.g. Windows: ipconfig/all or Raspberry Pi OS: ifconfig/all)
