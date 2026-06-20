import os
import gradio as gr
from huggingface_hub import InferenceClient

# Initialize Hugging Face Client
HF_TOKEN = os.getenv("HF_TOKEN", "YOUR_HF_TOKEN_HERE")
MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"

client = InferenceClient(model=MODEL_ID, api_key=HF_TOKEN)

# System prompts defining the "expert personas"
PERSONAS = {
    "Civic Translator": "You are an expert in local government. Your job is to simplify dense legal jargon and city council transcripts into plain, accessible language for everyday citizens. Highlight key dates, votes, and motions.",
    "Budget & Equity Auditor": "You are a forensic accountant and social equity analyst. Scan the text specifically for financial allocations, tax changes, or policy shifts that disproportionately impact underserved communities. Be objective and data-driven.",
    "Action Advocate": "You are a community organizer. Based on the text provided, help the user draft a professional, persuasive email or public comment letter to their local representatives advocating for or against the policy."
}

def analyze_civic_data(text_input, persona_choice, complexity_level):
    if not text_input.strip():
        return "⚠️ **Please provide some text or a transcript to analyze.**"
    
    system_prompt = PERSONAS[persona_choice]
    user_prompt = (
        f"Analyze the following text. Structure your response clearly using markdown headings, bullet points, and bold text. "
        f"Tailor the explanation level to a '{complexity_level}' audience.\n\n"
        f"Text to analyze:\n{text_input}"
    )
    
    try:
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1024,
            temperature=0.3,
            top_p=0.9
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ **An error occurred:** {str(e)}\n\nPlease ensure your Hugging Face Token is valid."

# 🎨 Custom Cyber-Neon Styling Theme
vibrant_theme = gr.themes.Default(
    primary_hue="fuchsia",
    secondary_hue="cyan",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Orbitron"), "ui-sans-serif", "system-ui"]
).set(
    body_background_fill="#07080a",       # Deep space black
    block_background_fill="#0d0e12",      # Deep obsidian cards
    block_border_width="2px",
    block_border_color="#ff007f",         # Cyber pink borders
    input_background_fill="#141722",
    input_border_color="#00f3ff",         # Cyber cyan input borders
)

# Custom injection CSS for animated gradients, neon glows, and custom button animations
custom_css = """
footer {visibility: hidden}
.container { max-width: 1200px; margin: auto; padding-top: 40px; }

/* Animated Gradient Title */
@keyframes gradient-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.gradient-title {
    background: linear-gradient(-45deg, #ff007f, #00f3ff, #9d4edd, #00f5d4);
    background-size: 400% 400%;
    animation: gradient-shift 10s ease infinite;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3.5rem;
    font-weight: 900;
    text-align: center;
    margin-bottom: 5px;
    letter-spacing: 2px;
    filter: drop-shadow(0 0 10px rgba(0, 243, 255, 0.2));
}
.subtitle-text {
    text-align: center;
    color: #a5b4fc;
    font-size: 1.2rem;
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: 40px;
}

/* Neon Glow Cards */
.gradio-container {
    box-shadow: 0 0 30px rgba(255, 0, 127, 0.1) inset;
}

/* Styled Section Headers */
h3 {
    color: #00f3ff !important;
    text-shadow: 0 0 8px rgba(0, 243, 255, 0.5);
    font-weight: bold;
    letter-spacing: 1px;
}

/* Futuristic Styled Buttons */
.cyber-btn-primary {
    background: linear-gradient(135deg, #ff007f 0%, #7000ff 100%) !important;
    border: none !important;
    box-shadow: 0 0 15px rgba(255, 0, 127, 0.4) !important;
    transition: all 0.3s ease-in-out !important;
    font-weight: bold !important;
}
.cyber-btn-primary:hover {
    transform: scale(1.03) !important;
    box-shadow: 0 0 25px rgba(255, 0, 127, 0.7) !important;
}

.cyber-btn-secondary {
    background: linear-gradient(135deg, #00f3ff 0%, #0070ff 100%) !important;
    color: #000 !important;
    border: none !important;
    box-shadow: 0 0 15px rgba(0, 243, 255, 0.4) !important;
    transition: all 0.3s ease-in-out !important;
    font-weight: bold !important;
}
.cyber-btn-secondary:hover {
    transform: scale(1.03) !important;
    box-shadow: 0 0 25px rgba(0, 243, 255, 0.7) !important;
}
"""

# Building the Interface
with gr.Blocks(theme=vibrant_theme, css=custom_css) as demo:
    
    with gr.Column(elem_classes="container"):
        # Header Section with Gradient Title
        gr.HTML("<h1 class='gradient-title'>⚡ CIVICPULSE AI ⚡</h1>")
        gr.HTML("<p class='subtitle-text'>Demystifying Local Government // Transparent Communities</p>")
        
        with gr.Row():
            # Left Column: Inputs & Controls
            with gr.Column(scale=1):
                gr.Markdown("### 📥 Input Control Hub")
                text_input = gr.Textbox(
                    label="Paste City Council Transcript, Bill Text, or Meeting Minutes",
                    placeholder="Example: 'Resolution 402-B proposes shifting $2M from the public park maintenance fund to...",
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
                
                analyze_btn = gr.Button("🔥 Run AI Audit", variant="primary", size="lg", elem_classes="cyber-btn-primary")
            
            # Right Column: AI Outputs
            with gr.Column(scale=1):
                gr.Markdown("### 📊 Live AI Analysis Workspace")
                
                with gr.Group(): 
                    output_display = gr.Markdown(
                        value="*Analysis will appear here after you paste text and click 'Run AI Audit'.*",
                    )
                
                # Contextual Action Area
                with gr.Accordion("💡 Next Steps & Community Mobilization", open=True):
                    gr.Markdown(
                        "Transform these machine insights into direct local democratic action automatically."
                    )
                    action_btn = gr.Button("📝 Draft Public Comment Letter", variant="secondary", size="md", elem_classes="cyber-btn-secondary")

        # Bottom Architecture Block
        gr.Markdown("<br><hr style='border-color: #ff007f; opacity: 0.3;'><br>")
        
        with gr.Accordion("🛠️ Enterprise Architecture & Technical Spec", open=False):
            gr.Markdown(
                """
                ### Behind the Dashboard:
                * **Dynamic Theming Engine:** Built using a customized abstraction layer of `gr.themes.Default` targeting specific color tokens to enable a sleek, high-contrast dark palette.
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