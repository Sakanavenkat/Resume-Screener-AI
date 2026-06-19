from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load AI model
model = SentenceTransformer('all-MiniLM-L6-v2')

def match_resume_to_job(resume_text, job_description):
    """
    Compares resume with job description mathematically.
    Think of it like checking how many puzzle pieces fit together.
    The higher the score, the better the match!
    """

    # Convert both texts to numbers (embeddings)
    resume_embedding = model.encode([resume_text])
    job_embedding = model.encode([job_description])

    # Calculate similarity score (0 to 1)
    # 1.0 = perfect match, 0.0 = no match
    score = cosine_similarity(resume_embedding, job_embedding)[0][0]

    # Convert to percentage
    match_percentage = round(score * 100, 2)

    return match_percentage


# --- TEST ---
if __name__ == "__main__":
    from step1_parse_pdf import parse_resume

    print("⏳ Loading AI model...")

    # Your real resume
    resume_text = parse_resume("SakanaV__Resume.pdf")

    # Sample job description (like a real Cognizant JD)
    job_description = """
    We are looking for a Programmer Analyst with skills in Python,
    Machine Learning, Deep Learning, NLP, and Data Analysis.
    Experience with TensorFlow, scikit-learn, pandas is preferred.
    Knowledge of BERT, Transformers, and AI frameworks is a plus.
    Freshers with strong project experience are welcome.
    B.E or B.Tech in Computer Science is required.
    """

    print("\n⏳ Comparing resume with job description...")
    score = match_resume_to_job(resume_text, job_description)

    print("\n=== MATCH RESULT ===")
    print(f"📄 Job Description : Programmer Analyst - AI/ML Role")
    print(f"🎯 Match Score     : {score}%")

    if score >= 70:
        print("🟢 STRONG MATCH — Great fit for this role!")
    elif score >= 50:
        print("🟡 MODERATE MATCH — Some skills align")
    else:
        print("🔴 LOW MATCH — Resume needs more relevant skills")