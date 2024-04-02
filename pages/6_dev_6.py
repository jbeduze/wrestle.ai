import streamlit as st
import cv2
import tempfile
import numpy as np
from moviepy.editor import VideoFileClip
import os

st.title('Video Segment Extractor')

video_file_buffer = st.file_uploader("Upload a Video", type=["mp4", "mov", "avi", "mkv"])
if video_file_buffer is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(video_file_buffer.read())
    video_path = tfile.name
    
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps

    # Play the video
    st.video(video_path)

    # Slider for marking start and end points
    start_time, end_time = st.slider("Mark the start and end points:", 0.0, duration, (0.0, duration), step=1/fps, format="%.2f s")
