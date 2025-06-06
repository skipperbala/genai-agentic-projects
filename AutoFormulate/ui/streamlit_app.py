import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
import json
import glob
import openai
from evaluation.feedback_loop import evaluate_hypotheses
from agents.hypothesis_agent import generate_hypothesis, fetch_graph_context


st.set_page_config(page_title="AutoFormulate: Hypothesis Generator", layout="wide")

st.title("🧬 AutoFormulate: AI-Powered Hypothesis Discovery")

tab1, tab2, tab3 = st.tabs(["📄 Parsed Papers", "🔗 Knowledge Graph", "💡 Hypotheses"])


with tab1:
    st.header("📄 Parsed Papers")
    files = glob.glob("data/parsed_papers/*_extracted.json")

    for file in files:
        with open(file) as f:
            paper = json.load(f)
        with st.expander(paper.get("title", "Untitled")):
            st.write(f"**Problem:** {paper.get('problem')}")
            st.write(f"**Methodology:** {paper.get('methodology')}")
            st.write(f"**Limitations:** {paper.get('limitations')}")
            st.write(f"**Future Work:** {paper.get('future_work')}")
            st.caption(f"From: {file}")

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
with tab2:
    st.header("🔗 Knowledge Graph View")
    st.markdown("👉 Use [Neo4j Desktop](https://neo4j.com/download/) or browser view at `localhost:7474` to explore the full graph.")
    st.info("Graph rendering inside Streamlit is optional. You can embed NetworkX or Pyvis here if desired.")


with tab3:
    st.header("💡 Generate & Evaluate Hypotheses")

    if st.button("🔁 Generate Hypotheses"):
        context = fetch_graph_context()
        hypotheses = generate_hypothesis(context)
        st.subheader("🧠 Proposed Hypotheses")
        st.code(hypotheses)

        with st.spinner("Evaluating hypotheses..."):
            feedback = evaluate_hypotheses(hypotheses)
        st.subheader("✅ Evaluation Feedback")
        st.text(feedback)
