from api.mongo_connection import insert_file, insert_json_file

insert_file("vid1_cam1_labeled.mp4", "videoData")
insert_json_file("vid1_cam1_predictions.json", "predictionData", "prediction")

insert_file("vid3_cam1_labeled.mp4", "videoData")
insert_json_file("vid3_cam1_predictions.json", "predictionData", "prediction")

insert_file("vid4_cam3_labeled.mp4", "videoData")
insert_json_file("vid4_cam3_predictions.json", "predictionData", "prediction")

insert_file("vid5_cam1_labeled.mp4", "videoData")
insert_json_file("vid5_cam1_predictions.json", "predictionData", "prediction")


