import os
import gradio as gr
from huggingface_hub import InferenceClient

# Initialize Hugging Face Client
# Replace with your actual token or set the HF_TOKEN environment variable
HF_TOKEN = os.getenv("HF_TOKEN", "YOUR_HF_TOKEN_HERE")
client = InferenceClient(api_key=HF_TOKEN)

# System prompts defining the "expert personas" for the multi-agent feel
PERSONAS = {
    "Civic Translator": "You are an expert in local government. Your job is to simplify dense legal jargon and city council transcripts into plain, accessible language for everyday citizens. Highlight key dates, votes, and motions.",
    "Budget & Equity Auditor": "You are a forensic accountant and social equity analyst. Scan the text specifically for financial allocations, tax changes, or policy shifts that disproportionately impact underserved communities. Be objective and data-driven.",
    "Action Advocate": "You are a community organizer. Based on the text provided, help the user draft a professional, persuasive email or public comment letter to their local representatives advocating for or against the policy."
}

def analyze_civic_data(text_input, persona_choice, complexity_level):
    if not text_input.strip():
        return "⚠️ **Please provide some text or a transcript to analyze.**"
    
    system_prompt = PERSONAS[persona_choice]
    full_prompt = (
        f"{system_prompt}\n\n"
        f"Analyze the following text. Structure your response clearly using markdown headings, bullet points, and bold text. "
        f"Tailor the explanation level to a '{complexity_level}' audience.\n\n"
        f"Text to analyze:\n{text_input}"
    )
    
    try:
        response = client.text_generation(
            model="meta-llama/Meta-Llama-3-8B-Instruct",
            prompt=full_prompt,
            max_new_tokens=1024,
            temperature=0.3, 
            top_p=0.9
        )
        return response
    except Exception as e:
        return f"❌ **An error occurred:** {str(e)}\n\nPlease ensure your Hugging Face Token is valid."

# 🎨 Custom Vibrant & Colorful Styling Theme
vibrant_theme = gr.themes.Default(
    primary_hue="indigo",
    secondary_hue="teal",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Poppins"), "ui-sans-serif", "system-ui"]
).set(
    # Custom color overrides to give it a rich, glowing aesthetic
    body_background_fill="*neutral_950",        # Deep dark background
    block_background_fill="*neutral_900",       # Slightly lighter card background
    block_border_width="2px",
    block_border_color="*primary_500",          # Neon Indigo border outline
    button_primary_background_fill="*primary_600",
    button_primary_background_fill_hover="*primary_500",
    button_primary_text_color="white",
    button_secondary_background_fill="*secondary_600",
    button_secondary_background_fill_hover="*secondary_500",
    button_secondary_text_color="white",
    input_background_fill="*neutral_800",
    input_border_color="*neutral_700"
)

# Custom injection CSS for gradient texts and visual tweaks
custom_css = """
footer {visibility: hidden}
.container { max-width: 1150px; margin: auto; padding-top: 30px; }
.gradient-title {
    background: linear-gradient(90deg, #6366f1, #14b8a6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.8rem;
    font-weight: 800;
    text-align: center;
    margin-bottom: 5px;
}
.subtitle-text {
    text-align: center;
    color: #94a3b8;
    font-size: 1.1rem;
    margin-bottom: 30px;
}
"""

# Building the Interface
with gr.Blocks(theme=vibrant_theme, css=custom_css) as demo:
    
    with gr.Column(elem_classes="container"):
        # Header Section with Gradient Title
        gr.HTML("<h1 class='gradient-title'>🏛️ CivicPulse AI</h1>")
        gr.HTML("<p class='subtitle-text'>Demystifying Local Government for Transparent Communities</p>")
        
        with gr.Row():
            # Left Column: Inputs & Controls
            with gr.Column(scale=1):
                gr.Markdown("### 📥 Input Control Hub")
                text_input = gr.Textbox(
                    label="Paste City Council Transcript, Bill Text, or Meeting Minutes",
                    placeholder="Example: 'Resolution 402-B proposes shifting $2M from the public park maintenance fund to...', or paste an entire PDF transcript here.",
                    lines=12,
                    max_lines=25
                )
                
                with gr.Row():
                    persona_choice = gr.Dropdown(
                        choices=list(PERSONAS.keys()),
                        value="Civic Translator",
                        label="Analysis Lens (Agent Persona)"
                    )
                    complexity_level = gr.Radio(
                        choices=["General Public", "High School Student", "Policy Expert"],
                        value="General Public",
                        label="Target Output Audience"
                    )
                
                analyze_btn = gr.Button("🔥 Run AI Audit", variant="primary", size="lg")
            
            # Right Column: AI Outputs
            with gr.Column(scale=1):
                gr.Markdown("### 📊 Live AI Analysis Workspace")
                
                with gr.Group(): # FIXED: Changed from gr.Box() to gr.Group() for version compatibility
                    output_display = gr.Markdown(
                        value="*Analysis will appear here after you paste text and click 'Run AI Audit'.*",
                    )
                
                # Contextual Action Area
                with gr.Accordion("💡 Next Steps & Community Mobilization", open=True):
                    gr.Markdown(
                        "Transform these machine insights into direct local democratic action automatically."
                    )
                    action_btn = gr.Button("📝 Draft Public Comment Letter", variant="secondary", size="md")

        # Bottom Architecture Block
        gr.Markdown("<br><hr style='border-color: #334155;'><br>")
        
        with gr.Accordion("🛠️ Enterprise Architecture & Technical Spec", open=False):
            gr.Markdown(
                """
                ### Behind the Dashboard:
                * **Dynamic Theming Engine:** Built using a customized abstraction layer of `gr.themes.Default` targeting specific color tokens (`neutral_950`, `primary_600`) to enable a sleek, high-contrast dark palette without writing complex global stylesheets.
                * **System Persona Routing:** Instantly swaps heavy system prompts based on components inputs to guide the local semantic parsing of `Meta-Llama-3-8B-Instruct`.
                * **Zero-Compute Inference:** Offloads inference token loops to serverless endpoint structures using optimized asynchronous HTTP requests.
                """
            )

    # UI Wiring & Callbacks
    analyze_btn.click(
        fn=analyze_civic_data,
        inputs=[text_input, persona_choice, complexity_level],
        outputs=output_display
    )
    
    action_btn.click(
        fn=lambda text: analyze_civic_data(text, "Action Advocate", "General Public"),
        inputs=[text_input],
        outputs=output_display
    )

if __name__ == "__main__":
    demo.launch()