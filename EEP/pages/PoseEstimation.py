import streamlit as st
import os
import base64
import sys
from PIL import Image
import cv2
import requests
import numpy as np
from io import BytesIO
import time
from sidebar import load_sidebar
from core.config import IEP1_URL

st.set_page_config(page_title="Pose Estimation | TrainMeAI", layout="centered")

load_sidebar()
# ------------------- Helpers -------------------

def lucide_icon(icon_name, size=20):
    icon_path = f"static/icons/{icon_name}.svg"
    try:
        with open(icon_path, "rb") as f:
            svg_bytes = f.read()
            encoded = base64.b64encode(svg_bytes).decode("utf-8")
            return f'<img src="data:image/svg+xml;base64,{encoded}" width="{size}" style="margin-bottom:-4px; margin-right:6px;" />'
    except FileNotFoundError:
        return ""

def alert_box(icon_svg, message, color="#FDECEA", border="#e74c3c"):
    st.markdown(
        f"""
    <div style="padding: 1em; background-color: {color}; border-left: 5px solid {border}; border-radius: 5px;">
        {icon_svg} <b>{message}</b>
    </div>
    """,
        unsafe_allow_html=True,
    )


def success_box(icon_svg, message):
    st.markdown(
        f"""
    <div style="padding: 1em; background-color: #E6F4EA; border-left: 5px solid #27ae60; border-radius: 5px;">
        {icon_svg} <b>{message}</b>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ------------------- App State -------------------

st.session_state.setdefault("selected_exercise", "Squat")
st.session_state.setdefault("analysis_mode", None)
st.session_state.setdefault("fitness_level", "beginner")

EXERCISES = {
    "Squat": "static/gifs/squat.gif",
    "Bicep Curl": "static/gifs/bicep_curl.gif",
    "Lateral Raise": "static/gifs/overhead_press.gif",
    "Shoulder Press": "static/gifs/resistance_band_chest_press.gif",
    "Jumping Jack": "static/gifs/jump_squat.gif",
    "Tricep Extension": "static/gifs/tricep_extension.webp",
}

# ------------------- UI Sections -------------------

def show_exercise_selection():
    st.markdown(
        f"""
    <h2 style='color:#1664AD; font-weight:700; margin-bottom:1rem;'>
        {lucide_icon('dumbbell')} Select an Exercise to Evaluate
    </h2>
    """,
        unsafe_allow_html=True,
    )
    cols = st.columns(3)
    for idx, (name, gif_path) in enumerate(EXERCISES.items()):
        with cols[idx % 3]:
            img = Image.open(gif_path)
            img.seek(0)
            buf = BytesIO()
            img.save(buf, format="PNG")
            b64_img = base64.b64encode(buf.getvalue()).decode()
            is_selected = st.session_state["selected_exercise"] == name
            border = "3px solid #1664AD" if is_selected else "1px solid #ddd"
            bg_color = "#F4F6F8" if is_selected else "#fff"
            filter_style = (
                "grayscale(0%)" if is_selected else "grayscale(100%) brightness(90%)"
            )

            st.markdown(
                f"""
            <div style="position: relative; border: {border}; border-radius: 12px; background-color: {bg_color};
                         overflow: hidden; margin-bottom: 10px; transition: 0.3s;">
                <img src="data:image/png;base64,{b64_img}" 
                    style="width:100%; display:block; filter: {filter_style};" />
            </div>
            """,
                unsafe_allow_html=True,
            )

            if st.button(name, key=f"btn_{name}"):
                st.session_state["selected_exercise"] = name

def show_mode_selector():
    st.markdown("---")
    st.markdown(
        f"""
    <h2 style='color:#1664AD; font-weight:700; margin-bottom:1rem;'>
        {lucide_icon('cpu')} How do you want to analyze your form?
    </h2>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    def mode_card(icon_name, title, desc, button_label, mode_key):
        st.markdown(
            f"""
        <div style='
            padding: 1.2em;
            border: 1px solid #D6E4F0;
            border-radius: 10px;
            background-color: #F4F6F8;
            box-shadow: 1px 1px 6px rgba(0,0,0,0.04);
            margin-bottom: 1em;
        '>
            <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 8px;'>
                {lucide_icon(icon_name, size=22)} <h4 style='margin: 0; color: #1664AD;'>{title}</h4>
            </div>
            <p style='margin-top: 0; font-size: 1rem; color: #333;'>{desc}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button(button_label, use_container_width=True):
            st.session_state.analysis_mode = mode_key

    with col1:
        mode_card(
            icon_name="upload",
            title="Upload a Video",
            desc="Record your workout and upload it to get AI feedback and rep count.",
            button_label="Analyze Uploaded Video",
            mode_key="upload",
        )

    with col2:
        mode_card(
            icon_name="video",
            title="Live Camera Analysis",
            desc="Use your webcam for real-time form correction and rep tracking.",
            button_label="Start Live Analysis",
            mode_key="live",
        )


def show_fitness_level_selector():
    st.selectbox(
        "Select your fitness level",
        options=["beginner", "pro"],
        index=0 if st.session_state["fitness_level"] == "beginner" else 1,
        key="fitness_level",
    )

# ------------------- Analysis Handlers -------------------

def handle_video_upload():
    st.markdown(
        f"### {lucide_icon('square-play')} Upload Your Exercise Video",
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader(
        "Upload a video (MP4, MOV, AVI)", type=["mp4", "mov", "avi"]
    )
    if uploaded_file:
        st.video(uploaded_file)
        st.markdown(
            f"{lucide_icon('rocket')} <b>Ready to let the AI judge your form?</b>",
            unsafe_allow_html=True,
        )
        if st.button("Analyze Video Now"):
            with st.spinner("Analyzing... because AI judge too 🤖🧐"):
                TEMP_FOLDER = "temp_videos"
                os.makedirs(TEMP_FOLDER, exist_ok=True)

                timestamp = time.strftime("%Y%m%d_%H%M%S")
                safe_exercise = (
                    st.session_state["selected_exercise"].lower().replace(" ", "_")
                )
                output_path = os.path.join(
                    TEMP_FOLDER, f"{safe_exercise}_{timestamp}.mp4"
                )

                files = {
                    "video": (uploaded_file.name, uploaded_file, uploaded_file.type)
                }
                data = {
                    "exercise": safe_exercise,
                    "level": st.session_state["fitness_level"],
                }

                try:
                    response = requests.post(
                        f"{IEP1_URL}/analyze-video", files=files, data=data
                    )
                    if response.status_code == 200:
                        with open(output_path, "wb") as f:
                            f.write(response.content)
                        success_box(
                            lucide_icon("check-circle"),
                            "Results ready. Minimal judgment... maximum gains 💪😄",
                        )
                        st.video(output_path)
                    else:
                        alert_box(
                            lucide_icon("circle-stop"),
                            f"Error: {response.status_code} - {response.text}",
                        )
                except Exception as e:
                    alert_box(lucide_icon("circle-stop"), f"Connection error: {e}")


def handle_live_camera():
    st.markdown(
        f"### {lucide_icon('video')} Real-time Feedback with Camera",
        unsafe_allow_html=True,
    )
    stframe = st.empty()
    stop_signal = st.empty()

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW if os.name == "nt" else 0)
    with stop_signal.container():
        stop_col1, stop_col2 = st.columns([0.1, 0.9])
        with stop_col1:
            st.markdown(lucide_icon("circle-stop", size=20), unsafe_allow_html=True)
        with stop_col2:
            stop_btn = st.button("Stop Analysis", use_container_width=True)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            alert_box(lucide_icon("circle-stop"), "Webcam not accessible.")
            break

        resized = cv2.resize(frame, (640, 480))
        success, encoded = cv2.imencode(".jpg", resized)
        if not success:
            alert_box(lucide_icon("circle-stop"), "Failed to encode frame.")
            break

        img_base64 = base64.b64encode(encoded).decode("utf-8")
        payload = {
            "session_id": "live-session",
            "image": img_base64,
            "exercise": st.session_state["selected_exercise"].lower().replace(" ", "_"),
            "level": st.session_state["fitness_level"],
        }

        try:
            response = requests.post(
                f"{IEP1_URL}/analyze-frame", json=payload, timeout=5
            )
            if response.status_code == 200:
                res = response.json()
                frame_data = base64.b64decode(res["frame"])
                nparr = np.frombuffer(frame_data, np.uint8)
                processed = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                stframe.image(processed, channels="BGR")
            else:
                alert_box(
                    lucide_icon("triangle-alert"),
                    f"Response {response.status_code}: {response.text}",
                )
        except Exception as e:
            alert_box(lucide_icon("triangle-alert"), f"API Error: {e}")
            break

        if stop_btn:
            break

    cap.release()
    stop_signal.empty()

# ------------------- Main UI -------------------

show_exercise_selection()
show_fitness_level_selector()
show_mode_selector()

if st.session_state.analysis_mode == "upload":
    handle_video_upload()
elif st.session_state.analysis_mode == "live":
    handle_live_camera()
