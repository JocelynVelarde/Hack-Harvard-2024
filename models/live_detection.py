import cv2
from roboflow import Roboflow
import os
import sys
# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from collections import deque
import pygame

from api.mongo_connection import insert_json_file


class LiveDetection:
    def __init__(self, api_key_file, project_name, version_num):
        with open(api_key_file, 'r') as f:
            service_key = json.load(f)

        rf = Roboflow(api_key=service_key["api_key"])
        project = rf.workspace().project(project_name)
        self.model = project.version(version_num).model
        self.prediction_data = []
        self.frame_buffer = deque(maxlen=120)

    def process_webcam(self, confidence_threshold=30, overlap_threshold=30, output_json="predictions.json"):
        pygame.init()
        window_width, window_height = 640, 480
        screen = pygame.display.set_mode((window_width, window_height))

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not open webcam.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to capture video from webcam.")
                break

            resized_frame = cv2.resize(frame, (640, 640))

            temp_frame_path = "temp_frame.jpg"
            cv2.imwrite(temp_frame_path, resized_frame)

            prediction = self.model.predict(temp_frame_path, confidence=confidence_threshold, overlap=overlap_threshold).json()

            processed_predictions = self.classify_predictions(prediction['predictions'])

            self.prediction_data.append({
                "frame": len(self.prediction_data), 
                "predictions": processed_predictions
            })

            frame_with_boxes = self.draw_predictions_on_frame(frame, processed_predictions)

            frame_rgb = cv2.cvtColor(frame_with_boxes, cv2.COLOR_BGR2RGB)
            frame_surface = pygame.surfarray.make_surface(frame_rgb.transpose(1, 0, 2))

            screen.blit(frame_surface, (0, 0))
            pygame.display.update()

            os.remove(temp_frame_path)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cap.release()
                    pygame.quit()

                    self.save_predictions_to_json(output_json)
                    print(f"Predictions saved to {output_json}.")
                    return

    def classify_predictions(self, predictions):
        processed_predictions = []
        detected_dangerous = False  # Track if "dangerous" level is detected

        for obj in predictions:
            confidence = obj['confidence']
            label = obj['class']
            x = obj['x']
            y = obj['y']

            if confidence > 0.6:
                level = 'normal'
                self.message_sent = False  # Reset the flag when back to normal
            elif 0.4 <= confidence < 0.6:
                level = 'dangerous'
                detected_dangerous = True

                # Send a WhatsApp message if the level is 'dangerous' and no message has been sent yet
                if not self.message_sent:
                    message = f"Warning: Dangerous activity detected! Class: {label}, Confidence: {confidence:.2f}, Coordinates: (x: {x}, y: {y})"
                    to_phone_number = "+13219788930"  # Replace with your actual number
                    WhatsappSender.send_message(to_phone_number, message)
                    print(f"Message sent: {message}")
                    self.message_sent = True  # Ensure the message is only sent once
            else:
                level = 'suspicious'

            processed_predictions.append({
                "x": obj['x'],
                "y": obj['y'],
                "width": obj['width'],
                "height": obj['height'],
                "confidence": confidence,
                "class": label,
                "level": level
            })

        return processed_predictions

    def draw_predictions_on_frame(self, frame, predictions):
        for obj in predictions:
            x0 = int(obj['x'] - obj['width'] / 2)
            y0 = int(obj['y'] - obj['height'] / 2)
            x1 = int(obj['x'] + obj['width'] / 2)
            y1 = int(obj['y'] + obj['height'] / 2)

            label = f"{obj['class']}: {obj['level']} ({obj['confidence']:.2f})"

            cv2.rectangle(frame, (x0, y0), (x1, y1), (0, 255, 0), 2)
            cv2.putText(frame, label, (x0, y0 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        return frame

    def save_predictions_to_json(self, output_json):
        with open(output_json, 'w') as json_file:
            json.dump(self.prediction_data, json_file, indent=4)
        print(f"Predictions saved to {output_json}.")

if __name__ == "__main__":
    detector = LiveDetection(api_key_file='cv/service_key.json', project_name="shoplifting-cuzf8", version_num=3)
    insert_json_file("predictions_output.json", "json", "json_live_video")
    detector.process_webcam(output_json="predictions_output.json")
