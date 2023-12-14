import streamlit as st
import plotly
import pandas as pd
import pygwalker as pyg


st.write('Welcome to your sports dashboard')
#uploaded_file = st.file_uploader("choose a file or drag and drop")
  #if uploaded_file is not None:
df = pd.read_csv("wrestling_fake_data_Sheet1.csv") #(uploaded_file)


video_file = st.video('Upload Video Here',
                     type=['.mp4', '.avi', '.mov', '.mkv'])
video_bytes = video_file.read()

st.video(video_bytes)
