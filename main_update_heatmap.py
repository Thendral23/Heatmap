# import the required dependencies
from update_heat_map import UpdateHeatMap
from constant import Constant
import json
import os

# Constants for different parameters
# Setting JSON root directory
JSON_ROOT_DIR = Constant.SAVE_JSON+f"{Constant.CLIENT_ID}"
# Setting the target camera
TARGET_CAM = Constant.TARGET_CAM
# Setting the target date
TARGET_DATE = Constant.TARGET_DATE
# Setting the start time to update heatmap
TARGET_START = Constant.START_TIME_TO_UPDATE_HM
# Setting the end time to update heatmap
TARGET_END = Constant.END_TIME_TO_UPDATE_HM

# Main function for generating the heatmap
def main_generate_heatmap(json_root_dir, target_cam, target_date, target_start, target_end):
    try:
        # Initializing result dictionary with default values
        result = {'status':False, 'status_message':False, 'message':'Update heatmap method failed','image_path':None}
        # Checking if the path exists for the target camera within the JSON root directory
        if os.path.exists(json_root_dir + f'\\{target_cam}'):
            # Creating an instance of UpdateHeatMap class
            updateheatmap = UpdateHeatMap(target_start,target_end)
            # Looping continuously
            while True:
                # Filtering the JSON files based on criteria
                filter_list = updateheatmap.filter_json(json_root_dir + f'\\{target_cam}', target_date, target_start, target_end)
                # Handling scenarios based on the filtered JSON list
                if not filter_list['status']:
                    print("Please enter the correct value of time.\n(or)\nThere is no data points saved in that time you have entered.")
                    result['message'] = filter_list['message']
                    return result
                else:
                    # Processing each filtered JSON file
                    for data_list in filter_list['filtered_json_list']:
                        # Opening each JSON file in read mode
                        with open(data_list, 'r') as json_file:
                            # Loading JSON content into a Python data structure
                            data_points = json.load(json_file)
                        # Updating the heatmap using the loaded data points from the JSON file
                        updateheatmap.update_heatmap(data_points)
                    # Merging the heatmap with frames
                    result = updateheatmap.merge_heatmap_with_frame()
                    return result
                break
        else:
            print("Invalid cam input or the cam you have entered is not found.")
            result['status'] = True
            result['message'] =  "invalid cam input or the cam you have entered is not found."
            return result
    except Exception as exception:
        print("Main_update_heat_map method failed.", exception.args)

# Main function to get the list of camera directories
def main_cam_list():
    try:
        # Initializing a list to store camera directory names
        cam_directory_list = []
        result = {'status':False, 'message':'Update heatmap method failed','cam_directory_list': None}
        # Scanning directory entries
        with os.scandir() as entries:
            for entry in entries:
                # Checking if it's a directory
                if entry.is_dir(JSON_ROOT_DIR):
                    # Adding directory name to the list
                    cam_directory_list.append(entry.name)
        # Checking if camera directories are found
        if len(cam_directory_list) > 0:
            result['status'] = True
            result['message'] = f"{len(cam_directory_list)} Camera(s) found."
            result['cam_directory_list'] = cam_directory_list
        else:
            result['message'] = "No Camera(s) found."
    except Exception as exception:
        print("Main cam_list method is failed.", exception.args)
    finally:
        # Returning the result dictionary
        return result


# Calling the main_generate_heatmap function with specified parameters
main_generate_heatmap(JSON_ROOT_DIR, TARGET_CAM, TARGET_DATE, TARGET_START, TARGET_END)


# max scalar , pixel depth