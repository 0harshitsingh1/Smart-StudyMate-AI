import nltk
import re  # Import the regular expression library

def generate_quiz(text):
    # --- 1. Clean the Text ---
    # Remove markdown headers, bold, italics, etc.
    cleaned_text = re.sub(r'[\#\*\`\>]+', '', text)
    # Remove list item markers like '-' at the start of a line
    cleaned_text = re.sub(r'^\s*-\s+', '', cleaned_text, flags=re.MULTILINE)
    # Replace newlines with spaces
    cleaned_text = re.sub(r'\n+', ' ', cleaned_text)
    # Squeeze multiple spaces down to one
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text).strip()

    # --- 2. Generate Quiz from Cleaned Text ---
    # Tokenize into sentences
    sentences = nltk.sent_tokenize(cleaned_text)
    
    # Filter for "good" sentences that are at least 10 words long
    good_sentences = [s for s in sentences if len(s.split()) > 10]
    
    if len(good_sentences) == 0:
        return "Not enough content for quiz generation. (Text is too short)"
        
    quiz = []
    # Create questions from the first 3 good sentences
    for i, sent in enumerate(good_sentences[:3]):
        # Take the first 10-12 words
        words = sent.split()
        question_base = ' '.join(words[:12])
        
        # Add '...' if the sentence was longer
        if len(words) > 12:
            question_base += "..."
            
        quiz.append(f"Q{i+1}: {question_base}?")
        
    return "\n".join(quiz)