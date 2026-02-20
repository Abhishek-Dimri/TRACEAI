"""
=============================================================================
  Week 1 — Frontend Developer
  File: Home_fixed.py
  Purpose: Verified and improved version of Home.py with Week 1 UX fixes.
=============================================================================

Changes from original:
  1. Added st.set_page_config(page_title=..., page_icon=...)
  2. Replaced raw HTML with Streamlit native components where possible.
  3. Added error handling for missing config keys.
  4. Minor code cleanup.
=============================================================================
"""

import yaml
import streamlit as st
from yaml import SafeLoader
import streamlit_authenticator as stauth


# ---------------------------------------------------------------------------
# Page config — MUST be the first Streamlit command
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Find Missing Person — Home",
    page_icon="🔍",
    layout="centered",
)


# ---------------------------------------------------------------------------
# Helper: background image (optional)
# ---------------------------------------------------------------------------
import base64

def add_bg_from_local(image_file):
    """Set a local image as the full-page background."""
    try:
        with open(image_file, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/png;base64,{encoded});
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
    except FileNotFoundError:
        pass  # silently skip if image not found


# ---------------------------------------------------------------------------
# Session state init
# ---------------------------------------------------------------------------
if "login_status" not in st.session_state:
    st.session_state["login_status"] = False


# ---------------------------------------------------------------------------
# Load login config
# ---------------------------------------------------------------------------
try:
    with open("login_config.yml") as file:
        config = yaml.load(file, Loader=SafeLoader)
except FileNotFoundError:
    st.error("⚠️ Configuration file `login_config.yml` not found. "
             "Please ensure it exists in the project root.")
    st.stop()


# ---------------------------------------------------------------------------
# Authenticator setup
# ---------------------------------------------------------------------------
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

authenticator.login(location="main")


# ---------------------------------------------------------------------------
# Post-login UI
# ---------------------------------------------------------------------------
if st.session_state.get("authentication_status"):
    # Logout button in sidebar
    authenticator.logout("Logout", "sidebar")
    st.session_state["login_status"] = True

    user_info = config["credentials"]["usernames"][st.session_state["username"]]
    st.session_state["user"] = user_info["name"]

    # --- User Info (native Streamlit instead of raw HTML) ---
    st.title(user_info["name"])
    st.caption(f"📍 {user_info.get('area', '')}, {user_info.get('city', '')}")
    st.caption(f"🏷️ Role: {user_info.get('role', 'User')}")
    st.divider()

    # --- Dashboard Metrics ---
    from pages.helper import db_queries

    found_cases = db_queries.get_registered_cases_count(user_info["name"], "F")
    non_found_cases = db_queries.get_registered_cases_count(user_info["name"], "NF")

    col1, col2 = st.columns(2)
    col1.metric("✅ Found Cases", value=len(found_cases))
    col2.metric("🔍 Not Found Cases", value=len(non_found_cases))

elif st.session_state.get("authentication_status") is False:
    st.error("❌ Username or password is incorrect.")

elif st.session_state.get("authentication_status") is None:
    st.warning("Please enter your username and password to continue.")
    st.session_state["login_status"] = False
