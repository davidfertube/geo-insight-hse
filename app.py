"""
Geo-Insight HSE Vision
Real-time PPE Detection System using YOLOv8

A production-ready Industrial AI solution for Health, Safety & Environment compliance
in the Energy Corridor. Detects helmets, goggles, masks, gloves, and safety shoes.

Author: David Fernandez
Portfolio: https://davidfernandez.dev
"""

from ultralytics import YOLO
from huggingface_hub import hf_hub_download

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================

MODEL_REPO = "keremberke/yolov8m-protective-equipment-detection"
MODEL_FILE = "best.pt"

# PPE Classes from the model
PPE_CLASSES = {
    0: "Protective Helmet",
    1: "Shield",
    2: "Jacket",
    3: "Dust Mask",
    4: "Eye Wear",
    5: "Glove",
    6: "Protective Boots"
}

# Colors for each class (BGR format for OpenCV)
CLASS_COLORS = {
    0: (0, 255, 0),      # Green - Helmet
    1: (255, 165, 0),    # Orange - Shield
    2: (0, 255, 255),    # Yellow - Jacket
    3: (255, 0, 255),    # Magenta - Mask
    4: (255, 255, 0),    # Cyan - Eye Wear
    5: (0, 165, 255),    # Orange - Glove
    6: (128, 0, 128),    # Purple - Boots
}

# ============================================================================
# MODEL LOADING
# ============================================================================

def load_model():
    """Download and load the pre-trained PPE detection model from Hugging Face."""
    try:
        # Download model from Hugging Face
        model_path = hf_hub_download(
            repo_id=MODEL_REPO,
            filename=MODEL_FILE
        )
        model = YOLO(model_path)
        print(f"[OK] Model loaded successfully from {MODEL_REPO}")
        return model
    except Exception as e:
        print(f"[WARNING] Could not load HF model: {e}")
        print("[INFO] Falling back to YOLOv8n base model...")
        # Fallback to base YOLOv8 for demo purposes
        return YOLO("yolov8n.pt")

# Global model instance
print("[INFO] Loading PPE Detection Model...")
model = load_model()

if __name__ == "__main__":
    print("[INFO] Model loaded successfully. Ready for inference.")
