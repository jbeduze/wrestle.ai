import streamlit as st
import cv2
import tempfile
import numpy as np

def get_frame(cap, time_in_seconds, fps):
    """Seek to the specified time in seconds and return the frame and frame number."""
    frame_number = int(time_in_seconds * fps)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    else:
        frame = np.zeros((100, 100, 3), dtype=np.uint8)  # Placeholder for an invalid frame
    return frame, frame_number

st.title('Frame by Frame Video Viewer with Time Slider')

video_file_buffer = st.file_uploader("Upload a Video", type=["mp4", "mov", "avi", "mkv"])
if video_file_buffer is not None:
    # Create a temporary file to read the video with OpenCV
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
        tmp_file.write(video_file_buffer.read())
        video_path = tmp_file.name
    
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps

    if 'selected_time' not in st.session_state:
        st.session_state.selected_time = 0.0

    # Adjust the current time by one frame
    def adjust_time(delta):
        st.session_state.selected_time = min(max(0, st.session_state.selected_time + delta), duration)

    # Play the video
    st.video(video_path)

    # Frame navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.button('Previous Frame', on_click=adjust_time, args=(-1/fps,))
    with col3:
        st.button('Next Frame', on_click=adjust_time, args=(1/fps,))

    # Time slider
    selected_time = st.slider('Select Time (seconds)', 0.0, duration, st.session_state.selected_time, 0.01, key='selected_time_slider')

    # Update the selected time based on the slider's value
    st.session_state.selected_time = selected_time

    # Display the current, next, and previous frames based on selected time
    current_frame, frame_number = get_frame(cap, selected_time, fps)
    col1, col2, col3 = st.columns(3)

    with col1:  # Previous frame
        if frame_number > 0:
            prev_frame, _ = get_frame(cap, max(selected_time - 1/fps, 0), fps)
            st.image(prev_frame)
            st.caption(f"Time: {max(selected_time - 1/fps, 0):.2f}s (Frame {frame_number - 1})")
        else:
            st.write("No previous frame")

    with col2:  # Current frame
        st.image(current_frame)
        st.caption(f"Time: {selected_time:.2f}s (Frame {frame_number})")

    with col3:  # Next frame
        if frame_number < total_frames - 1:
            next_frame, _ = get_frame(cap, min(selected_time + 1/fps, duration), fps)
            st.image(next_frame)
            st.caption(f"Time: {min(selected_time + 1/fps, duration):.2f}s (Frame {frame_number + 1})")
        else:
            st.write("No next frame")

    cap.release()
else:
    st.text("Please upload a video file to proceed")
