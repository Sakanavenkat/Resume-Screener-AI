import re

def extract_keywords(text):
    """
    Scans resume text and pulls out important sections.
    Think of it like a highlighter marking important parts of a resume.
    """

    keywords = {
        "skills": [],
        "education": [],
        "experience": []
    }

    # --- SKILLS ---
    # Common tech skills to look for
    skill_list = [
        "python", "java", "sql", "machine learning", "deep learning",
        "tensorflow", "keras", "pytorch", "scikit-learn", "pandas",
        "numpy", "flask", "fastapi", "bert", "nlp", "cnn", "rnn",
        "lstm", "transformers", "opencv", "matplotlib", "seaborn",
        "git", "docker", "aws", "react", "html", "css", "javascript"
    ]

    text_lower = text.lower()
    for skill in skill_list:
        if skill in text_lower:
            keywords["skills"].append(skill)

    # --- EDUCATION ---
    education_keywords = ["b.e", "b.tech", "m.tech", "mba", "bachelor",
                          "master", "degree", "university", "college", "cgpa"]
    for word in education_keywords:
        if word in text_lower:
            keywords["education"].append(word)

    # --- EXPERIENCE ---
    experience_keywords = ["internship", "intern", "project", "worked",
                           "developed", "built", "designed", "engineer",
                           "analyst", "programmer"]
    for word in experience_keywords:
        if word in text_lower:
            keywords["experience"].append(word)

    return keywords


# --- TEST ---
if __name__ == "__main__":
    # Import Step 1 to get resume text
    from step1_parse_pdf import parse_resume

    resume_text = parse_resume("SakanaV__Resume.pdf")
    keywords = extract_keywords(resume_text)

    print("=== EXTRACTED KEYWORDS ===\n")
    print(f"🛠️  SKILLS FOUND     : {keywords['skills']}")
    print(f"🎓 EDUCATION FOUND  : {keywords['education']}")
    print(f"💼 EXPERIENCE FOUND : {keywords['experience']}")
    print(f"\n✅ Total skills matched: {len(keywords['skills'])}")