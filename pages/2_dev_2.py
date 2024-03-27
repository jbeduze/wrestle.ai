import streamlit as st
from moviepy.editor import VideoFileClip
import tempfile
import os

# Subheader for video upload
st.subheader('Upload an Existing Video File')
video_files = st.file_uploader("", type=['mp4', 'avi', 'mov', 'mkv'], accept_multiple_files=True)

if video_files:
    for video_file in video_files:
        # Save the uploaded video file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            tmp_file.write(video_file.getvalue())
            tmp_file_path = tmp_file.name

        # Display the uploaded video
        st.video(tmp_file_path)

        # Load the video to get duration and frame rate
        clip = VideoFileClip(tmp_file_path)
        total_frames = int(clip.fps * clip.duration)


#1st expander for the seconds to be displayed     
        with st.expander(f"Select Frame Range of the {total_frames} from the upload"):
# Define the range slider for selecting start and end times within the expander
            start_time, end_time = st.slider("Time Range (seconds)", 0.0, clip.duration, (0.0, clip.duration))

            if st.button("Extract Video Segment from original"):
                # Extract the segment
                segment_clip = clip.subclip(start_time, end_time)
                
                # Save the segment to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as segment_file:
                    segment_clip.write_videofile(segment_file.name, codec="libx264", audio_codec="aac")

                    # Display the segment
                    st.video(segment_file.name)

            else: st.warning("Please select a range to create a video segment")
#2nd expander for the frames to be displayed              
        with st.expander(f"Select Frame Range of the {total_frames} from the upload"):
# Define the range slider for selecting start and end Frames within the expander
            start_frame, end_frame = st.slider("Frame Range", 0, total_frames, (0, total_frames))
            if st.button("Extract Video Segment from original"):
                # Extract the segment
                segment_clip = clip.subclip(start_time, end_time)
                
                # Save the segment to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as segment_file:
                    segment_clip.write_videofile(segment_file.name, codec="libx264", audio_codec="aac")

                    # Display the segment
                    st.video(segment_file.name)

            else: st.warning("Please select a range to create a video segment")
