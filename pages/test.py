import streamlit as st
import cv2
import tempfile
import base64
import os
from openai import OpenAI

# Initialize the OpenAI client (configure with your API key)
client = OpenAI(api_key=st.secrets.openai_api_key)

st.write('Welcome to your Athlete Analysis dashboard')

def encode_image(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    base64_image = base64.b64encode(buffer).decode('utf-8')
    encoded_image_url = f"data:image/jpeg;base64,{base64_image}"
    return encoded_image_url

def analyze_frame_with_openai_vision(encoded_frame):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe what is occuring. Identify any scoring opportunity."},
                    {"type": "image_url", "image_url": {"url": encoded_frame}},
                ],
            }
        ],
        max_tokens=300,
    )
    return response.choices[0].message['content']

video_files = st.file_uploader("Upload a video file", type=['.mp4', '.avi', '.mov', '.mkv'], accept_multiple_files=True)

for video_file in video_files:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
        tmp_file.write(video_file.read())
        tmp_file_path = tmp_file.name

    st.video(tmp_file_path)

    video = cv2.VideoCapture(tmp_file_path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    analysis_results = []

    for frame_idx in range(0, total_frames, 50):  # Process every 50th frame
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        success, frame = video.read()
        if success:
            encoded_frame = encode_image(frame)
            result = analyze_frame_with_openai_vision(encoded_frame)
            analysis_results.append((frame_idx, result))
    
    video.release()

    # Display analysis results
    for frame_idx, result in analysis_results:
        st.write(f"Frame {frame_idx}: {result}")
