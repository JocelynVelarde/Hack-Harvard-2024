import cv2
import cv2.data
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.mongo_connection import insert_file

def crop_frame(file_path, frame, target_x, target_y, target_width, target_height, show_frame=True, save_image=False, file_name='cropped_image.jpg'):
    """
    Crops a region of the image around the given x, y position with the specified width and height.

    :param frame: The frame from which to crop the region.
    :param target_x: The x position to center the crop.
    :param target_y: The y position to center the crop.
    :param target_width: The target width of the crop region.
    :param target_height: The target height of the crop region.
    :param show_frame: Whether to display the frame with the cropped region.
    :param save_image: Whether to save the cropped image to a file.
    :param file_name: The name of the file to save the cropped image.
    """
    video_capture = cv2.VideoCapture(file_path)
    
    # Set the video capture to the frame
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame)

    ret, frame = video_capture.read()

    if not ret:
        print("Failed to capture frame")
        return

    # Get the frame dimensions
    height, width, _ = frame.shape

    # Calculate crop boundaries
    crop_x1 = max(0, target_x - target_width // 2)
    crop_y1 = max(0, target_y - target_height // 2)
    crop_x2 = min(width, target_x + target_width // 2)
    crop_y2 = min(height, target_y + target_height // 2)

    # Crop the region
    cropped_region = frame[crop_y1:crop_y2, crop_x1:crop_x2]

    # Optionally display the cropped region
    if show_frame:
        cv2.imshow('Cropped Region', cropped_region)
        cv2.waitKey(0)

    # Optionally save the cropped region
    if save_image:
        cv2.imwrite(file_name, cropped_region)
        print(f"Cropped image saved as {file_name}")
