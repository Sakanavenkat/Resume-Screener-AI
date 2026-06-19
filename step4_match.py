from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

model = None

def get_model():
    global model
    if model is None:
        model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

def match_resume_to_job(resume_text, job_description):
    try:
        m = get_model()
        resume_emb = m.encode([resume_text])
        job_emb    = m.encode([job_description])
        score = cosine_similarity(resume_emb, job_emb)[0][0]
        return round(score * 100, 2)
    except:
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([resume_text, job_description])
        score = cosine_similarity(vectors[0], vectors[1])[0][0]
        return round(score * 100, 2)