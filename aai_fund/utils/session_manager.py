# utils/session_manager.py
import streamlit as st

def start_session(user: dict):
    st.session_state["logged_in"] = True
    st.session_state["user_id"] = user.get("user_id")
    st.session_state["name"] = user.get("name")
    st.session_state["email"] = user.get("email")
    st.session_state["role"] = user.get("role")
    st.session_state["department"] = user.get("department")
    st.session_state["station_id"] = user.get("station_id")
    st.session_state["station_name"] = user.get("station_name")

def end_session():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
