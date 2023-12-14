import streamlit as st
import plotly
import pandas as pd
import pygwalker as pyg


st.write('Welcome to your sports dashboard')
#uploaded_file = st.file_uploader("choose a file or drag and drop")
  #if uploaded_file is not None:
df = pd.read_csv("wrestling_fake_data_Sheet1.csv") #(uploaded_file)


video_files = st.file_uploader("Upload a video file", type=['.mp4', '.avi', '.mov', '.mkv'], accept_multiple_files=True)
for video_file in video_files:
  video_bytes = video_file.read()
  st.video(video_bytes)
"---"
uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write(bytes_data)
