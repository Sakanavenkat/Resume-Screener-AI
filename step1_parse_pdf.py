import pdfplumber

def parse_resume(pdf_path):
    """
    Opens a PDF resume and extracts all text from it.
    Like a human reading the resume and typing it out.
    """
    full_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    return full_text


# --- TEST ---
if __name__ == "__main__":
    resume_text = parse_resume("SakanaV__Resume.pdf")

    print("=== EXTRACTED RESUME TEXT ===")
    print(resume_text[:1000])
    print(f"\n✅ Total characters extracted: {len(resume_text)}")