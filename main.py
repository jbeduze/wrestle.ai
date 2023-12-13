import streamlit as st
import plotly
import pandas as pd
import pygwalker as pyg


st.write('Welcome to your sports dashboard')
uploaded_file = st.file_uploader("choose a file or drag and drop")
  if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)
    pyg.walk(df, dark='light')
