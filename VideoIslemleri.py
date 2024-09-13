import cv2
import numpy as np
import tempfile

def CozunurlukDusurme(video_data):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_input_video:
        temp_input_video.write(video_data)
        temp_input_video_path = temp_input_video.name
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_output_video:
        temp_output_video_path = temp_output_video.name
    cap = cv2.VideoCapture(temp_input_video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    new_width = int(frame_width * 0.5)
    new_height = int(frame_height * 0.5)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_output_video_path, fourcc, fps, (new_width, new_height))
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        resized_frame = cv2.resize(frame, (new_width, new_height))
        out.write(resized_frame)
    cap.release()
    out.release()
    with open(temp_output_video_path, 'rb') as output_video_file:
        reduced_video_data = output_video_file.read()
    import os
    os.remove(temp_input_video_path)
    os.remove(temp_output_video_path)
    return reduced_video_data


def VideoKareYakala(video_data):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
        temp_video.write(video_data)
        temp_video_path = temp_video.name
    cap = cv2.VideoCapture(temp_video_path)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise ValueError("Videodan kare çekilemedi.")
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame_rgb