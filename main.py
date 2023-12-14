import streamlit as st
import plotly
import pandas as pd
import pygwalker as pyg

from IPython.display import display, Image, Audio
import cv2
import base64
import time
from openai import OpenAI
import os
import requests

client = OpenAI()

st.write('Welcome to your sports dashboard')
#uploaded_file = st.file_uploader("choose a file or drag and drop")
  #if uploaded_file is not None:
#df = pd.read_csv("wrestling_fake_data_Sheet1.csv") #(uploaded_file)


video_files = st.file_uploader("Upload a video file", type=['.mp4', '.avi', '.mov', '.mkv'], accept_multiple_files=True)
for video_file in video_files:
  video_bytes = video_file.read()
  st.video(video_bytes)

st.write("Read video uploaded, establish keyframes, produce dynamic slider to be able to reference key frames, provide discription of what's happening in video")
"---"
# uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
# for uploaded_file in uploaded_files:
#     bytes_data = uploaded_file.read()
#     st.write(bytes_data)
"---"
# video = cv2.VideoCapture(video_files)

# base64Frames = []
# while video.isOpened():
#     success, frame = video.read()
#     if not success:
#         break
#     _, buffer = cv2.imencode(".jpg", frame)
#     base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

# video.release()
# print(len(base64Frames), "frames read.")
