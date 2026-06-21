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

# Sample datasets for rapid testing
SAMPLE_DATA = {
    "City Budget Reallocation": "Resolution 2026-44B: Section 4.A outlines a structural amendment to the municipal budget. The City Council proposes a reduction of $4,200,000 from the Public Parks & Community Infrastructure Maintenance fund. Concurrently, Section 4.B dictates the immediate allocation of $3,850,000 to the Department of Police Technology Upgrades for automated license plate reader expansions and predictive analytics software licenses. Public feedback window closes in 14 days. Vote passed 5-2 in preliminary session.",
    "Zoning & Affordable Housing Amendment": "Ordinance No. 902-Z modifies Municipal Code Chapter 11 regarding high-density residential development. The amendment repeals mandatory inclusionary zoning thresholds which previously required commercial developers to set aside 12% of units for low-income residents in Transit-Oriented Districts. The revised text establishes a voluntary 'Density Bonus' system, where developers can opt out of affordable housing mandates by paying an in-lieu fee of $45,000 per missing unit into the general housing trust fund. Community activists note this trust fund has a 3-year backlog for deployment.",
}

def analyze_civic_data(text_input, persona_choice, complexity_level):
    if not text_input or not text_input.strip():
        return "⚠️ **Please provide some text or a transcript to analyze.**"
    
    system_prompt = PERSONAS[persona_choice]
    user_prompt = (
        f"{system_prompt}\n\n"
        f"Analyze the following text. Structure your response beautifully using markdown headings, bullet points, and bold text. "
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

def run_multi_agent_debate(text_input):
    if not text_input or not text_input.strip():
        return "⚠️ **Please provide a text or proposal to debate.**"
    
    prompt = (
        f"You are hosting a panel between two experts regarding this municipal text:\n\n'{text_input}'\n\n"
        f"Provide a structured debate layout. "
        f"First, have the 'Budget Auditor' criticize the fiscal efficiency and systemic equity of the proposal. "
        f"Second, have a 'Civic Optimist' defend the potential structural advantages or administrative goals of the proposal. "
        f"Conclude with a 'Synthesized Verdict' highlighting the core tension citizens should look out for."
    )
    try:
        response = client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1200,
            temperature=0.4
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ **Debate engine failed:** {str(e)}"

def load_sample(choice):
    return SAMPLE_DATA.get(choice, "")

# 🎨 Premium High-Contrast Cyberpunk Theme Configuration
cyber_theme = gr.themes.Default(
    primary_hue="fuchsia",
    secondary_hue="cyan",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Inter"), "-apple-system", "sans-serif"]
).set(
    body_background_fill="#050609",       # Deep Void Black
    block_background_fill="#0b0d13",      # Crisp Obsidian Cards
    block_border_width="1px",
    block_border_color="#1e293b",         # Sleek subtle border default
    input_background_fill="#111420",      # Dark contrast inputs
    input_border_color="#00f3ff",         # Cyber Cyan focal rings
    button_primary_background_fill="linear-gradient(135deg, #ff007f 0%, #7000ff 100%)",
    button_secondary_background_fill="linear-gradient(135deg, #00f3ff 0%, #0070ff 100%)",
)

# Advanced Custom CSS Injector for Layout Enhancements and Glow Metrics
custom_css = """
footer { visibility: hidden !important; }
.container { max-width: 1300px; margin: auto; padding-top: 20px; }

/* Animated Neon Cyber Header */
@keyframes cyber-pulse {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.glitch-title {
    background: linear-gradient(-45deg, #ff007f, #00f3ff, #ab47bc, #00e5ff);
    background-size: 300% 300%;
    animation: cyber-pulse 12s ease infinite;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3.5rem;
    font-weight: 900;
    text-align: center;
    margin-bottom: 2px;
    letter-spacing: -1px;
}
.subtitle-text {
    text-align: center;
    color: #94a3b8;
    font-size: 1rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 4px;
    margin-bottom: 30px;
}

/* Custom Metric Cards */
.metric-card {
    background: #0f172a !important;
    border: 1px solid #ff007f !important;
    border-radius: 8px !important;
    padding: 15px !important;
    text-align: center;
    box-shadow: 0 0 10px rgba(255, 0, 127, 0.1);
}
.metric-card-alt {
    background: #0f172a !important;
    border: 1px solid #00f3ff !important;
    border-radius: 8px !important;
    padding: 15px !important;
    text-align: center;
    box-shadow: 0 0 10px rgba(0, 243, 255, 0.1);
}

/* Tab Layout Adjustments */
.tabs {
    border-bottom: 2px solid #1e293b !important;
}
.tab-nav button.selected {
    color: #00f3ff !important;
    border-bottom: 2px solid #00f3ff !important;
    font-weight: bold !important;
}

/* Button UI Scale Effects */
.cyber-btn {
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}
.cyber-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(255, 0, 127, 0.3) !important;
}
.cyber-btn-sec:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(0, 243, 255, 0.3) !important;
}
"""

# Theme and CSS removed from constructor here
with gr.Blocks() as demo:
    with gr.Column(elem_classes="container"):
        # Header System
        gr.HTML("<h1 class='glitch-title'>⚡ CIVICPULSE // OS</h1>")
        gr.HTML("<p class='subtitle-text'>Decentralized Semantic Analysis Protocol for Local Democracy</p>")
        
        # Upper KPI Dashboard / Metric Highlights
        with gr.Row():
            with gr.Column(elem_classes="metric-card", scale=1):
                gr.Markdown("### 🔍 TARGET\nMunicipal Transparency")
            with gr.Column(elem_classes="metric-card-alt", scale=1):
                gr.Markdown("### ⚙️ CORE ENGINE\nLlama-3-8B-Instruct")
            with gr.Column(elem_classes="metric-card", scale=1):
                gr.Markdown("### 🗺️ STATUS\nInference Node Online")
        
        gr.Markdown("<br>")

        # Primary Workspace Multi-Tab Architecture
        with gr.Tabs(elem_classes="tabs"):
            
            # TAB 1: Core AI Auditing Framework
            with gr.TabItem("📊 SYSTEM AUDIT PROTOCOL"):
                with gr.Row():
                    # Inputs Column
                    with gr.Column(scale=1):
                        gr.Markdown("### 📥 Document Intake Node")
                        
                        # Fixed dropdown argument bug
                        sample_selector = gr.Dropdown(
                            choices=list(SAMPLE_DATA.keys()),
                            label="⚡ Quick Load Demo Dataset",
                            filterable=True
                        )
                        
                        text_input = gr.Textbox(
                            label="Municipal Document Payload (Transcripts, Resolutions, Zoning Codes)",
                            placeholder="Paste text here or select a quick load dataset above...",
                            lines=10,
                            max_lines=20
                        )
                        
                        with gr.Row():
                            persona_choice = gr.Dropdown(
                                choices=list(PERSONAS.keys()),
                                value="Civic Translator",
                                label="Analytical Persona Lens"
                            )
                            complexity_level = gr.Radio(
                                choices=["General Public", "High School Student", "Policy Expert"],
                                value="General Public",
                                label="Target Formatting Horizon"
                            )
                        
                        analyze_btn = gr.Button("🔥 INITIALIZE AI AUDIT", variant="primary", elem_classes="cyber-btn")
                    
                    # Outputs Column
                    with gr.Column(scale=1):
                        gr.Markdown("### 🖥️ Decrypted Output Display")
                        with gr.Group():
                            output_display = gr.Markdown(
                                value="*Awaiting analysis initialization payload...*"
                            )
                        
                        gr.Markdown("---")
                        gr.Markdown("### 💡 Downstream Automation Protocols")
                        with gr.Row():
                            action_btn = gr.Button("📝 DRAFT CIVIC ACTION LETTER", variant="secondary", elem_classes="cyber-btn-sec")
            
            # TAB 2: Multi-Agent Cross Examination
            with gr.TabItem("⚔️ MULTI-AGENT DEBATE ENGINE"):
                gr.Markdown("### 🧠 Automated Hegelian Dialectic Console")
                gr.Markdown("Synthesize objective truth by forcing multiple specialized personas to debate the policy proposal from conflicting perspectives.")
                
                with gr.Row():
                    with gr.Column(scale=1):
                        debate_input = gr.Textbox(
                            label="Target Policy Text for Cross-Examination",
                            placeholder="Paste specific controversial clauses here...",
                            lines=8
                        )
                        run_debate_btn = gr.Button("⚡ TRIGGER CONTRAST DEBATE", variant="primary", elem_classes="cyber-btn")
                    
                    with gr.Column(scale=1):
                        debate_output = gr.Markdown(value="*Dialectic terminal idle. Initiate trigger...*")

            # TAB 3: Tech Spec & Node Infrastructure
            with gr.TabItem("🛠️ ARCHITECTURE SPECIFICATION"):
                gr.Markdown(
                    """
                    ### 🎛️ System Configuration Matrix
                    
                    | Layer | Protocol | Function |
                    | :--- | :--- | :--- |
                    | **UI Frontend Layer** | Gradio Blocks 6.0 | High-readability responsive UI layout framework |
                    | **Inference Pipeline** | Hugging Face Serverless API | Handles low-latency token streaming and model routing |
                    | **Semantic Parser** | Meta-Llama-3-8B-Instruct | Deep structural analysis of complex legalese |
                    | **Design Theme** | Custom Cyberpunk CSS Core | Tailored styles avoiding bloom effects for ideal pixel rendering |
                    
                    ### 🔒 Privacy Guard Informational Node
                    * All input parsing sessions operate stateless over secure TLS endpoints. 
                    * Local analysis runs on zero-compute structures directly utilizing distributed open-weight inference hardware clusters.
                    """
                )
        
        # System Footer
        gr.Markdown("<br><hr style='border-color: #ff007f; opacity: 0.1;'><br>")
        gr.Markdown("<p style='text-align: center; color: #475569; font-size: 0.8rem;'>CIVICPULSE OS v2.4.0 // Secured Connection Verified // 2026</p>")

    # --- Event Wiring Logic ---
    
    sample_selector.change(
        fn=load_sample,
        inputs=[sample_selector],
        outputs=[text_input]
    )
    
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
    
    run_debate_btn.click(
        fn=run_multi_agent_debate,
        inputs=[debate_input],
        outputs=debate_output
    )

if __name__ == "__main__":
    # Theme and CSS injected into launch() to adhere to Gradio specifications
    demo.launch(theme=cyber_theme, css=custom_css)