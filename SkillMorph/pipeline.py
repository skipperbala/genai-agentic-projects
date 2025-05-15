# pipeline.py

from agents.extractor import run_extractor
from agents.comparator import run_comparator
from agents.rewriter import run_rewriter
from agents.advisor import run_advisor
from export.pdf_generator import generate_pdf
from llm.model_config import load_llm
from pathlib import Path
from utils.logger import get_logger

logger = get_logger()

def run_pipeline(resume_path: Path, jd_path: Path) -> Path:
    """
    Execute SkillMorph pipeline with error handling and logging.
    """
    try:
        logger.info("Loading LLM model...")
        llm_model = load_llm("mistral")

        logger.info("Step 1: Extracting resume and JD...")
        extracted_data = run_extractor(resume_path, jd_path, llm_model)

        logger.info("Step 2: Comparing skills and roles...")
        comparison_results = run_comparator(extracted_data, llm_model)

        logger.info("Step 3: Rewriting resume bullets...")
        resume_text = extracted_data.get("resume_text", "")
        jd_text = extracted_data.get("jd_text", "")
        rewritten_result = run_rewriter(resume_text, jd_text, llm_model)

        # Handle whether rewriter returns dict or str
        if isinstance(rewritten_result, dict):
            rewritten_bullets = rewritten_result.get("rewritten_bullets", "")
        else:
            rewritten_bullets = rewritten_result

        logger.info("🎓 Step 4: Generating personalized learning plan...")
        if isinstance(comparison_results, dict):
            learning_plan = run_advisor(comparison_results, llm_model)
        else:
            learning_plan = "Unable to generate learning plan due to comparison format issue."

        logger.info("Step 5: Creating PDF...")
        output_pdf_path = Path("output/optimized_resume_and_plan.pdf")
        generate_pdf(
            rewritten_bullets if isinstance(rewritten_bullets, str) else "\n".join(rewritten_bullets),
            learning_plan,
            output_pdf_path
        )

        logger.info(f"✅ PDF generated at: {output_pdf_path}")
        return output_pdf_path

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise RuntimeError("Pipeline execution failed.") from e
