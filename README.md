 # RESA - Resume Evaluation & Screening AI

An AI-powered web application that automatically screens resumes against job descriptions, ranks candidates by match score, and generates professional HR explanations using Generative AI.

## ✨ Features
- 📄 Upload up to 5 resumes at once (PDF)
- 🎯 AI match score for each resume
- 🏆 Auto-ranking of candidates
- 📊 Visual bar chart comparison
- 💡 AI improvement tips per resume
- 🕒 Screening history database
- 🎨 Glassmorphism dashboard UI

## 🧠 How It Works

| Step | Technology | What It Does |
|---|---|---|
| Step 1 | pdfplumber | Reads resume PDF and extracts text |
| Step 2 | Python + regex | Finds skills, education, experience |
| Step 3 | sentence-transformers | Converts text to 384 AI embeddings |
| Step 4 | cosine similarity | Compares resume vs job description |
| Step 5 | Groq LLM (Llama 3.3) | Writes professional HR explanation |

## 🏗️ Tech Stack
- **Frontend** → HTML + CSS + Chart.js
- **Backend** → Python + Flask
- **AI/NLP** → sentence-transformers + cosine similarity
- **Generative AI** → Groq API (Llama 3.3 70B)
- **Database** → SQLite
- **PDF Parsing** → pdfplumber

## ⚙️ Installation

```bash
git clone https://github.com/Sakanavenkat/Resume-Screener-AI.git
cd Resume-Screener-AI
pip install -r requirements.txt
python resume_app.py
```

## 🔑 Setup
1. Get free API key from https://console.groq.com
2. Add your key in `resume_app.py`:
```python
GROQ_API_KEY = "your_groq_key_here"
```
3. Run and open http://localhost:5000

## 📊 Sample Results
- Resume: B.E CSE AI & ML Graduate
- Job: Programmer Analyst - AI/ML Role
- Match Score: 55.79%
- Skills Found: 17 (Python, BERT, NLP, ML...)

