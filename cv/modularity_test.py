from core_detection import ShopliftingDetector

detector = ShopliftingDetector(api_key_file='service_key.json', project_name="shoplifting-cuzf8", version_num=3)

detector.process_video(
    video_path="video/vid1_cam2_trimmed.mp4", 
    output_video_path="vid1_cam2_labeled.mp4", 
    json_output_path="predictions_output.json"
)