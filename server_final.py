# import the required dependencies
import socket
import os
import cv2
import base64
import numpy as np
import threading
from datetime import datetime
import logging
import os 
import time
import traceback
from utils import resize
from constant import Constant
import shutil


# Function to create a folder for the current hor with start times
def create_hour_folder(client_id, cam_id, folder_name):
    try:
        if Constant.current_dir is not None:
            if not os.path.exists(Constant.current_dir): 
                move_dir = os.path.abspath(f"{Constant.PATH_SAVE_FRAMES}\\{client_id}\\{cam_id}\\saved_folder")
                os.makedirs(move_dir, exist_ok=True)
                shutil.move(os.path.abspath(f"{Constant.PATH_SAVE_FRAMES}\\{client_id}\\{cam_id}\\current_folder\\{str(int(folder_name)-1)}"), move_dir)
                save_directory = os.path.abspath(f"{Constant.PATH_SAVE_FRAMES}\\{client_id}\\{cam_id}\\current_folder\\{folder_name}")
                os.makedirs(save_directory, exist_ok=True)
                return save_directory
            else:
                save_directory = os.path.abspath(f"{Constant.PATH_SAVE_FRAMES}\\{client_id}\\{cam_id}\\current_folder\\{folder_name}")
                # os.makedirs(save_directory, exist_ok=True)
                return save_directory

        elif Constant.current_dir is None:
            folder_to_move = f"{Constant.PATH_SAVE_FRAMES}\\{client_id}\\{cam_id}\\current_folder"
            if not os.path.exists(folder_to_move):
                os.makedirs(folder_to_move, exist_ok=True)
            dir_to_move = f"{Constant.PATH_SAVE_FRAMES}\\{client_id}\\{cam_id}\\saved_folder"
            count = 1
            for existing_frames_folder in os.listdir(folder_to_move):
                folder_to_move_ = os.path.join(dir_to_move, existing_frames_folder)
                if os.path.exists(folder_to_move_):
                    re_folder_to_move_ = folder_to_move_ + '_' + str(count)
                    try:
                        os.rename(folder_to_move_, re_folder_to_move_)
                        shutil.move(re_folder_to_move_, dir_to_move)
                    except:
                        pass
                    count += 1
                    continue
                shutil.move(os.path.join(folder_to_move, existing_frames_folder), dir_to_move)
            save_directory = os.path.abspath(f"{Constant.PATH_SAVE_FRAMES}\\{client_id}\\{cam_id}\\current_folder\\{folder_name}")
            os.makedirs(save_directory, exist_ok=True)
            return save_directory
    except Exception as exception:
        print("Error occurred while receiving bit(str) from the client.", f"An error occurred on line {traceback.format_exc()}")
        

def receive_and_save_frames(client_socket, Camera):
    while True:
        try:
            # Initialize an empty bytes object to store frame data
            frame_data = b''

            while True:
                try:
                    # Receive a packet of specified length from the client
                    packet = client_socket.recv(Constant.BYTE_LENGTH)
                    
                    # Check if no data is received in the current packet
                    if not packet:
                        # Break the loop if no more data is received (end of transmission)
                        break

                    # Accumulate the received packet to reconstruct the complete frame data
                    frame_data += packet

                    # Decode the accumulated frame data into a string
                    frame_data_decode = frame_data.decode()
                    
                    # Check if a special marker '*cam#' is present in the decoded frame data
                    if '*cam#' in frame_data_decode:
                        # Extract the client_id from the frame data
                        client_id = frame_data_decode[:Constant.CLIENT_ID_INDEXING_END]
                        # Extract the cam_id from the frame data
                        cam_id = frame_data_decode[Constant.CAM_ID_INDEXING_START:Constant.CAM_ID_INDEXING_END]
                        # Remove the metadata prefix, leaving only the frame data
                        frame_data_decode = frame_data_decode[Constant.FRAME_DATA_DECODE_INDEXING_START:]
                    
                    # Check if the end marker "#end#" is present in the decoded frame data
                    if "#end#" in frame_data_decode:
                        # Remove the end marker from the frame data
                        frame_data = frame_data_decode.replace("#end#", '')
                        # Break the loop as the end of the frame data is reached
                        break

                except Exception as exception:
                    print("Error occurred while adding packet to frame_data.", f"An error occurred on line {traceback.format_exc()}")
                    logging.error("Error occurred while adding packet to frame_data.", f"An error occurred on line {traceback.format_exc()}")
                    print("Trying to add packet to frame_data after some time!")
                    time.sleep(Constant.time_to_wait)
            
            # Check if no frame data is accumulated
            if not frame_data:
                # Break the loop if there is no more frame data, indicating the end of the frame transmission
                break
            
            # Store the accumulated frame data before decoding
            base64_data = frame_data

            # Decode the accumulated base64-encoded frame data
            frame_data = base64.b64decode(base64_data)
            logging.info("Bytes, string are b64decoded into frame from the client...")
            
            # Check if the decoded frame data is empty
            if len(frame_data) == 0:
                print("Received empty frame data. Skipping.")
                logging.info("Received empty frame data. Skipping.")
                continue
            
            # Decode the raw frame data using OpenCV
            frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
            
            # Check if the frame decoding was successful
            if frame is not None:
                now = datetime.now()
                timestamp_folder = now.strftime("%Y%m%d%H")
                folder_name = f"{timestamp_folder}"
                
                # Create a folder structure based on the current time for storing received frames
                save_directory = create_hour_folder(client_id, cam_id, folder_name)
                Constant.current_dir = save_directory
                timestamp_frame = now.strftime("%Y%m%d%H%M%S")

                # Generate a unique path for saving the frame as an image file
                frame_path = os.path.join(save_directory, f'frame_{timestamp_frame}.jpg')

                # Assuming 'resize' is defined in 'utils', resize the frame
                frame = resize(frame)
                
                # Save the frame as an image file
                cv2.imwrite(frame_path, frame)
                print(f"Frame is successfully saved in the server: {frame_path}")
                logging.info(f"Frame is successfully saved in the server: {frame_path}")

            else:
                print("Failed to decode the frame. Skipping.")
                logging.info("Failed to decode the frame. Skipping.")

        except Exception as exception:
            print("Error occurred while receiving bit(str) from the client.", f"An error occurred on line {traceback.format_exc()}")
            logging.error("Error occurred while receiving bit(str) from the client.", f"An error occurred on line {traceback.format_exc()}")
            print("Trying to receive bit(str) from the client after some time!")
            time.sleep(Constant.TIME_TO_WAIT)

    print(f"Frames received and saved for client {Camera}")
    logging.info(f"Frames received and saved for client {Camera}")

while True:
    try:
        # Configure the log files for info and error messages
        log_file = "server.log"
        error_log_file = "server_error.log"

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
        break
    except Exception as exception:
        print("Log file creation failed", f"An error occurred on line {traceback.format_exc()}")
        logging.error("Log file creation failed", f"An error occurred on line {traceback.format_exc()}")
        print("Trying to create log file after some time!")
        time.sleep(Constant.time_to_wait)
        continue

while True:
    try:
        # Listen on all available interfaces
        server_host = '0.0.0.0' 

        # Define the port for the server to listen on
        server_port = Constant.SERVER_PORT
        
        # Create a TCP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the specified host and port
        server_socket.bind((server_host, server_port))

        #Start listening for incoming client connections with a maximum queue size of 5
        server_socket.listen(5)
        print(f"Server listening on {server_host}:{server_port}")
        logging.info(f"Server listening on {server_host}:{server_port}")
        break

    except Exception as exception:
        print("Error occurred while creating socket object", f"An error occurred on line {traceback.format_exc()}")
        logging.error("Error occurred while creating socket object", f"An error occurred on line {traceback.format_exc()}")
        print("Trying to create socket object after some time!")
        time.sleep(Constant.TIME_TO_WAIT)
        continue

while True:
    try:
        # Accept an incoming client connection
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        logging.info(f"Accepted connection from {addr}")
        
        # Generate a unique identifier for the client thread (e.g., camera)
        Camera = str(threading.active_count())

        # Create a new thread to handle the client
        client_thread = threading.Thread(target=receive_and_save_frames, args=(client_socket, Camera))

        # Start the client thread to handle frame reception and saving
        client_thread.start()

    except Exception as exception:
        print("Error occurred while creating client connection.", f"An error occurred on line {traceback.format_exc()}")
        logging.error("Error occurred while creating client connection.", f"An error occurred on line {traceback.format_exc()}")
        print("Trying to create client connection after some time!")
        time.sleep(Constant.time_to_wait)
        continue
































































# import socket
# import os
# import cv2
# import struct
# import base64
# import numpy as np
# import threading
# from datetime import datetime
# import logging
# import os 
# import time
# import traceback
# from utils import *
# from constant import Constant

# while True:
#     try:
#         # Configure the log files for info and error messages
#         log_file = "server.log"
#         error_log_file = "sever_error.log"

#         # Clear existing log files
#         if os.path.exists(log_file):
#             open(log_file, 'w').close()
#         if os.path.exists(error_log_file):
#             open(error_log_file, 'w').close()

#         # Configure the logging for info messages
#         logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%Y %H:%M:%S')

#         # Configure the logging for error messages
#         error_logger = logging.getLogger('error_logger')
#         error_handler = logging.FileHandler(error_log_file)
#         error_formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%d-%b-%Y %H:%M:%S')
#         error_handler.setFormatter(error_formatter)
#         error_logger.addHandler(error_handler)
#         error_logger.setLevel(logging.ERROR)
#         break
#     except Exception as exception:
#         print("Log file creation failed", f"An error occurred on line {traceback.format_exc()}")
#         logging.error("Log file creation failed", f"An error occurred on line {traceback.format_exc()}")
#         print("Trying to create log file aftersome time!")
#         time.sleep(Constant.time_to_wait)
#         continue        


# def receive_and_save_frames(client_socket, Camera):
#     #frame_counter = 0

#     while True:
#         try:
#             frame_data = b''
#             while True:
#                 try:
#                     packet = client_socket.recv(Constant.BYTE_LENGTH)
#                     #print(f'while 57 {packet[:5]}')
#                     if not packet:
#                         break
#                     frame_data += packet
#                     frame_data_decode = frame_data.decode()
#                     # Need to change as switchcase 
#                     if '*cam#' in frame_data_decode:
#                         client_id = frame_data_decode[:Constant.CLIENT_ID_INDEXING_END]
#                         cam_id = frame_data_decode[Constant.CAM_ID_INDEXING_START:Constant.CAM_ID_INDEXING_END]
#                         frame_data_decode = frame_data_decode[Constant.FRAME_DATA_DECODE_INDEXING_START:]
#                     if "#end#" in frame_data_decode:
#                         frame_data = frame_data_decode.replace("#end#", '')
#                         break
#                 except Exception as exception:
#                     print("Error occured while adding packet to frame_data.", f"An error occurred on line {traceback.format_exc()}")
#                     logging.error("Error occured while adding packet to frame_data.", f"An error occurred on line {traceback.format_exc()}")
#                     print("Trying to add packet to frame_data aftersome time!")
#                     time.sleep(Constant.time_to_wait)

#             if not frame_data:
#                 break
#             base64_data = frame_data

#             frame_data = base64.b64decode(base64_data)
#             logging.info("Bytes, string are b64decoded into frame from client...")
#             if len(frame_data) == 0:
#                 print("Received empty frame data. Skipping.")
#                 logging.info("Received empty frame data. Skipping.")
#                 continue

#             frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)

#             if frame is not None:
#                 now = datetime.now()
#                 timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
#                 save_directory = os.path.abspath(f"received_frames/{client_id}/{cam_id}")
#                 os.makedirs(save_directory, exist_ok=True)
#                 frame_path = os.path.join(save_directory, f'frame_{timestamp}.jpg')
#                 # print("B4", frame.shape)
#                 frame = resize(frame)
#                 # print("Ater", frame.shape)
#                 cv2.imwrite(frame_path, frame)
#                 print(f"Frame is successfully saved in the server: {frame_path}")
#                 logging.info(f"Frame is successfully saved in the server: {frame_path}")
#             else:
#                 print("Failed to decode the frame. Skipping.")
#                 logging.info("Failed to decode the frame. Skipping.")

#             #frame_counter += 1
#         except Exception as exception:
#             print("Error occured while Receiving bit(str) from client.", f"An error occurred on line {traceback.format_exc()}")
#             logging.error("Error occured while Receiving bit(str) from client.", f"An error occurred on line {traceback.format_exc()}")
#             print("Trying to receive bit(str) from client aftersome time!")
#             time.sleep(Constant.time_to_wait)
#             continue

#     print(f"Frames received and saved for client {Camera}")
#     logging.info(f"Frames received and saved for client {Camera}")

# while True:
#     # Define the server host and port
#     try:
#         server_host = '0.0.0.0'  # Listen on all available interfaces
#         server_port = Constant.server_port

#         # Create a socket object
#         server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         server_socket.bind((server_host, server_port))
#         server_socket.listen(5)
#         print(f"Server listening on {server_host}:{server_port}")
#         logging.info(f"Server listening on {server_host}:{server_port}")
#         break
#     except Exception as exception:
#         print("Error occured while creating socket object", f"An error occurred on line {traceback.format_exc()}")
#         logging.error("Error occured while creating socket object", f"An error occurred on line {traceback.format_exc()}")
#         print("Trying to create socket object aftersome time!")
#         time.sleep(Constant.time_to_wait)
#         continue
# while True:
#     try:
#         client_socket, addr = server_socket.accept()
#         print(f"Accepted connection from {addr}")
#         logging.info(f"Accepted connection from {addr}")

#         # Assign a client ID based on the order of connection
#         Camera = str(threading.active_count())

#         client_thread = threading.Thread(target=receive_and_save_frames, args=(client_socket, Camera))
#         client_thread.start()
#     except Exception as exception:
#         print("Error occured while creating client connection.", f"An error occurred on line {traceback.format_exc()}")
#         logging.error("Error occured while creating client connection.", f"An error occurred on line {traceback.format_exc()}")
#         print("Trying to create client connection aftersome time!")
#         time.sleep(Constant.time_to_wait)
#         continue
