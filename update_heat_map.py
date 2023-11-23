# import the required dependencies
import numpy as np
import os
from constant import Constant
import cv2
from datetime import datetime
import json
from utilss import find_files, list_frames

# Constant representing the path for initializing frames
FRAME_INIT_PATH = Constant.INITIAL_FRAME_FOLDER + f"{Constant.CLIENT_ID}\\{Constant.TARGET_CAM}"


class UpdateHeatMap:
    # Constructor to initialize the class instance
    def __init__(self,start_time,end_time):
        try:
            # Initializing attributes for the UpdateHeatMap instance
            self.frame = self.initialize_frame()
            self.heatmap = np.zeros(self.frame.shape[:2], dtype=np.float16)
            # Calculating the update threshold based on start and end times
            self.update_threshold = round(self.calculate_update_threshold(start_time, end_time), 6)
            # Storing the required date-time range for saving the output
            self.requrired_date_time_to_save = (start_time, end_time)
            print(self.update_threshold)
        except Exception as exception:
            print("Constructor method failed while creating heatmap", exception.args)

    # Method to initialize and retrieve the first frame from the specified path
    def initialize_frame(self):
        try:
            # Fetching and reading the initial frame from the specified path
            frame = list_frames(FRAME_INIT_PATH)[0]
            # Reading the selected frame using OpenCV's imread function
            frame = cv2.imread(frame)
            return frame
        except Exception as exception:
            print("initialize_frame_fps method failed.", exception.args)

    def calculate_update_threshold(self, start_time, end_time):
        try:
            total_time = (end_time - start_time)
            # Calculate total frames based on the time duration and average frame count
            total_frames = total_time * Constant.AVG_FRMAE_COUNT
            # Calculate the update threshold based on the total frames
            update_threshold = 255 / total_frames
            # Return the calculated update threshold
            return update_threshold
        except Exception as exception:
            print("calculate_update_threshold method failed while calculating update_threshold", exception.args)

    def update_heatmap(self, data_point):
        try:
        # Update the heatmap using the provided data points
            for point in data_point:
                # Retrieve coordinates and dimensions from data point
                delta_x = point['x']
                delta_y = point['y']
                width = point['width']
                height = point['height']
                # Update the heatmap at the specified region
                self.heatmap[delta_y:delta_y + height, delta_x:delta_x + width] += self.update_threshold
        except Exception as exception:
            print("update_heatmap method failed while updating heatmap", exception.args)
    
    # Function to find JSON files in a directory
    def find_json_files(self):
        # Retrieve the target camera from constants
        Cam = Constant.TARGET_CAM
        # Find JSON files in the specified directory based on the target camera and extension
        json_files = find_files(Constant.SAVE_JSON + f'{Cam}', Constant.JSON_EXTENSION)
        # Return the list of found JSON files
        return json_files
        
        
    def merge_heatmap_with_frame(self):
        try:
            # Initialize the result dictionary with default values
            result = {'status':False, 'status_message':False, 'message':'Update heatmap method failed','image_path':None}
            # Normalize the heatmap to a range of 0-255
            self.heatmap = self.heatmap / np.max(self.heatmap) * 255

            # Generate heatmap overlay using a color map
            heatmap_intensity = self.heatmap.astype(np.uint8)
            heatmap_img = cv2.applyColorMap(heatmap_intensity, cv2.COLORMAP_HOT)

            # Combine the last frame and the heatmap to create the final heatmap image
            heatmap_img = cv2.resize(heatmap_img, (self.frame.shape[1], self.frame.shape[0]))
            heatmap_img = cv2.addWeighted(self.frame, 0.5, heatmap_img, 0.5, 0)
            # Check if the directory to save the output exists, if not, create it
            if not os.path.exists(Constant.WRITE_LOCATION + f"\\{Constant.CLIENT_ID}\\{Constant.TARGET_CAM}"):
                os.makedirs(Constant.WRITE_LOCATION + f"\\{Constant.CLIENT_ID}\\{Constant.TARGET_CAM}", exist_ok=True)
            # Save the merged heatmap and frame image
            if cv2.imwrite(Constant.WRITE_LOCATION + f"\\{Constant.CLIENT_ID}\\{Constant.TARGET_CAM}\\" + f"output_of_{Constant.TARGET_CAM}_on_{Constant.TARGET_DATE}_from_{min(self.requrired_date_time_to_save)}_to_{max(self.requrired_date_time_to_save)}.jpg", heatmap_img):
                print(f"Output for the required date {Constant.TARGET_DATE} and {Constant.TARGET_CAM} saved successfully between the time {min(self.requrired_date_time_to_save)} to {max(self.requrired_date_time_to_save)}.")
                result['status'] = True
                result['status_message'] = True
                result['message'] = f"Output for the required date {Constant.TARGET_DATE} and {Constant.TARGET_CAM} saved successfully between the time {min(self.requrired_date_time_to_save)} to {max(self.requrired_date_time_to_save)}."
                result['image_path'] = Constant.WRITE_LOCATION + f"\\{Constant.CLIENT_ID}\\{Constant.TARGET_CAM}\\" + f"output_of_{Constant.TARGET_CAM}_on_{Constant.TARGET_DATE}_from_{min(self.requrired_date_time_to_save)}_to_{max(self.requrired_date_time_to_save)}.jpg"
            else:
                print("Output saving method failed.")
        except Exception as exception:
            print("Merge_heatmap_with_frame method failed while getting final output.", exception.args)
        finally:
            return result 


    def filter_json(self, folder_path, target_date, target_start, target_end):
        try:
            # Initialize the result dictionary with default values
            result = {'status':False, 'status_message':False, 'message':'Filter_json method failed','image_path':None}
            # Initialize lists to store required data
            required_date = []
            filtered_json_list = []
            available_time = []
            # Traverse through the directory structure
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    # Check if the file is a JSON file
                    if file.endswith('.json'):
                        # Extract the date string from the file name
                        date_str = file.split('___')[1].split('.json')[0][:8]
                        # Check if the date matches the target date
                        if date_str == target_date:
                            # Add the path of the JSON file that matches the target date
                            required_date.append(os.path.join(root, file))
                    for i in required_date:
                        # Extract the time from the file name
                        time_ = int(i.split('___')[1].split('.json')[0][8:10])
                        # Handle special case for midnight (0 hours)
                        if time_ == 0: time_ = 24
                        # Check if the time falls within the specified range
                        if target_start <= time_ and time_ < target_end:
                                print(time_)
                                available_time.append(time_)
                                filtered_json_list.append(os.path.join(root, file))
                                required_date.clear()
            # Update result dictionary based on filtered JSON list
            # Check if any JSON files match the specified criteria
            if len(filtered_json_list) > 0:
                result['status'] = True
                result['message'] = " Filtered_json method sucessfully execueted"
                result['filtered_json_list'] = filtered_json_list
            else:
                result['message'] = "Input date or time are not found. Please enter correct date or time."
                result['filtered_json_list'] = filtered_json_list
            # Update required date and time to save
            self.requrired_date_time_to_save = available_time
        except Exception as exception:
            print("filter_json method failed while filtering json files.", exception.args)
        finally:
            return result
