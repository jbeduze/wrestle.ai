import streamlit as st
import plotly
import pandas as pd
import pygwalker as pyg

from IPython.display import display, Image, Audio
import cv2
import base64
import time
#from openai import OpenAI
import os
import requests

st.write('Welcome to your sports dashboard')

video_files = st.file_uploader("Upload a video file", type=['.mp4', '.avi', '.mov', '.mkv'], accept_multiple_files=True)
for video_file in video_files:
  video_bytes = video_file.read()
  st.video(video_bytes)

st.write("Read video uploaded, establish keyframes, provide description of what's happening in video")
"---"
# uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
# for uploaded_file in uploaded_files:
#     bytes_data = uploaded_file.read()
#     st.write(bytes_data)
# "---"
#client = OpenAI()
      #extract the Frames from uploaded video
      # Load the video
video = cv2.VideoCapture(video_files)

# Get the total number of frames
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# Define the slider with the total number of frames as the max value
frame_number = st.slider('Select a frame', 0, total_frames - 1)

# Processing the video
base64Frames = []
frame_idx = 0
while video.isOpened():
    success, frame = video.read()
    if not success:
        break
    _, buffer = cv2.imencode(".jpg", frame)
    base64Frames.append(base64.b64encode(buffer).decode("utf-8"))
    frame_idx += 1
    if frame_idx > frame_number:
        break

video.release()
print(len(base64Frames), "frames read.")

# base64Frames = []
# while video.isOpened():
#     success, frame = video.read()
#     if not success:
#         break
#     _, buffer = cv2.imencode(".jpg", frame)
#     base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

# video.release()
# print(len(base64Frames), "frames read.")

# #Display the frames
# display_handle = display(None, display_id=True)
# for img in base64Frames:
#     display_handle.update(Image(data=base64.b64decode(img.encode("utf-8"))))
#     time.sleep(0.025)

# keyFrames_Select = st.slider(
#   label = "find the KeyFrames you'd like to make note of",
#   max_value = 
