from sentence_transformers import SentenceTransformer

# Load the AI model
# Think of this like hiring an AI expert who understands language
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text):
    """
    Converts text into a list of numbers (embedding).
    Think of it like giving the resume a unique DNA fingerprint in numbers.
    """
    embedding = model.encode(text)
    return embedding


# --- TEST ---
if __name__ == "__main__":
    from step1_parse_pdf import parse_resume

    print("⏳ Loading AI model... (first time takes 1-2 minutes)")

    resume_text = parse_resume("SakanaV__Resume.pdf")
    embedding = embed_text(resume_text)

    print("\n=== EMBEDDING RESULT ===")
    print(f"✅ Resume converted to {len(embedding)} numbers!")
    print(f"🔢 First 5 numbers (sample): {embedding[:5]}")
    print(f"\n💡 These numbers represent your resume's meaning in AI language!")