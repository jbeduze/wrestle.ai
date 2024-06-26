import streamlit as st
import cv2
import tempfile
from moviepy.editor import VideoFileClip
import numpy as np
import os
from streamlit_webrtc import webrtc_streamer
import av

#sidebar elements
with st.sidebar:
    ("---")

    if 'import_or_live' not in st.session_state:
        st.session_state.import_or_live = "import already existing video"
    
    st.session_state.import_or_live = st.radio(
    "Select if you are importing an existing video or if you'd like to reocrd live video",
    ["Import already existing video", "Record Live Video"],
    index=0,
)

st.write(f"You selected:{st.session_state.import_or_live}")


st.title('Video Segment Extractor')
st.write("this app allows you to either select an already recorded video or take a live video for displaying and review, selecting frames and a total segment, to then finally export for analysis")

# Function to safely get a frame at a specific time
def get_frame_at_time(video_path, time_in_seconds, duration):
    with VideoFileClip(video_path) as clip:
        # Clamp time to ensure it's within the video duration
        safe_time = max(0, min(time_in_seconds, duration - 0.04))  # Subtracting a small buffer to avoid going over
        frame = clip.get_frame(safe_time)
    return frame

# Function to extract and save a video segment
def extract_video_segment(video_path, start_time, end_time, output_path):
    with VideoFileClip(video_path) as clip:
        segment = clip.subclip(start_time, end_time)
        segment.write_videofile(output_path, codec="libx264", audio_codec="aac")
# if st.session_state.import_or_live(0):
webrtc_streamer(key="live")
# if st.session_state.import_or_live(1):
#     st.write("LMFAO")

video_file_buffer = st.file_uploader("Upload a Video", type=["mp4", "mov", "avi", "mkv"])
if video_file_buffer is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(video_file_buffer.read())
    video_path = tfile.name
    
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps
    cap.release()

    st.video(video_path)

    start_time, end_time = st.slider("Mark the start and end points:", 0.0, duration, (0.0, duration), step=1/fps, format="%.2f s")

    if video_file_buffer is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.write("Start Frame")
            start_frame_img = get_frame_at_time(video_path, start_time, duration)
            st.image(start_frame_img, use_column_width=True)

        with col2:
            st.write("End Frame")
            end_frame_img = get_frame_at_time(video_path, end_time, duration)
            st.image(end_frame_img, use_column_width=True)

    if st.button("Extract Segment"):
        output_path = tempfile.mktemp(suffix=".mp4")
        extract_video_segment(video_path, start_time, end_time, output_path)
        
        with open(output_path, "rb") as file:
            st.download_button(
                    label="Download Video Segment",
                    data=file,
                    file_name="extracted_segment.mp4",
                    mime="video/mp4"
                )
        os.remove(output_path)  # Clean up the temporary file
