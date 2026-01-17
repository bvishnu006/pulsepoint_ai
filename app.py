import streamlit as st
import os
from google import genai
from moviepy.video.io.VideoFileClip import VideoFileClip
from dotenv import load_dotenv
import tempfile
import time
from google import genai
from google.genai import types
import re

# 1. Configuration & Setup
load_dotenv()
#client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"),http_options=types.HttpOptions(api_version='v1'))
#client = genai.Client(
#    api_key=os.getenv("GEMINI_API_KEY"),
#    http_options=types.HttpOptions(api_version='v1') # Force stable v1
#)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_ID = "gemini-3-flash-preview"

st.set_page_config(page_title="PulsePoint AI", layout="centered")
st.title("PulsePoint AI 🎙️✨")
st.info("Upload a long video, and I'll find the viral nuggets for you.")

# 2. File Upload Logic
uploaded_file = st.file_uploader("Upload your video (MP4)", type=['mp4'])

if uploaded_file is not None:
    # Save the file to a temporary location so MoviePy can read it
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
        tmp.write(uploaded_file.read())
        video_path = tmp.name

    st.video(video_path) # Preview the uploaded video

    # --- UPDATED PROMPT AND LOGIC ---

    if st.button("🚀 Generate 4 Viral Reels (9:16)"):
        with st.spinner("Gemini 3 is selecting your top moments..."):
            try:
                # 1. Upload & Wait (Same as before)
                video_upload = client.files.upload(file=video_path)
                while video_upload.state.name == "PROCESSING":
                    time.sleep(2)
                    video_upload = client.files.get(name=video_upload.name)

                # 2. Strict Prompt for 4 Reels of 60s
                # We explicitly ask for 60-second windows
                prompt = (
                    "Identify a maximum of 4 high-energy, viral moments from this video. "
                    "Each moment should be exact 60 seconds. "
                    "Return ONLY the timestamps in this format: MM:SS-MM:SS. "
                    "Example: 00:05-01:05"
                )

                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=[video_upload, prompt],
                    config=types.GenerateContentConfig(
                        thinking_config=types.ThinkingConfig(thinking_level="MEDIUM")
                    )
                )

                # 3. Safe Parsing with 'Max 4' Cap
                timestamp_pattern = r'\d{2}:\d{2}-\d{2}:\d{2}'
                all_found = re.findall(timestamp_pattern, response.text)
                
                # This is the "Safety Cap" - take only the first 4
                timestamps = all_found[:4] 

                if not timestamps:
                    st.error("Could not find viral moments. Try a longer video!")
                else:
                    for i, ts in enumerate(timestamps):
                        st.write(f"🎬 Processing Reel {i+1}/4...")
                        start_str, end_str = ts.split('-')
                        
                        with VideoFileClip(video_path) as video:
                            # Convert to seconds
                            m1, s1 = map(int, start_str.split(':'))
                            m2, s2 = map(int, end_str.split(':'))
                            start_sec, end_sec = m1*60+s1, m2*60+s2

                            # Cut the 60s clip
                            clip = video.subclipped(start_sec, end_sec)

                            # Apply 9:16 Center Crop
                            w, h = clip.size
                            target_w = int(h * (9/16))
                            x1 = (w / 2) - (target_w / 2)
                            x2 = (w / 2) + (target_w / 2)
                            
                            final_reel = clip.cropped(x1=x1, y1=0, x2=x2, y2=h)

                            # Write with high-quality settings
                            out_name = f"reel_{i+1}.mp4"
                            final_reel.write_videofile(out_name, codec="libx264", audio_codec="aac", threads=4)

                            st.video(out_name)
                            with open(out_name, "rb") as f:
                                st.download_button(f"📥 Download Reel {i+1}", f, out_name)

            except Exception as e:
                st.error(f"Error: {e}")