import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
from core.langgraph_runner import build_story_graph

st.set_page_config(page_title="ContextWeaver Storyteller", page_icon="📖")

st.title("🌟 ContextWeaver: Dynamic Storytelling")

if "story_state" not in st.session_state:
    st.session_state.story_state = {
        "user_input": "",
        "plot_context": "",
        "world_context": "",
        "character_output": ""
    }

graph = build_story_graph()

user_input = st.text_input("Your prompt:", "")

if st.button("Continue Story") and user_input.strip():
    st.session_state.story_state["user_input"] = user_input
    result = graph.invoke(st.session_state.story_state)

    # Update session state with new context
    st.session_state.story_state.update(result)

    # Display character response (story output)
    st.markdown(f"### Story Output:\n\n{result['character_output']}")

    # Optionally display plot and world context for debugging
    with st.expander("Plot Context"):
        st.write(result["plot_context"])

    with st.expander("World Context"):
        st.write(result["world_context"])
