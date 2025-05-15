import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
from datetime import datetime
from agent.planner import generate_daily_plan
from agent.reflection import reflect_on_day
from agent.memory import create_memory_store, persist_memory
from config.settings import APP_MODE

# Initialize memory
memory = create_memory_store()

st.set_page_config(page_title="🧠 ChainPlanner", layout="centered")

st.title("🧠 ChainPlanner: Reflective Daily Task Planner")
st.write("An adaptive planner that evolves with your mood, feedback, and experience.")

today = datetime.today().strftime("%Y-%m-%d")

# --- Input: Mood and Feedback ---
st.subheader("🔄 Start Your Day")

with st.form("daily_input"):
    mood = st.selectbox("How are you feeling today?", ["Happy", "Focused", "Tired", "Stressed", "Neutral"])
    feedback = st.text_area("Anything you'd like to tell your planner?", placeholder="I didn’t sleep well... etc.")
    submitted = st.form_submit_button("Generate My Plan")

# --- Generate Plan ---
if submitted:
    with st.spinner("Thinking..."):
        plan = generate_daily_plan(date=today, feedback=feedback, mood=mood)
    st.success("✅ Here's your plan for today:")
    st.text_area("🗓️ Plan", plan, height=250)

    # Store plan in session state
    st.session_state["plan"] = plan

# --- End of Day Reflection ---
st.divider()
st.subheader("🌙 End of Day Reflection")

with st.form("reflection_input"):
    completed = st.text_area("What did you actually complete today?", placeholder="Finished 2/3 tasks...")
    reflect = st.form_submit_button("Reflect and Improve")

if reflect:
    if "plan" not in st.session_state:
        st.warning("⚠️ Please generate a plan before reflecting.")
    else:
        with st.spinner("Reflecting..."):
            summary = reflect_on_day(
                memory,
                date=today,
                feedback=feedback,
                mood=mood,
                plan=st.session_state["plan"],
                completed=completed
            )
            persist_memory(memory)
        st.success("🧠 Reflection complete:")
        st.text_area("📘 Reflection Summary", summary, height=250)
