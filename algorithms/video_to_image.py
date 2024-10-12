import cv2
import os

def save_img_range(video_path, start_sec, stop_sec, step_sec,
                         dir_path, basename, ext='jpg'):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

    fps = cap.get(cv2.CAP_PROP_FPS)
    fps_inv = 1 / fps

    sec = start_sec
    while sec < stop_sec:
        n = round(fps * sec)
        cap.set(cv2.CAP_PROP_POS_FRAMES, n)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(
                '{}_{}_{:.2f}.{}'.format(
                    base_path, str(n).zfill(digit), n * fps_inv, ext
                ),
                frame
            )
        else:
            return
        sec += step_sec