from step1_parse_pdf import parse_resume
from step2_extract_keywords import extract_keywords
from step4_match import match_resume_to_job
from step5_explain import explain_match

def run_resume_screener(resume_path, job_description):
    """
    Master function that runs all 5 steps together.
    Think of it like a conveyor belt in a factory —
    resume goes in one end, AI explanation comes out the other!
    """

    print("\n" + "="*50)
    print("   🤖 RESUME SCREENER WITH AI")
    print("="*50)

    # STEP 1 — Parse PDF
    print("\n⏳ Step 1: Reading resume PDF...")
    resume_text = parse_resume(resume_path)
    print(f"✅ Resume read! ({len(resume_text)} characters extracted)")

    # STEP 2 — Extract Keywords
    print("\n⏳ Step 2: Extracting keywords...")
    keywords = extract_keywords(resume_text)
    print(f"✅ Found {len(keywords['skills'])} skills: {keywords['skills']}")

    # STEP 3 — Embed (happens inside step 4)
    print("\n⏳ Step 3 & 4: Embedding + Calculating match score...")

    # STEP 4 — Match Score
    score = match_resume_to_job(resume_text, job_description)
    print(f"✅ Match Score calculated!")

    # STEP 5 — AI Explanation
    print("\n⏳ Step 5: Asking AI to explain the match...")
    explanation = explain_match(resume_text, job_description, score, keywords)

    # FINAL OUTPUT
    print("\n" + "="*50)
    print("   📊 FINAL RESULTS")
    print("="*50)

    print(f"\n📄 Resume    : {resume_path}")
    print(f"🎯 Match Score: {score}%")

    if score >= 70:
        print("🟢 STRONG MATCH — Great fit!")
    elif score >= 50:
        print("🟡 MODERATE MATCH — Some skills align")
    else:
        print("🔴 LOW MATCH — Needs more relevant skills")

    print("\n--- 🤖 AI EXPLANATION ---")
    print(explanation)
    print("\n" + "="*50)


# --- RUN ---
if __name__ == "__main__":

    # Your resume
    resume_path = "SakanaV__Resume.pdf"

    # Job Description
    job_description = """
    We are looking for a Programmer Analyst with skills in Python,
    Machine Learning, Deep Learning, NLP, and Data Analysis.
    Experience with TensorFlow, scikit-learn, pandas is preferred.
    Knowledge of BERT, Transformers, and AI frameworks is a plus.
    Freshers with strong project experience are welcome.
    B.E or B.Tech in Computer Science is required.
    """

    run_resume_screener(resume_path, job_description)