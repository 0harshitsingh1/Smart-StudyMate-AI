import nltk
import ssl
import gradio as gr
from summarizer_module import summarize_text
from keyword_extractor import extract_keywords
from quiz_generator import generate_quiz
from tts_module import summary_to_speech
from utils import validate_input

# --- NLTK Downloader (Fix for Hugging Face) ---
# This code runs first to download the language models
# before the app starts, fixing the 'punkt_tab' error.
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

print("Downloading NLTK data...")
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')
print("NLTK data download complete.")
# --- End of NLTK Fix ---


# --- Custom Styling (CSS) ---
custom_css = f"""
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
/* ---------- Root / Page ---------- */
:root{{
    --bg-1: #0f172a;
    --bg-2: #0b1220;
    --accent: #fb923c; /* orange */
    --glass: rgba(255,255,255,0.06);
    --glass-strong: rgba(255,255,255,0.08);
    --muted: #9ca3af;
}}
html, body, #root {{
    height: 100%;
    min-height: 100vh;
    margin: 0;
    font-family: 'Poppins', sans-serif;
    color: #e6eef8;
    -webkit-font-smoothing:antialiased;
    -moz-osx-font-smoothing:grayscale;
    overflow: hidden; /* Prevent scrollbars from background */
    box-sizing: border-box;
    /* --- New Background Image & Blended Gradients --- */
    background-image: 
        radial-gradient(1200px 600px at 10% 20%, rgba(59,130,246,0.06), transparent),
        radial-gradient(800px 400px at 90% 80%, rgba(234,88,12,0.04), transparent),
        url('https://images.unsplash.com/photo-1518770660439-4636190af170?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'); /* Abstract circuit board / tech */
    background-size: cover, cover, cover; /* Ensure all layers cover */
    background-position: center, center, center; /* Center all layers */
    background-repeat: no-repeat, no-repeat, no-repeat; /* No repeat for all layers */
    background-color: var(--bg-1); /* Fallback color, darker base */
    background-blend-mode: overlay, overlay, normal; /* Blend gradients over image */
}}
/* animated floating blobs */
body::before, body::after {{
    content: "";
    position: fixed;
    z-index: 0;
    filter: blur(60px);
    opacity: 0.6;
    pointer-events: none;
}}
body::before {{
    width: 42vmax;
    height: 42vmax;
    left: -10vmax;
    top: -20vmax;
    background: radial-gradient(circle at 30% 30%, rgba(99,102,241,0.18), transparent 35%),
                radial-gradient(circle at 70% 70%, rgba(96,165,250,0.09), transparent 40%);
    animation: blob-slow 18s linear infinite alternate;
}}
body::after {{
    width: 36vmax;
    height: 36vmax;
    right: -14vmax;
    bottom: -24vmax;
    background: radial-gradient(circle at 40% 40%, rgba(251,146,60,0.14), transparent 35%),
                radial-gradient(circle at 60% 60%, rgba(234,88,12,0.06), transparent 45%);
    animation: blob-slower 22s linear infinite alternate-reverse;
}}
@keyframes blob-slow {{
    from {{ transform: translateY(0) rotate(0deg) scale(1); }}
    to   {{ transform: translateY(6vmin) rotate(8deg) scale(1.06); }}
}}
@keyframes blob-slower {{
    from {{ transform: translateY(0) rotate(0deg) scale(1); }}
    to   {{ transform: translateY(-5vmin) rotate(-6deg) scale(1.03); }}
}}
/* ---------- Main container & layout ---------- */
.gradio-container {{
    position: relative;
    z-index: 1; /* above background blobs */
    width: 100vw !important;
    max-width: none !important; /* Ensure it takes full width */
    height: 100vh !important;
    margin: 0 !important;
    padding: 28px !important;
    box-sizing: border-box;
    border-radius: 0 !important;
    display: flex;
    flex-direction: column;
    gap: 18px;
    align-items: center;
    justify-content: flex-start;
}}
/* top area / hero */
.gradio-container > .gr-block:first-child {{
    width: 100%;
    max-width: 1200px;
    display:flex;
    flex-direction:column;
    align-items:center;
    z-index:2;
    pointer-events:auto;
}}
h1 {{
    color: white;
    text-align: center;
    font-size: 2.4rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 12px;
    margin: 8px 0 4px 0;
    letter-spacing: -0.02em;
    background: linear-gradient(90deg, #fff 0%, #ffd8b0 40%, rgba(255,255,255,0.85) 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    text-shadow: 0 6px 24px rgba(2,6,23,0.6);
}}
/* subtitle / copyright */
.copyright {{
    color: var(--muted);
    margin-top: 6px;
    font-size: 13px;
}}
/* content area as a centered card */
.gradio-container .gr-row {{
    width: 100%;
    max-width: 1200px;
    display: flex;
    gap: 22px;
    flex: 1 1 auto;
    align-items: stretch;
    z-index:2;
    pointer-events:auto;
}}
/* glass cards for columns */
.gradio-container .gr-column {{
    flex: 1 1 50%;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 14px;
    align-items: stretch;
    padding: 18px;
    border-radius: 14px;
    background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.04);
    box-shadow: 0 10px 30px rgba(2,6,23,0.55), inset 0 1px 0 rgba(255,255,255,0.02);
    backdrop-filter: blur(8px) saturate(120%);
    -webkit-backdrop-filter: blur(8px) saturate(120%);
    overflow: hidden;
}}
/* make inputs/outputs visually distinct cards */
.gradio-container .gr-column .gr-box,
.gradio-container .gr-column .gr-block,
.gradio-container .gr-column .gr-field {{
    background: transparent;
    border: none;
    padding: 0;
}}
.gradio-container .gr-column .gr-textbox,
.gradio-container .gr-column textarea,
.gradio-container .gr-column .gradio-textbox {{
    background: rgba(2,6,23,0.35);
    color: #e6eef8;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.04);
    padding: 12px;
    resize: vertical;
    min-height: 64px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.02);
}}
/* larger output boxes expand */
.gradio-container .gr-column .gradio-textbox[rows],
.gradio-container .gr-column .gradio-audio {{
    flex: 1 1 auto;
    min-height: 120px;
}}
/* file input and radio styling fallback */
.gradio-container input[type="file"] {{
    background: rgba(255,255,255,0.02);
    border-radius: 8px;
    padding: 10px;
}}
.gradio-container .gr-radio, .gradio-container .gradio-radio {{
    background: transparent;
}}
/* Button styling - pill buttons */
.gr-button.primary {{
    background: linear-gradient(90deg, var(--accent), #ffb86b);
    border: none;
    color: #08101a;
    font-weight: 700;
    padding: 10px 18px;
    border-radius: 999px;
    box-shadow: 0 8px 18px rgba(251,146,60,0.18);
    transition: transform 0.16s ease, box-shadow 0.16s ease;
}}
.gr-button.primary:hover {{
    transform: translateY(-3px) scale(1.01);
    box-shadow: 0 18px 34px rgba(251,146,60,0.22);
}}
.gr-button.secondary {{
    background: transparent;
    color: var(--muted);
    border: 1px solid rgba(255,255,255,0.04);
    padding: 8px 14px;
    border-radius: 999px;
}}
.gr-row > .gr-button, .gr-row > .gr-clear {{
    min-width: 120px;
}}
/* small helper labels */
label {{
    color: #dbeafe;
    font-weight: 600;
    font-size: 0.95rem;
}}
/* remove default footer */
footer {{ display: none !important; }}
/* responsive: stack columns on small screens and center content */
@media (max-width: 1000px) {{
    .gradio-container {{
        padding: 18px !important;
    }}
    .gradio-container .gr-row {{
        flex-direction: column;
        gap: 18px;
        align-items: stretch;
    }}
    .gradio-container .gr-column {{
        width: 100%;
        flex: 0 0 auto;
        padding: 14px;
    }}
    h1 {{ font-size: 1.8rem; }}
}}
/* extra small */
@media (max-width: 480px) {{
    .gradio-container {{
        padding: 12px !important;
    }}
    h1 {{ font-size: 1.35rem; }}
    .gr-button.primary, .gr-button.secondary {{
        width: 100%;
    }}
    .gradio-container .gr-column {{
        padding: 12px;
        border-radius: 10px;
    }}
}}
/* ensure textareas & outputs use available space */
.gradio-container textarea, .gradio-container .gr-textbox {{
    width: 100% !important;
    box-sizing: border-box;
    color: #e6eef8 !important;
}}
/* subtle focus states */
.gradio-container input:focus, .gradio-container textarea:focus, .gradio-container .gradio-textbox:focus {{
    outline: none;
    box-shadow: 0 6px 18px rgba(59,130,246,0.08);
    border-color: rgba(59,130,246,0.12);
}}
/* small utility */
.center-row {{
    display:flex;
    justify-content:center;
    gap:10px;
    align-items:center;
}}
"""

# --- Main Processing Function ---
def process_input(text, pdf_file, summary_size):
    try:
        if pdf_file is not None:
            from pdf_helpers import extract_text_from_pdf
            text = extract_text_from_pdf(pdf_file)
        if not validate_input(text):
            return "Please enter text or upload a PDF.", "", "", None
        
        summary = summarize_text(text, summary_size)
        keywords = extract_keywords(text)
        quiz = generate_quiz(text)
        audio_file = summary_to_speech(summary)
        
        return summary, keywords, quiz, audio_file
    
    except Exception as e:
        print(f"An error occurred: {e}")
        error_message = f"An error occurred: {e}. Please try again."
        return error_message, error_message, error_message, None

# --- Build the Gradio Interface with gr.Blocks ---
with gr.Blocks(
    theme=gr.themes.Default(primary_hue="orange").set(
        # Set body_background_fill to transparent so our CSS background is visible
        body_background_fill="transparent",
        # Also ensure component backgrounds are transparent or slightly opaque
        # to allow background image/blobs to show through the glass effect
        block_background_fill="rgba(255,255,255,0.02)", 
        block_background_fill_dark="rgba(255,255,255,0.02)"
    ),
    css=custom_css,
    analytics_enabled=False
) as app:
    
    # Title and Copyright
    gr.HTML(f"<h1>🔒 Smart StudyMate AI</h1>")
    gr.Markdown("<p class='copyright'>© 2025 Smart StudyMate AI. All rights reserved.</p>")

    # This Row creates the 50/50 split
    with gr.Row():
        
        # --- Left Column (Inputs) ---
        with gr.Column(scale=1):
            with gr.Group():
                text_input = gr.Textbox(label="✍️ Enter Notes or Text", placeholder="Paste your notes here...")
                pdf_input = gr.File(label="📄 Or Upload PDF", file_types=['.pdf'])
                size_input = gr.Radio(
                    label="Select Summary Size",
                    choices=["Small (20-40 words)", "Medium (40-80 words)", "Large (70+ words)"],
                    value="Medium (40-80 words)",
                    interactive=True
                )
            
            with gr.Row():
                submit_btn = gr.Button("Generate", variant="primary")
                clear_btn = gr.ClearButton()
                

        # --- Right Column (Outputs) ---
        with gr.Column(scale=1):
            summary_output = gr.Textbox(label="📘 Summary", lines=6, show_copy_button=True)
            keywords_output = gr.Textbox(label="🔑 Key Topics", lines=3, show_copy_button=True)
            quiz_output = gr.Textbox(label="🧩 Quiz Questions", lines=3, show_copy_button=True)
            audio_output = gr.Audio(label="🔊 Listen to Summary", show_label=True)

    # --- Define Button Logic ---
    submit_btn.click(
        fn=process_input,
        inputs=[text_input, pdf_input, size_input],
        outputs=[summary_output, keywords_output, quiz_output, audio_output]
    )
    
    clear_btn.click(
        fn=lambda: ("", None, "Medium (40-80 words)", "", "", "", None),
        inputs=[],
        outputs=[text_input, pdf_input, size_input, summary_output, keywords_output, quiz_output, audio_output]
    )

# --- Launch the app ---
if __name__ == "__main__":
    app.launch()