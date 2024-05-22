import cv2
import numpy as np
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import matplotlib.pyplot as plt
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

def detect_first_loud_noise(audio_path, threshold=0.3, chunk_size=10):
    audio = AudioSegment.from_file(audio_path)
    samples = np.array(audio.get_array_of_samples())
    max_value = np.max(np.abs(samples))
    samples = samples.astype(np.float32) / max_value

    for i, sample in enumerate(samples):
        if abs(sample) > threshold:
            return i / audio.frame_rate
    return None


def extract_audio_from_video(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)

def plot_audio(audio_path):
    audio = AudioSegment.from_file(audio_path)
    samples = np.array(audio.get_array_of_samples())
    max_value = np.max(np.abs(samples))
    samples = samples.astype(np.float32) / max_value

    plt.figure(figsize=(14, 7))
    plt.plot(samples)
    plt.title("Audio dB Values")
    plt.xlabel("Sample")
    plt.ylabel("dB")
    plt.show()

def main(video_path, output_path, brightness_threshold=10, loud_noise_threshold=0.3, chunk_size=10, cut_start_time=None):
    audio_path = "temp_audio.wav"
    extract_audio_from_video(video_path, audio_path)
    plot_audio(audio_path)
    loud_noise_timestamp = detect_first_loud_noise(audio_path, loud_noise_threshold, chunk_size)
    os.remove(audio_path)
    if loud_noise_timestamp is None:
        raise ValueError("No loud noise detected in the audio.")
    print(f"First loud noise detected at: {loud_noise_timestamp} seconds")
    
    if cut_start_time is None:
        cut_start_time = loud_noise_timestamp
    cut_video(video_path, cut_start_time, output_path)
    print(f"Video saved after cutting at: {output_path}")
