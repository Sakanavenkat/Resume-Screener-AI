from groq import Groq
import os

def explain_match(resume_text, job_description, match_score, keywords):
    """
    Sends resume details to Groq AI (free LLM).
    AI writes a professional HR explanation of the match.
    Think of it like asking an expert HR manager to review!
    """

    # Paste your NEW Groq API key her
    client = Groq(api_key=os.environ.get("GROQ_API_KEY", "gsk_f6zK2l8iXgmAQVtSNw4VWGdyb3FYANgVGBbYaEdxJ3OkeRbrF4"))
    prompt = f"""
    You are an expert HR recruiter. Analyze this resume match and give a short professional explanation.
    Do NOT use any markdown formatting like ** or * or #.
    Write in plain text only.

    Match Score: {match_score}%
    Skills found in resume: {keywords['skills']}
    Job Description: {job_description}
    Resume Summary: {resume_text[:500]}

    Please provide:
    1. Overall assessment (2 sentences)
    2. Top 3 matching strengths
    3. Top 2 skill gaps
    4. Final recommendation

    Keep it short and professional.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# --- TEST ---
if __name__ == "__main__":
    from step1_parse_pdf import parse_resume
    from step2_extract_keywords import extract_keywords
    from step4_match import match_resume_to_job

    print("⏳ Loading everything...")

    resume_text = parse_resume("SakanaV__Resume.pdf")
    keywords = extract_keywords(resume_text)

    job_description = """
    We are looking for a Programmer Analyst with skills in Python,
    Machine Learning, Deep Learning, NLP, and Data Analysis.
    Experience with TensorFlow, scikit-learn, pandas is preferred.
    Knowledge of BERT, Transformers, and AI frameworks is a plus.
    Freshers with strong project experience are welcome.
    B.E or B.Tech in Computer Science is required.
    """

    print("⏳ Calculating match score...")
    score = match_resume_to_job(resume_text, job_description)

    print("⏳ Asking AI to explain the match...")
    explanation = explain_match(resume_text, job_description, score, keywords)

    print("\n=== AI EXPLANATION ===")
    print(f"🎯 Match Score : {score}%")
    print(f"\n{explanation}")