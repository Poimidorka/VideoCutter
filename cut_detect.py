import cv2
import numpy as np
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import os

def detect_first_brightness_increase(video_path, threshold=30):
    cap = cv2.VideoCapture(video_path)
    ret, prev_frame = cap.read()
    if not ret:
        print("Failed to read the video file.")
        return None
    prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(frame_gray, prev_frame_gray)
        if np.mean(diff) > threshold:
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
            cap.release()
            return timestamp
        prev_frame_gray = frame_gray
    cap.release()
    return None

def cut_video(video_path, start_time, output_path):
    print(start_time)
    print(video_path)
    video = VideoFileClip(video_path).subclip(start_time)
    video.write_videofile(output_path, codec="libx264")

def detect_first_loud_noise(audio_path, threshold=-20, chunk_size=10):
    audio = AudioSegment.from_file(audio_path)
    nonsilent_ranges = detect_nonsilent(audio, min_silence_len=chunk_size, silence_thresh=threshold)
    if nonsilent_ranges:
        return nonsilent_ranges[0][0] / 1000.0
    return None

def extract_audio_from_video(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)

def main(video_path, output_path, brightness_threshold=10, loud_noise_threshold=-20, chunk_size=10, cut_start_time=None):
    brightness_timestamp = detect_first_brightness_increase(video_path, brightness_threshold)
    if brightness_timestamp is None:
        raise ValueError("No brightness increase detected in the video.")
    print(f"First brightness increase detected at: {brightness_timestamp} seconds")
    
    audio_path = "temp_audio.wav"
    extract_audio_from_video(video_path, audio_path)
    loud_noise_timestamp = detect_first_loud_noise(audio_path, loud_noise_threshold, chunk_size)
    os.remove(audio_path)
    if loud_noise_timestamp is None:
        raise ValueError("No loud noise detected in the audio.")
    print(f"First loud noise detected at: {loud_noise_timestamp} seconds")
    
    if cut_start_time is None:
        cut_start_time = brightness_timestamp
    cut_video(video_path, cut_start_time, output_path)
    print(f"Video saved after cutting at: {output_path}")

