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

You can then run the code:
- ```bash
  python path/robot.py --input rpi
  ```
- Replace *path* with the path to the robot.py file
- e.g. /home/*username*/Robotic-Car-Project/Autonomous Driving Code/robot.py or e.g. /home/*username*/Downloads/Robotic-Car-Project/Autonomous Driving Code/robot.py
- You may need to modify the input command if not using picamera2
- Run --help for options in this case to see how
