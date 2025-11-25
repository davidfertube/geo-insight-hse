"""
Geo-Insight HSE Vision
Real-time PPE Detection System using YOLOv8

A production-ready Industrial AI solution for Health, Safety & Environment compliance
in the Energy Corridor. Detects helmets, goggles, masks, gloves, and safety shoes.

Author: David Fernandez
Portfolio: https://davidfernandez.dev
"""

import cv2
import numpy as np
from PIL import Image
import time
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
        return YOLO("yolov8n.pt")

# Global model instance
print("[INFO] Loading PPE Detection Model...")
model = load_model()

# ============================================================================
# KPI TRACKING
# ============================================================================

class KPITracker:
    """Track detection performance metrics for the dashboard."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.total_detections = 0
        self.frames_processed = 0
        self.total_inference_time = 0
        self.detections_by_class = {cls: 0 for cls in PPE_CLASSES.values()}
        self.compliance_scores = []
    
    def update(self, results, inference_time):
        self.frames_processed += 1
        self.total_inference_time += inference_time
        
        if results and len(results) > 0:
            boxes = results[0].boxes
            if boxes is not None:
                self.total_detections += len(boxes)
                
                # Count detections by class
                for cls_id in boxes.cls.cpu().numpy():
                    cls_name = PPE_CLASSES.get(int(cls_id), "Unknown")
                    if cls_name in self.detections_by_class:
                        self.detections_by_class[cls_name] += 1
    
    def get_metrics(self):
        avg_latency = (self.total_inference_time / self.frames_processed * 1000) if self.frames_processed > 0 else 0
        return {
            "frames_processed": self.frames_processed,
            "total_detections": self.total_detections,
            "avg_latency_ms": round(avg_latency, 2),
            "detections_per_frame": round(self.total_detections / max(1, self.frames_processed), 2),
            "detections_by_class": self.detections_by_class.copy()
        }

# Global KPI tracker
kpi_tracker = KPITracker()

# ============================================================================
# DETECTION FUNCTIONS
# ============================================================================

def detect_ppe(image, confidence_threshold=0.25):
    """
    Run PPE detection on an input image.
    
    Args:
        image: Input image (PIL Image or numpy array)
        confidence_threshold: Minimum confidence for detections
    
    Returns:
        Annotated image with bounding boxes and labels
    """
    if image is None:
        return None, "No image provided", ""
    
    # Convert to numpy array if needed
    if isinstance(image, Image.Image):
        image_np = np.array(image)
    else:
        image_np = image
    
    # Ensure RGB format
    if len(image_np.shape) == 2:
        image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)
    elif image_np.shape[2] == 4:
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)
    
    # Run inference
    start_time = time.time()
    results = model(image_np, conf=confidence_threshold, verbose=False)
    inference_time = time.time() - start_time
    
    # Update KPIs
    kpi_tracker.update(results, inference_time)
    
    # Get annotated image
    annotated = results[0].plot()
    
    # Build detection summary
    summary_lines = []
    if results[0].boxes is not None and len(results[0].boxes) > 0:
        boxes = results[0].boxes
        detected_items = {}
        
        for i, (cls_id, conf) in enumerate(zip(boxes.cls.cpu().numpy(), boxes.conf.cpu().numpy())):
            cls_name = PPE_CLASSES.get(int(cls_id), f"Class {int(cls_id)}")
            if cls_name not in detected_items:
                detected_items[cls_name] = []
            detected_items[cls_name].append(f"{conf:.1%}")
        
        summary_lines.append(f"**{len(boxes)} PPE Items Detected**\n")
        for item, confs in detected_items.items():
            summary_lines.append(f"- {item}: {len(confs)} detected ({', '.join(confs)})")
    else:
        summary_lines.append("No PPE detected in this image")
    
    summary_lines.append(f"\nInference Time: {inference_time*1000:.1f}ms")
    
    # Get KPI report
    metrics = kpi_tracker.get_metrics()
    kpi_report = f"""
## Session KPIs

| Metric | Value | Target |
|--------|-------|--------|
| Frames Processed | {metrics['frames_processed']} | - |
| Total Detections | {metrics['total_detections']} | - |
| Avg Latency | {metrics['avg_latency_ms']:.1f}ms | <100ms |
| Detections/Frame | {metrics['detections_per_frame']:.1f} | - |

### Detection Distribution
"""
    for cls_name, count in metrics['detections_by_class'].items():
        if count > 0:
            kpi_report += f"- **{cls_name}**: {count}\n"
    
    return annotated, "\n".join(summary_lines), kpi_report


def reset_kpis():
    """Reset the KPI tracker."""
    kpi_tracker.reset()
    return "KPIs Reset Successfully", ""

if __name__ == "__main__":
    print("[INFO] Model and KPI tracker loaded. Ready for inference.")
