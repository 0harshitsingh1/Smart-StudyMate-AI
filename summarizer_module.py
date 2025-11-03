from transformers import pipeline

# Load summarization model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
def summarize_text(text, summary_size):
    if not text.strip():
        return "Please enter or upload some text."

    # Set dynamic lengths based on user choice
    if "Small" in summary_size:
        min_len = 20
        max_len = 40
    elif "Large" in summary_size:
        min_len = 70
        max_len = 250
    else: # Default to Medium
        min_len = 40
        max_len = 80
    
    summary = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)
    return summary[0]['summary_text']