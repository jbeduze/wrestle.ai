import streamlit as st

st/set_page_config(
  page_title="Team Roster and cross analysis",
  page_icon=":snake:",
  layout="wide",
  initial_sidebar_state="expanaded",
)

@st.cache_data
df = pd.read_csv("wrestling_fake_data_Sheet1.csv")
  
