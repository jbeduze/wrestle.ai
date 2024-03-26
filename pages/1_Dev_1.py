import streamlit as st
import plotly
import pandas as pd
import pygwalker as pyg
import tempfile
from IPython.display import display, Image, Audio
import cv2
import base64
import time
#from openai import OpenAI
import os
import requests
#activate webcam
from streamlit_webrtc import webrtc_streamer, RTCConfiguration
import av
import urllib.request
from streamlit_webrtc import webrtc_streamer, RTCConfiguration, VideoProcessorBase
import threading

haar_url = "https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml?raw=true"
haar_file = "haarcascade_frontalface_default.xml"
urllib.request.urlretrieve(haar_url, haar_file)

# ... [rest of your imports]

st.write('Welcome to your Athlete Analysis dashboard')
st.write("If you choose to upload files into this software or take live videos, all is possible!")
st.subheader('Upload an Existing Video File')
video_files = st.file_uploader("",type=['.mp4', '.avi', '.mov', '.mkv'], accept_multiple_files=True)

if video_files:
    for video_file in video_files:
        # Save the uploaded video file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            tmp_file.write(video_file.read())
            tmp_file_path = tmp_file.name

    st.video(tmp_file_path)

    # Load the video using OpenCV
    video = cv2.VideoCapture(tmp_file_path)

    # Get the total number of frames and calculate duration
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps
    st.write(f"Total frames in the uploaded video: {total_frames}")
    with st.expander(f"Select Frame Range of the {total_frames} from the upload"):
            # Define the range slider for selecting start and end frames within the expander
        
        start_frame, end_frame = st.slider("Frame Range", 0, total_frames, (0, total_frames))
        # Make sure to release the video capture object
        if st.button('Extract Video Segment'):
        start_frame = int(start_time * fps)
        end_frame = int(end_time * fps)
        with segment_file.NamedTemporaryFile(delete=False, suffix='.mp4') as segment_file:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter('segment_file.name', fourcc, fps, (int(video.get(3)), int(video.get(4))))
    
            video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
            for _ in range(start_frame, end_frame):
                ret, frame = video.read()
                if ret and video.get(cv2.CAP_PROP_POS_FRAMES) <= end_frame:
                    out.write(frame)
                else:
                    break
        video.release()
else:
    st.warning("Please upload a video")
    # Display the video
    

# Define the slider with the total number of frames as the max value and the range within that you want to grab
# Define the range slider for selecting start and end times
with st.expander(f"Select Time Range"):
    start_time, end_time = st.slider("Select Time Range (seconds)", 0.0, duration, (0.0, duration), 0.1)


    if st.button('Extract Video Segment'):
        start_frame = int(start_time * fps)
        end_frame = int(end_time * fps)
        with segment_file.NamedTemporaryFile(delete=False, suffix='.mp4') as segment_file:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter('segment_file.name', fourcc, fps, (int(video.get(3)), int(video.get(4))))
    
            video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
            for _ in range(start_frame, end_frame):
                ret, frame = video.read()
                if ret and video.get(cv2.CAP_PROP_POS_FRAMES) <= end_frame:
                    out.write(frame)
                else:
                    break
    
        out.release()
        st.video('output.mp4')

video.release()
'---'
st.subheader('Live Video Analysis')


class VideoProcessor(VideoProcessorBase):
    def __init__(self) -> None:
        self.is_recording = False
        self.video_frames = []
        self.recording_lock = threading.Lock()

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        frm = frame.to_ndarray(format="bgr24")
        faces = cascade.detectMultiScale(cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY), 1.1, 3)

        for x, y, w, h in faces:
            cv2.rectangle(frm, (x, y), (x + w, y + h), (0, 255, 0), 3)

        if self.is_recording:
            with self.recording_lock:
                self.video_frames.append(frm)

        return av.VideoFrame.from_ndarray(frm, format='bgr24')

    def start_recording(self):
        with self.recording_lock:
            self.is_recording = True
            self.video_frames.clear()

    def stop_recording(self, filename):
        with self.recording_lock:
            self.is_recording = False
            if self.video_frames:
                self.save_video(filename)

    def save_video(self, filename):
        if not self.video_frames:
            return
        first_frame = self.video_frames[0]
        height, width, _ = first_frame.shape
        codec = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(filename, codec, 20.0, (width, height))

        for frame in self.video_frames:
            out.write(frame)
        out.release()

cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

ctx = webrtc_streamer(key="key", video_processor_factory=VideoProcessor,
                      rtc_configuration=RTCConfiguration(
                          {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
                      ))

if ctx.video_processor:
    if st.button("Start Recording"):
        ctx.video_processor.start_recording()
        st.write("Recording started.")

    if st.button("Stop Recording"):
        video_filename = "output.mp4"
        ctx.video_processor.stop_recording("output.mp4")
        st.write("Recording stopped. Video saved as output.mp4.")
        st.video(video_filename)
