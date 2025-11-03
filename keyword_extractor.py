import nltk
from rake_nltk import Rake
import re # Import the regular expression library

nltk.download('punkt')
nltk.download('stopwords')

def extract_keywords(text):
    # 1. Clean the text: Remove punctuation that breaks keywords
    # Remove content inside parentheses, colons, etc.
    cleaned_text = re.sub(r'\(.*?\)', '', text) # Remove (anything in parentheses)
    cleaned_text = re.sub(r'[:;]', ' ', cleaned_text) # Replace colons/semicolons with space
    
    # 2. Initialize RAKE
    # We set a max_length of 3 words for any keyword phrase
    r = Rake(
        stopwords=nltk.corpus.stopwords.words('english'),
        max_length=3
    )

    # 3. Extract keywords from the *cleaned* text
    r.extract_keywords_from_text(cleaned_text)
    
    # 4. Get the 10 highest-scoring phrases
    keywords_with_scores = r.get_ranked_phrases_with_scores() 
    
    # 5. Get just the keyword text
    top_keywords = [kw[1] for kw in keywords_with_scores]
    
    # 6. Post-process: Filter out any keywords that are too short
    final_keywords = []
    for kw in top_keywords:
        if len(kw.strip()) > 3: # Keyword must be longer than 3 characters
            final_keywords.append(kw)

    # Return the best 8 keywords
    return ", ".join(final_keywords[:8])