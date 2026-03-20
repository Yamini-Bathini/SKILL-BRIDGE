import pandas as pd
from modules.hunter import extract_skills

# Prerequisite map (can be extended)
prereq_map = {
    'Machine Learning': ['Statistics', 'Linear Algebra'],
    'Deep Learning': ['Machine Learning', 'Python'],
    'Pandas': ['Python'],
    'Scikit-learn': ['Python'],
    'TensorFlow': ['Python', 'Machine Learning'],
    'PyTorch': ['Python', 'Machine Learning'],
    'Data Visualization': ['Pandas', 'Python']
}

def analyze_gaps(resume_text, jd_text):
    """
    Compare resume skills with job description skills.
    Returns a dict with 'has', 'required', and 'gaps'.
    """
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    # Identify missing skills
    missing = {}
    for skill, conf in jd_skills.items():
        if skill not in resume_skills:
            missing[skill] = conf

    # Add prerequisites for missing skills that are not already present
    all_needed = set(missing.keys())
    for skill in list(missing.keys()):
        if skill in prereq_map:
            for prereq in prereq_map[skill]:
                if prereq not in resume_skills and prereq not in all_needed:
                    missing[prereq] = 0.9  # inferred prerequisite
                    all_needed.add(prereq)

    return {
        'has': resume_skills,
        'required': jd_skills,
        'gaps': missing
    }