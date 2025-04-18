import streamlit as st
from core.db_utils import init_db
from sidebar import load_sidebar

st.set_page_config(
    page_title="TrainMeAI",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None,
)

init_db()
load_sidebar()

st.title("Welcome to TrainMeAI 💪")
st.markdown("Use the navigation on the left to get started.")
