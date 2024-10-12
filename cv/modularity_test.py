from core_detection import ShopliftingDetector

detector = ShopliftingDetector(api_key_file='service_key.json', project_name="shoplifting-cuzf8", version_num=3)

detector.process_video(video_path="video/group1_sidecam1.mp4", output_video_path="group1_sidecam1_exp.mp4")

#formatted_predictions = detector.get_predictions(formatted=True)
#print("Formatted Predictions with Levels:\n", formatted_predictions)