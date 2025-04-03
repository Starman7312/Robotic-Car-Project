# Machine Learning Powered Autonamous Driving of the robot  

## Dependancies:  
- Uses the HAILO Raspberry PI AI HAT NPU Accelerator: [Raspberry PI AI HAT](https://www.raspberrypi.com/products/ai-hat/)  
- You must have set this repository up first: [hailo-rpi5-examples](https://github.com/hailo-ai/hailo-rpi5-examples) 

## Running the code:  
You must access the **Venv** installed from the **hailo-rpi5-examples** library:
- ```bash
  cd hailo-rpi5-examples
  ```
- ```bash
  source setup_env.sh
  ```
You must also have downloaded the robot.py file located within this folder:
[robot.py](https://github.com/Starman7312/Robotic-Car-Project/blob/2722a39ef8a3fbd1f0c879badb777c0f49078721/Autonomous%20Driving%20Code/robot.py)

You can then run the code within the Venv:
- ```bash
  python path/robot.py --input rpi
  ```
- Replace *path* with the path to the robot.py file
- >e.g. /home/*username*/Robotic-Car-Project/Autonomous Driving Code/robot.py  
  >e.g. /home/*username*/Downloads/Robotic-Car-Project/Autonomous Driving Code/robot.py  
- You may need to modify the input command if not using picamera2
- Run --help for options in this case to see how

## Notes:
- You must run within the Venv to access dependecy files for communicating with the AI HAT
