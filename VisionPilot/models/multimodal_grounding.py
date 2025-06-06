import os

folders = [
    "VisionPilot/data/images",
    "VisionPilot/data/docs",
    "VisionPilot/data/outputs",
    "VisionPilot/models",
    "VisionPilot/agents",
    "VisionPilot/retriever",
    "VisionPilot/utils",
    "VisionPilot/notebooks"
]

files = {
    "VisionPilot/README.md": "# VisionPilot: Industrial Fault Explainer\n",
    "VisionPilot/requirements.txt": "",
    "VisionPilot/.gitignore": "__pycache__/\n.env\n*.ckpt\n*.pt\n*.log\noutputs/\n",
    "VisionPilot/config.yaml": "device: cuda\nmodel:\n  captioner: blip2\n  detector: yolov8n.pt\n",
    "VisionPilot/main.py": "# Entry point for VisionPilot pipeline\n",
    "VisionPilot/.env": "# Add API keys or config variables here\n",

    # Init files
    "VisionPilot/models/__init__.py": "",
    "VisionPilot/agents/__init__.py": "",
    "VisionPilot/retriever/__init__.py": "",
    "VisionPilot/utils/__init__.py": "",

    # Sample notebooks
    "VisionPilot/notebooks/01_test_captioning.ipynb": "",
    "VisionPilot/notebooks/02_object_detection.ipynb": "",
    "VisionPilot/notebooks/03_agent_workflow.ipynb": "",
}

def create_structure():
    # Create folders
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✅ Created folder: {folder}")

    # Create files
    for file_path, content in files.items():
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"📄 Created file: {file_path}")

if __name__ == "__main__":
    create_structure()

