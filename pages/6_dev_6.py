import streamlit as st
import cv2
import tempfile
import numpy as np
from moviepy.editor import VideoFileClip
import os

st.title('Video Segment Extractor')

#extract videos or single images for ai analysis



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

    options = st.selectbox(
        "Extract either a single frame or video segment for analysis", 
        ("Video Segment", "Single Image"),
        index=None,
        placeholder="Select imaging method...",
    )

        # Slider for marking start and end points
        start_time, end_time = st.slider("Mark the start and end points:", 0.0, duration, (0.0, duration), step=1/fps, format="%.2f s")
        
def get_frame_at_time(video_path, time_in_seconds):
    clip = VideoFileClip(video_path)
    frame = clip.get_frame(time_in_seconds)
    clip.close()
    return frame

if video_file_buffer is not None:
    col1, col2 = st.columns(2)
    with col1:
        st.write("Start Frame")
        start_frame_img = get_frame_at_time(video_path, start_time)
        st.image(start_frame_img, use_column_width=True)

    with col2:
        st.write("End Frame")
        end_frame_img = get_frame_at_time(video_path, end_time)
        st.image(end_frame_img, use_column_width=True)
        
def extract_video_segment(video_path, start_time, end_time, output_path):
    clip = VideoFileClip(video_path).subclip(start_time, end_time)
    clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    clip.close()

if video_file_buffer is not None and st.button("Extract Segment"):
    output_path = tempfile.mktemp(suffix=".mp4")
    extract_video_segment(video_path, start_time, end_time, output_path)
    
    with open(output_path, "rb") as file:
        btn = st.download_button(
                label="Download Video Segment",
                data=file,
                file_name="extracted_segment.mp4",
                mime="video/mp4"
            )
