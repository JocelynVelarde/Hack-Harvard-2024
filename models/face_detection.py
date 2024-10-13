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

def video_timestamp_detection(file_path, frame):
    video_capture = cv2.VideoCapture(file_path)
    
    # Set the video capture to the frame
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame)

    # Analyze this frame
    ret, frame = video_capture.read()

    if not ret:
        print("Failed to capture frame")
        return
    
    detect_frame(frame)
    cv2.waitKey(0)

    # Release the video capture and close windows
    video_capture.release()

def detect_frame(frame):
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

    os.remove('face_detection.jpg')

    # Display the resulting frame
    cv2.imshow('Face Detection', frame)

cv2.destroyAllWindows()
