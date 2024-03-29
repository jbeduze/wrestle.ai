import streamlit as st
import cv2
import tempfile
import numpy as np

def get_frame(cap, frame_number):
    """Seek to the specified frame number and return the frame."""
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    if ret:
        # Convert BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    else:
        frame = np.zeros((100, 100, 3), dtype=np.uint8)  # Placeholder for an invalid frame
    return frame

st.title('Frame by Frame Video Viewer')

# Initialize or update the frame_number in session state
if 'frame_number' not in st.session_state:
    st.session_state.frame_number = 0

# Adjust frame_number when buttons are pressed
def increment_frame():
    st.session_state.frame_number = min(st.session_state.frame_number + 1, st.session_state.total_frames - 1)

def decrement_frame():
    st.session_state.frame_number = max(st.session_state.frame_number - 1, 0)

video_file_buffer = st.file_uploader("Upload a Video", type=["mp4", "mov", "avi", "mkv"])
if video_file_buffer is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file_buffer.read())
    video_path = tfile.name

    cap = cv2.VideoCapture(video_path)
    st.session_state.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Frame navigation
    st.slider('Select Frame', 0, st.session_state.total_frames - 1, key='frame_number')
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.button('Previous Frame', on_click=decrement_frame)
    with col3:
        st.button('Next Frame', on_click=increment_frame)

    # Display frames
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Previous Frame")
        if st.session_state.frame_number > 0:
            prev_frame = get_frame(cap, st.session_state.frame_number - 1)
            st.image(prev_frame)
        else:
            st.write("No previous frame")
    
    with col2:
        st.write("Current Frame")
        curr_frame = get_frame(cap, st.session_state.frame_number)
        st.image(curr_frame)
    
    with col3:
        st.write("Next Frame")
        if st.session_state.frame_number < st.session_state.total_frames - 1:
            next_frame = get_frame(cap, st.session_state.frame_number + 1)
            st.image(next_frame)
        else:
            st.write("No next frame")

    cap.release()
else:
    st.text("Please upload a video file to proceed")
