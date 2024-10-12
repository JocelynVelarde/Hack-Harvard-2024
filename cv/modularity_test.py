from core_detection import ShopliftingDetector

detector = ShopliftingDetector(api_key_file='service_key.json', project_name="shoplifting-cuzf8", version_num=3)

detector.process_video(video_path="video/short_shoplifting.mp4")

formatted_predictions = detector.get_predictions(formatted=True)
print("Formatted Predictions:\n", formatted_predictions)