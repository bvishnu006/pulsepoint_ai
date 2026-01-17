# pulsepoint_ai

vedio link: https://drive.google.com/drive/folders/1mF9xqFVzkcfy1729v80HgRCCCFnHqw0N?usp=sharing

PulsePoint AI is an end-to-end automated system that converts long-form landscape videos into viral-ready vertical (9:16) short reels using Generative AI and programmatic video editing.

# Project Overview
The system analyzes visual frames and audio signals to detect high-energy, high-engagement moments and transforms them into social-media-optimized clips for platforms such as Instagram Reels, YouTube Shorts, and TikTok — with zero manual editing.

# System Architecture
User Upload (MP4)
        │
        ▼
Streamlit Web Interface
        │
        ▼
Gemini File API (Cloud Upload)
        │
        ▼
Gemini 3 Flash (Video + Audio Analysis)
        │
        ▼
Timestamp Extraction (Regex Parser)
        │
        ▼
MoviePy Video Processing
        │
        ▼
Center Crop (9:16)
        │
        ▼
Vertical MP4 Reels
        │
        ▼
User Download
