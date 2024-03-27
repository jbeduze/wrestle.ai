import streamlit as st
import cv2
import tempfile

st.title('Frame by Frame Video Viewer')

video_file_buffer = st.file_uploader("Upload a Video", type=["mp4", "mov", "avi", "mkv"])
if video_file_buffer is not None:
    # To read video file buffer with OpenCV, we save it to a temporary file
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file_buffer.read())
    video_path = tfile.name

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps

    st.write(f"Total frames: {total_frames}, FPS: {fps}, Duration: {duration:.2f} seconds")

    # Slider for selecting frame
    frame_number = st.slider('Select Frame', 0, total_frames - 1, 0)

    # Navigate frame by frame
    if st.button('Previous Frame'):
        frame_number = max(0, frame_number - 1)
    if st.button('Next Frame'):
        frame_number = min(total_frames - 1, frame_number + 1)

    # Set the current frame position of the video file
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()

    if ret:
        # Convert the frame to RGB (OpenCV uses BGR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame)
    else:
        st.error("Error reading frame")

    cap.release()
else:
    st.text("Please upload a video file to proceed")
