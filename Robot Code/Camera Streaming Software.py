import io
import logging
import socketserver
from http import server
from threading import Condition
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from libcamera import controls
from libcamera import Transform

# Source code modified and reproduced under the BSD-2 Clause License, from: https://github.com/raspberrypi/picamera2

# Sets the host IP address


def setIP():
    opt = 0
    count = 0

    while opt > 4 or opt < 1:
        try:
            opt = int(input('Set Host IP:\n1: Pi Hotspot (Raspberry Pi Hotspot IP)\n2: Wireless LAN (Raspberry Pi Wireless LAN IP)\n3: Wired LAN (Raspberry Pi Wired LAN IP)\n4: Other\n\nChoice: '))
        except ValueError:  # Loops when an value error occurs
            opt = 0
    if opt == 1:
        ip = 'Raspberry Pi Hotspot IP'  # Rasperry Pi Hotspot IP
    elif opt == 2:
        ip = 'Raspberry Pi Wireless LAN IP'  # Wireless Home LAN IP
    elif opt == 3:
        ip = 'Raspberry Pi Wired LAN IP'  # Wired Home LAN IP
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

    return ip  # Returns the selected IP


ip = setIP()  # Runs the set IP procedure

# Sets the camera footage resolution


def setRes():
    opt = 0

    while opt > 5 or opt < 1:
        try:
            opt = int(input('Select Quality:\n1. Ultra High (2304 * 1296)\n2. High (1920 * 1080)\n3. Medium (1280 * 720)\n4. Low (960 * 540)\n5. Very Low (640 * 360)\n\nChoice: '))
            print()
        except ValueError:  # Loops when an value error occurs
            opt = 0

    if opt == 1:  # UHD Camera resolution
        width = 2304
        height = 1296
    elif opt == 2:  # HD Camera Resolution
        width = 1920
        height = 1080
    elif opt == 3:  # Medium Camera Resolution
        width = 1700
        height = 850
    elif opt == 4:  # Low Camera Resolution
        width = 1280
        height = 720
    else:  # Very Low Camera Resolution
        width = 640
        height = 360

    return width, height  # Returns width and height values


width, height = setRes()  # Sets camera resolution

# Sets the frames per second for the camera to capture


def setFrameRate():
    opt = 0

    while opt > 6 or opt < 1:
        try:
            opt = int(input(
                'Select Frame Rate:\n1. 60 FPS\n2. 56\n3. 30 FPS\n4. 20 FPS\n5. 15 FPS\n6. Other\n\nChoice: '))
        except ValueError:  # Loops when an value error occurs
            opt = 0
    if opt == 1:
        fps = 60
    elif opt == 2:
        fps = 56
    elif opt == 3:
        fps = 30
    elif opt == 4:
        fps = 20
    elif opt == 5:
        fps = 15
    else:
        fps = 0
        skip = False
        while fps < 1 or fps > 120:  # Validates the framerate is in a reasonable range
            try:
                # Allows for a custom no. to be set
                fps = int(input('Enter FPS: '))
                skip = False
            except ValueError:
                fps = 0
                print('\n*Error: Data must only contain numbers*\n')
                skip = True

            if (fps < 1 or fps > 120) and not skip:
                print('\n*Error: FPS must be between 1-120 FPS*\n')
                skip = False

    return fps


fps = setFrameRate()  # Runs the set frame rate function

# Creates the webpage used to stream the camera footage
PAGE = """\
<html>
<head>
<!-- Sets webpage styles via inline CSS -->
<style>
h1 {
	font-family: Verdana;
	font-size: 30px;
	text-align: center; /* Aligns text centrally */
	color: #ff0000; /* Sets text colour */
	background-color: #1034A6; /* Sets background colour */
	border-width: 0px;
	border-style: solid;
	border-color: #039; /* Sets border colour */
	width: 100%; /* Sets border to be 100% zoomed */
	height: 40px; /* Sets border height */
}

body {
	text-align: center; /* Centres video feed */
	margin: 0;
}
</style>
<title>Robot Live Camera Feed</title> <!-- Titles the tab -->
</head>
<body>
<h1>Robot Live Camera Feed</h1> <!-- Titles the webpage -->
<img src="stream.mjpg" width="1280" height="720" /> <!-- Inserts the webcam feed into the webpage -->
</body>
</html>
"""

# Class to handle streaming output


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

# Class to handle HTTP requests


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Redirects root path to index.html for streaming
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            # Serves the HTML page to the client
            # Encodes website HTML in the utf-8 format
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            # Set up MJPEG streaming of camera feed
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header(
                'Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:  # Streams video feed to webpage
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)  # Inserts video into page
                    self.wfile.write(b'\r\n')
            except Exception as e:  # Outputs the error code when a client is removed and outputs their ip and port
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            # Handles 404 Not Found error
            self.send_error(404)
            self.end_headers()

# Class to handle streaming server


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    # Ensures that the same socket address (host, port) can be rebound, preventing lag
    allow_reuse_address = True
    # Sets threaded functions to exit automatically when main program exits
    daemon_threads = True


# Instantiates camera and starts it running
picam2 = Picamera2()
# Reconfigures video so it isn't upside down or horizontally inverted
picam2.configure(picam2.create_video_configuration(
    transform=Transform(vflip=True, hflip=True), main={"size": (width, height)}))
picam2.set_controls({'FrameRate': fps})  # Sets the frame rate

# config = picam2.create_preview_configuration({'size': (width, height)})
# picam2.align_configuration(config)

output = StreamingOutput()  # Instantiates the stream output class
# Starts video recording and streaming
picam2.start_recording(JpegEncoder(), FileOutput(output))

try:
    # Initiates the streaming server
    address = (ip, 8000)  # Sets the address (host, port) to be used
    # Sets up the server for streaming and connecting to
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()  # Keeps server streaming video
finally:
    # Shuts down the camera when an interrupt occurs
    picam2.stop_recording()
