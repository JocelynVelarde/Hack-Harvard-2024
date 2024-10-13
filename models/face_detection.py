import cv2
import cv2.data
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.mongo_connection import insert_file

# Initialize the face detector
detector = cv2.FaceDetectorYN_create('./models/yunet/face_detection_yunet_2023mar.onnx', "", (300, 300), score_threshold=0.5)

# Capture video from the default camera (0)

def live_video_detection():
    video_capture = cv2.VideoCapture(0)
        
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        if not ret:
            print("Failed to capture frame")
            break

        detect_frame(frame)
        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close windows
    video_capture.release()

def video_file_detection(file_path):
    video_capture = cv2.VideoCapture(file_path)
    
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        if not ret:
            print("Failed to capture frame")
            break

        detect_frame(frame)
        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close windows
    video_capture.release()

def image_file_detection(file_path):
    frame = cv2.imread(file_path)
    detect_frame(frame)
    cv2.waitKey(0)

def video_timestamp_detection(file_path, frame, show_frame=True):
    video_capture = cv2.VideoCapture(file_path)
    
    # Set the video capture to the frame
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame)

    # Analyze this frame
    ret, frame = video_capture.read()

    if not ret:
        print("Failed to capture frame")
        return
    
    detect_frame(frame, show_frame)
    if show_frame:
        cv2.waitKey(0)

    # Release the video capture and close windows
    video_capture.release()

def video_timestamp_detection(file_path, frame, target_x, target_y, target_width, target_height, show_frame=True, save_image=False):
    video_capture = cv2.VideoCapture(file_path)
    
    # Set the video capture to the frame
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame)

    # Analyze this frame
    ret, frame = video_capture.read()

    if not ret:
        print("Failed to capture frame")
        return
    
    # remove the extension to the file_path
    file_path = file_path.split('.')[0]

    detect_frame(frame, target_x=target_x, target_y=target_y,  target_height=target_height, target_width=target_width, show_frame=show_frame, save_image=save_image, file_name=f'{file_path}_face_detection.jpg')
    if show_frame:
        cv2.waitKey(0)

    # Release the video capture and close windows
    video_capture.release()


def detect_frame(frame, show_frame=True):
    # Get frame dimensions for the detector
    height, width, _ = frame.shape
    detector.setInputSize((width, height))

    # Detect faces in the frame
    num_faces, face_data = detector.detect(frame)

    # Check if any faces are detected
    if num_faces > 0 and face_data is not None:
        for face in face_data:
            # Extract coordinates of the face box
            x, y, w, h = face[:4].astype(int)

            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # convert the frame to an image file
    cv2.imwrite('face_detection.jpg', frame)
    
    insert_file('face_detection.jpg', 'faceDetectionData')

    if show_frame:
        # Display the frame with the face detection
        cv2.imshow('Face Detection', frame)

    os.remove('face_detection.jpg')

def detect_frame(frame, target_x, target_y, target_width, target_height, show_frame=True, save_image=False, file_name='face_detection.jpg'):
    """
    Detects faces in a frame and crops the image to the detected face near a given x, y position, 
    considering the target width and height.

    :param frame: The frame where faces are detected.
    :param target_x: The x position to find the closest face.
    :param target_y: The y position to find the closest face.
    :param target_width: The target width of the region around the x, y position.
    :param target_height: The target height of the region around the x, y position.
    :param proximity: The maximum distance to consider a face near the given x, y position.
    :param show_frame: Whether to display the frame with face detection.
    """
    # Get frame dimensions for the detector
    height, width, _ = frame.shape
    detector.setInputSize((width, height))

    # Detect faces in the frame
    num_faces, face_data = detector.detect(frame)

    # Check if any faces are detected
    if num_faces > 0 and face_data is not None:
        nearest_face = None
        min_distance = float('inf')

        for face in face_data:
            # Extract coordinates of the face box
            x, y, w, h = face[:4].astype(int)

            # Calculate the center of the detected face
            face_center_x = x + w // 2
            face_center_y = y + h // 2

            # Calculate the distance from the target position to the center of the face
            distance = ((face_center_x - target_x) ** 2 + (face_center_y - target_y) ** 2) ** 0.5

            # Check if the face is inside the target region
            if face_center_x > target_x - target_width // 2 and face_center_x < target_x + target_width // 2 and face_center_y > target_y - target_height // 2 and face_center_y < target_y + target_height // 2:
                nearest_face = (x, y, w, h)
                
                # Check if the face is the closest to the target position
                if distance < min_distance:
                    min_distance = distance
                    nearest_face = (x, y, w, h)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                break

        if nearest_face:
            x, y, w, h = nearest_face

            # Define the cropping region using the face box coordinates
            crop_x = max(0, x - 20)
            crop_y = max(0, y - 20)
            crop_x2 = min(width, x + w + 20)
            crop_y2 = min(height, y + h + 20)

            # Ensure the cropping region includes the detected face
            cropped_face = frame[crop_y:crop_y2, crop_x:crop_x2]

            # Save the cropped face
            cv2.imwrite(filename=file_name, img=cropped_face)

            # Optionally display the cropped face
            if show_frame:
                cv2.imshow('Cropped Face', frame)

            # Insert the cropped face into a file
            insert_file(file_name, 'faceDetectionData')

            # Remove the saved image
            if not save_image:
                os.remove(file_name)

def destroy_windwows():
    cv2.destroyAllWindows()

