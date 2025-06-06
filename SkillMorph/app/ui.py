import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pipeline import run_pipeline
import streamlit as st
from pathlib import Path
import tempfile
import shutil
from utils.logger import get_logger

logger = get_logger()

st.set_page_config(page_title="SkillMorph", layout="centered")

st.title("🧠 SkillMorph: Agentic Resume Optimizer")
st.markdown("Upload your **resume** and **job description**, and let AI tailor your resume + suggest personalized upskilling.")

with st.form("resume_form", clear_on_submit=False):
    resume_file = st.file_uploader("📎 Upload Resume (PDF)", type=["pdf"])
    jd_file = st.file_uploader("📄 Upload Job Description (PDF or TXT)", type=["pdf", "txt"])
    submitted = st.form_submit_button("🚀 Optimize Resume")

if submitted:
    if not resume_file or not jd_file:
        st.warning("Please upload both your resume and the job description.")
    else:
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                resume_path = Path(tmpdir) / "resume.pdf"
                jd_path = Path(tmpdir) / jd_file.name

                with open(resume_path, "wb") as f:
                    f.write(resume_file.read())
                with open(jd_path, "wb") as f:
                    f.write(jd_file.read())

                with st.spinner("🔧 Running SkillMorph pipeline..."):
                    output_pdf = run_pipeline(resume_path, jd_path)

                # Copy to Streamlit's download directory
                output_dest = Path("output/SkillMorph_Report.pdf")
                shutil.copy(output_pdf, output_dest)

                st.success("✅ Optimization complete! Download your results below:")
                st.download_button(
                    label="📥 Download Optimized Resume + Learning Plan (PDF)",
                    data=open(output_dest, "rb").read(),
                    file_name="SkillMorph_Optimized_Resume.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            logger.error(f"Streamlit UI error: {e}")
            st.error("Something went wrong during optimization. Please try again.")
