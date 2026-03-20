import spacy
import pandas as pd
from fuzzywuzzy import fuzz, process
import re
import os

# Load the small spaCy model
nlp = spacy.load("en_core_web_sm")

# Load skill lexicon
script_dir = os.path.dirname(os.path.abspath(__file__))
skill_path = os.path.join(script_dir, '..', 'data', 'skill_lexicon.csv')
skill_df = pd.read_csv(skill_path)
skill_list = skill_df['skill'].tolist()

def extract_skills(text, method='fuzzy'):
    """
    Extract skills from text using exact and fuzzy matching.
    Returns a dict {skill: confidence}.
    """
    text_lower = text.lower()
    found = {}

    # Exact match
    for skill in skill_list:
        if skill.lower() in text_lower:
            found[skill] = 1.0

    # Fuzzy match on tokens/phrases
    if method == 'fuzzy':
        # Extract possible skill phrases (words or multiple words)
        tokens = set(re.findall(r'\b[a-zA-Z\-]+(?:\s+[a-zA-Z\-]+)*\b', text_lower))
        for skill in skill_list:
            if skill in found:
                continue
            match, score = process.extractOne(skill, tokens, scorer=fuzz.token_sort_ratio)
            if score > 85:
                found[skill] = round(score / 100, 2)

    return found