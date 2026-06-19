import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

def explain_match(resume_text, job_description, match_score, keywords):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    prompt = f"""
    You are an expert HR recruiter. Analyze this resume match.
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

    response = Groq(
        api_key=os.environ.get("GROQ_API_KEY")
    ).chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content