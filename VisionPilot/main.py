import os
from dotenv import load_dotenv

from models.vision_caption import VisionCaptioner
from models.object_detection import FaultDetector
from retriever.vector_store import query_documents
from agents.root_cause_agent import RootCauseAgent
from agents.explainer_agent import ExplanationAgent
import gradio as gr
from PIL import Image


# Load .env
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# Initialize models
captioner = VisionCaptioner()
detector = FaultDetector(model_path="yolov8n.pt")
root_agent = RootCauseAgent(openai_key=OPENAI_KEY)
explain_agent = ExplanationAgent(openai_key=OPENAI_KEY)

def run_pipeline(image_path):
    print("🔍 Generating caption...")
    caption = captioner.generate_caption(image_path)
    print(f"📝 Caption: {caption}")

    print("📦 Detecting objects...")
    detection_results = detector.detect(image_path)
    labels = [box.name for box in detection_results[0].boxes.data] if detection_results[0].boxes else []
    print(f"📌 Detected Faults: {labels}")

    print("📚 Retrieving documents...")
    top_docs = query_documents(" ".join(labels) + " " + caption)

    print("🧠 Root cause analysis...")
    diagnosis = root_agent.analyze_fault(caption, labels, top_docs)
    print(f"⚙️ Diagnosis: {diagnosis}")

    print("💡 Generating explanation and fix...")
    explanation = explain_agent.explain_fix(caption, diagnosis)
    print(f"🛠️ Explanation: {explanation}")

    return {
        "caption": caption,
        "detections": labels,
        "diagnosis": diagnosis,
        "explanation": explanation
    }

def run_gradio_interface():
    def infer(image):
        # Save uploaded image
        image_path = "data/images/temp.jpg"
        Image.fromarray(image).save(image_path)

        result = run_pipeline(image_path)
        return (
            result["caption"],
            ", ".join(result["detections"]),
            result["diagnosis"],
            result["explanation"]
        )

    interface = gr.Interface(
        fn=infer,
        inputs=gr.Image(type="numpy", label="Upload Fault Image"),
        outputs=[
            gr.Textbox(label="Generated Caption"),
            gr.Textbox(label="Detected Fault Labels"),
            gr.Textbox(label="Root Cause Diagnosis"),
            gr.Textbox(label="Fix Explanation")
        ],
        title="🔧 VisionPilot: Industrial Fault Explainer",
        description="Upload an image of a faulty machine part. The system will describe, analyze, and explain the likely cause and fix."
    )

    interface.launch()

if __name__ == "__main__":
    test_img = "data/images/sample_fault.jpg"  # replace with your test image
    output = run_pipeline(test_img)

    print("\n✅ Pipeline Complete!")
    for key, val in output.items():
        print(f"\n🔹 {key.upper()}:\n{val}")
    run_gradio_interface()
