#required libraries
#streamlit, python, streamlit-extras, PyPFD, faiss, langchain
#tutorial: https://www.youtube.com/watch?v=RIWbalZ7sTo&t=475s

import streamlit as st


st.header("Credit application processing")
st.markdown('''
this will do the following:
-End goal is to import doc.s and pull the important info and display it in an easier fashion
-this will drop the necsary info into an internal doc
''')
add_vertical_space(5)
("---")
st.write('langchain will be the main engine of this processing')
