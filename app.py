import gradio as gr
from PIL import Image
from src.vision_agent import vision_agent

def hse_analysis(image, task):
    if image is None:
        return "Please upload an image."
    
    try:
        # Convert numpy array to PIL Image if necessary
        if not isinstance(image, Image.Image):
            image = Image.fromarray(image)
        
        result = vision_agent.analyze_image(image, task)
        return result
    except Exception as e:
        return f"### Error During Analysis\n{str(e)}"

# ============================================
# GRADIO UI
# ============================================

with gr.Blocks(title="Geo Insight HSE", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # Geo Insight HSE
    ### Vision AI Safety Inspector
    
    Using **Qwen2-VL** to detect PPE violations and hazardous conditions in real-time.
    """)
    
    with gr.Row():
        with gr.Column():
            input_img = gr.Image(label="Site Photo / CCTV Frame")
            task_input = gr.Dropdown(
                choices=[
                    "PPE Compliance Check",
                    "Hazard Identification",
                    "Worker Safety Verification",
                    "Zone Perimeter Breach"
                ],
                label="Analysis Task",
                value="PPE Compliance Check"
            )
            submit_btn = gr.Button("Run AI Inspection", variant="primary")
            
        with gr.Column():
            output_text = gr.Markdown(label="Safety Assessment")
            
    gr.Examples(
        examples=[
            ["https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/segmentation.png", "Work Zone Analysis"]
        ],
        inputs=[input_img, task_input]
    )
    
    submit_btn.click(
        fn=hse_analysis,
        inputs=[input_img, task_input],
        outputs=[output_text]
    )
    
    gr.Markdown("""
    ---
    **Tech Stack:** Qwen2-VL • Hugging Face Inference • PIL • Gradio
    
    **Author:** [David Fernandez](https://davidfernandez.dev) | AI Engineer
    """)

if __name__ == "__main__":
    demo.launch()
