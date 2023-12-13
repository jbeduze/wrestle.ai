import streamlit as st

st/set_page_config(
  page_title="Team Roster and cross analysis",
  page_icon=":snake:",
  layout="wide",
  initial_sidebar_state="expanaded",
)
#load local data file
@st.cache_data
df = pd.read_csv("wrestling_fake_data_Sheet1.csv")
  
#set up Pygwalker
def load_config(file_path):
  with open(file_path, 'r') as config_file:
    config_str = config_file.read()
  return config_str
config = load_config('config.json')
pyg.walk(df, env='streamlit', dark='dark', spec=config)
