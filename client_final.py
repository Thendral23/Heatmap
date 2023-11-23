# import the required dependencies 
import socket
import cv2
import base64
import threading
import time
import logging
import os 
import traceback
from utils import *
from constant import Constant 

# Infinite loop for initializing the client
while True:
    try:
        # Configure the log files for info and error messages
        log_file = "client.log"
        error_log_file = "client_error.log"

        # Clear existing log files
        if os.path.exists(log_file):
            open(log_file, 'w').close()
        if os.path.exists(error_log_file):
            open(error_log_file, 'w').close()

        # Configure the logging for info messages
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%Y %H:%M:%S')

        # Configure the logging for error messages
        error_logger = logging.getLogger('error_logger')
        error_handler = logging.FileHandler(error_log_file)
        error_formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%d-%b-%Y %H:%M:%S')
        error_handler.setFormatter(error_formatter)
        error_logger.addHandler(error_handler)
        error_logger.setLevel(logging.ERROR)

        # Define the server host and port
        server_host = Constant.SERVER_HOST  # Replace with the server's IP or hostname
        server_port = Constant.SERVER_PORT
        break
    except Exception as exception:
        # Log initialization errors
        print("Log file creation failed", f"An error occurred on line {traceback.format_exc()}")
        logging.error("Log file creation failed", f"An error occurred on line {traceback.format_exc()}")
        print("Trying to create log file aftersome time!")
        time.sleep(Constant.TIME_TO_WAIT)
        continue  

# Function to send frames to the server
def send_frames(rtsp_link, cam_id):
    while True:
        try:
            # Assuming internet_connect is a global variable
            if internet_connect:

                # Create a TCP socket for communication with the server
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Connect the client socket to the server at the specified host and port
                client_socket.connect((server_host, server_port))

                # Open a connection to the RTSP stream using OpenCV's VideoCapture
                cap = cv2.VideoCapture(rtsp_link)
                
                # Break out of the loop
                break

            else:
                print("Internet interrupted during video objet or socket object creation creation!!!Trying  aftersome time!!")
                time.sleep(Constant.TIME_TO_WAIT)
                continue 

        except Exception as exception:
            # Log video object creation errors
            print("Video object creation failed", f"An error occurred on line {traceback.format_exc()}")
            logging.error("Video object creation failed", f"An error occurred on line {traceback.format_exc()}")
            print("Trying  aftersome time!")
            time.sleep(Constant.TIME_TO_WAIT)
            continue

    while True:
        try:
            # Check if there is an active internet connection
            if internet_connect:

                # Attempt to read a frame from the RTSP stream
                ret, frame = cap.read()

                # Check if the frame reading was successful
                if not ret:
                    print(f"Frame capture failed for {rtsp_link}")
                    logging.info(f"Frame capture failed for {rtsp_link}")

                    # Release the VideoCapture object and start a new thread
                    cap.release()
                    cap = cv2.VideoCapture(rtsp_link)
                    continue
                    # start_thread()

                # Encode the frame in JPEG format using cv2.imencode() and then base64 encode the result    
                frame_data = base64.b64encode(cv2.imencode('.jpg', frame)[1]) # .decode('utf-8')
                logging.info("Frames are sucessfully b64encoded....")
                
                # Get the size of the base64 encoded frame data
                frame_size = len(frame_data)
                
                # Check if the size of the base64 encoded frame data is greater than 0
                if frame_size > 0:

                    # Send the frame data to the server
                    # print(f"{cam_id}, {frame[10:]}")
                    client_socket.sendall(Constant.CLIENT_ID.encode()+cam_id.encode()+'*cam#'.encode()+frame_data+ "#end#".encode()) 
                    logging.info("Encoded frame (String, bytes) are successfully send into the server")

                else:
                    print(f"Empty frame data for {rtsp_link}. Skipping.")
                    logging.info(f"Empty frame data for {rtsp_link}. Skipping.")
            else:
                print("Internet interrupted during frame creation!!!Trying  aftersome time!!")
                time.sleep(Constant.TIME_TO_WAIT)
                continue

        except Exception as exception:
            # Log frame sending errors
            print("sending frame to server failed", f"An error occurred on line {traceback.format_exc()}")
            logging.error("sending frame to server failed", f"An error occurred on line {traceback.format_exc()}")
            print("Trying  aftersome time!")
            time.sleep(Constant.TIME_TO_WAIT)
            continue
        
        time.sleep(Constant.TIME_TO_WAIT_TO_SEND_FRAMES)

    # Release the VideoCapture object to free resources
    cap.release()
    
    # Close the client socket connection
    client_socket.close()

# Function to start threads for each camera stream    
def start_thread():
    try:
        # Create threads to handle each camera stream
        # Retrieve the RTSP camera URLs from the Constant module
        rtsp_links = Constant.SOURCE_URLS

        # Initialize a counter for creating unique camera IDs
        count = 1

         # Create a dictionary to store camera IDs and their corresponding RTSP URLs
        rtsp_links_dict = {}
        for rtsp in rtsp_links:
            rtsp_links_dict["Cam_"+str(count)] = rtsp
            
            # Increment the count to create a unique camera ID for the next camera
            count += 1

        # Create a list of threads, each targeting the send_frames function for a specific camera
        # threads = [threading.Thread(target=send_frames, args=(rtsp_link,cam_id, )) for (cam_id, rtsp_link) in rtsp_links_dict.items()]

        threads = []
        for (cam_id, rtsp_link) in rtsp_links_dict.items():
            thread = threading.Thread(target=send_frames, args=(rtsp_link,cam_id, ))
            thread.start()
        # Start each thread to concurrently capture and send frames from multiple cameras
        # for thread in threads:
        #     thread.start()

        # Wait for all threads to finish before proceeding
        # for thread in threads:
        #     thread.join()
            
    except Exception as exception:
        # Log thread creation errors
        print("Thread creation failed", f"An error occurred on line {traceback.format_exc()}")
        logging.error("Thread creation failed", f"An error occurred on line {traceback.format_exc()}")
        print("Trying aftersome time!")
        time.sleep(Constant.TIME_TO_WAIT)

# Start the thread creation and execution 
start_thread()
