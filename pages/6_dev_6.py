import streamlit as st
import cv2
import tempfile
from moviepy.editor import VideoFileClip
import numpy as np
import os

# Function to get a frame from the video at a specified time
def get_frame_at_time(video_path, time_in_seconds):
    """Extract a frame at a specific time from the video."""
    with VideoFileClip(video_path) as clip:
        # Ensure time is within the clip duration
        time_in_seconds = min(time_in_seconds, clip.duration - 1 / clip.fps)
        frame = clip.get_frame(time_in_seconds)
    return frame

# Function to extract a video segment
def extract_video_segment(video_path, start_time, end_time, output_path):
    """Extract a video segment and save it."""
    with VideoFileClip(video_path) as clip:
        # Adjust end time if it's beyond the clip's duration
        end_time = min(end_time, clip.duration)
        segment = clip.subclip(start_time, end_time)
        segment.write_videofile(output_path, codec="libx264", audio_codec="aac")

st.title('Video Segment Extractor')

# Upload video and display initial instructions
video_file_buffer = st.file_uploader("Upload a Video", type=["mp4", "mov", "avi", "mkv"])
if video_file_buffer is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tfile:
        tfile.write(video_file_buffer.read())
        video_path = tfile.name

    # Obtain video information
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
    cap.release()

    # Display the video
    st.video(video_path)

    # Slider for marking start and end points, adjusting for non-exact seconds
    start_time, end_time = st.slider("Mark the start and end points:", 
                                     0.0, 
                                     duration, 
                                     (0.0, duration), 
                                     step=1/fps, 
                                     format="%.2f s")

    # Displaying selected start and end frames
    col1, col2 = st.columns(2)
    with col1:
        st.write("Start Frame")
        start_frame_img = get_frame_at_time(video_path, start_time)
        st.image(start_frame_img, use_column_width=True)

    with col2:
        st.write("End Frame")
        end_frame_img = get_frame_at_time(video_path, end_time)
        st.image(end_frame_img, use_column_width=True)

    # Extracting segment and providing download button
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
