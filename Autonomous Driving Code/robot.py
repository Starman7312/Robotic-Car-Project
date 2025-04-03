import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import os
import numpy as np
import cv2
import hailo
import time
import threading
from gpiozero import CamJamKitRobot

from hailo_apps_infra.hailo_rpi_common import (
    get_caps_from_pad,
    get_numpy_from_buffer,
    app_callback_class,
)
from hailo_apps_infra.detection_pipeline import GStreamerDetectionApp
# Inheritance from the app_callback_class
class user_app_callback_class(app_callback_class):
    def __init__(self):
        """Recursive callback class with user defined data
        """
        super().__init__()

        # Defines variables used for robot control
        
        self.busy = False # Used to check if the robot is busy moving
        self.robot = CamJamKitRobot() # Robot object to command

        self.no_count = 0 # Tracks number of consecutive times target object not seen
        self.count = 0 # Tracks number of consecutive target object seen

# This is the callback function that will be called when data is available from the pipeline
def app_callback(pad, info, user_data):
    """Callback function used to analyse next frame when available

    Args:
        user_data (object): Contains user initialised vars

    Returns:
        _type_: _description_
    """
    # Get the GstBuffer from the probe info
    buffer = info.get_buffer()
    # Check if the buffer is valid
    if buffer is None:
        return Gst.PadProbeReturn.OK

    # Using the user_data to count the number of frames
    user_data.increment()
    string_to_print = f"Frame count: {user_data.get_count()}\n"

    # Get the caps from the pad
    format, width, height = get_caps_from_pad(pad)

    # If the user_data.use_frame is set to True, we can get the video frame from the buffer
    frame = None
    if user_data.use_frame and format is not None and width is not None and height is not None:
        # Get video frame
        frame = get_numpy_from_buffer(buffer, format, width, height)

    # Get the detections from the buffer
    roi = hailo.get_roi_from_buffer(buffer)
    detections = roi.get_objects_typed(hailo.HAILO_DETECTION)

    # Parse the detections
    detection_count = 0
    detected = False
    
    for detection in detections:
        label = detection.get_label() # Gets object seen name
        bbox = detection.get_bbox()
        confidence = detection.get_confidence() # Gets confidence if object
        
        if label == "person" and confidence > 0.4: # Searches for object named here
            detected = True

    if detected:
        user_data.count += 1
        user_data.no_count = 0

        # If target seen 5 times (to prevent false positive)
        if user_data.count > 5 and not user_data.busy:
            user_data.busy = True # Robot busy

            # Creates thread to drive to object
            drive_thread = threading.Thread(target=drive, args=(user_data.robot, 'F'))
            drive_thread.start()

    elif not user_data.busy:
        user_data.no_count += 1
        user_data.count = 0

        if user_data.no_count > 10:
            user_data.busy = True # Robot busy

            # Creates thread to search for object
            drive_thread = threading.Thread(target=drive, args=(user_data.robot, 'L'))
            drive_thread.start()
            
    if user_data.use_frame:
        # Prints detection count to image frame
        cv2.putText(frame, f"Detections: {detection_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Names detected objects image
        cv2.putText(frame, f"{user_data.new_function()} {user_data.new_variable}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Convert the frame to BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        user_data.set_frame(frame)

    print(string_to_print)
    return Gst.PadProbeReturn.OK

def drive(robot, direction):
    """Drives robot motors in specified direction

    Args:
        robot (robot object): robot object to command
        direction (string): string to control direction (F, L)
    """
    # Drives motors in selected direction
    if direction == 'F':
        # Drive to object when seen
        robot.forward()
    else:
        # Search for object by turing left until seen
        robot.left()
        time.sleep(0.2)
        robot.stop()

    time.sleep(0.2) # Pauses to stabilise time
    user_data.busy = False # Task ended, sets flag appropriately
    exit() # Terminates thread


if __name__ == "__main__":
    # Create an instance of the user app callback class
    user_data = user_app_callback_class()
    app = GStreamerDetectionApp(app_callback, user_data)
    app.run()
