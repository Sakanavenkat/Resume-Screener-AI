from flask import Flask, request, render_template_string
from step1_parse_pdf import parse_resume
from step2_extract_keywords import extract_keywords
from step4_match import match_resume_to_job
from step5_explain import explain_match
from groq import Groq
import os, sqlite3
from datetime import datetime

app = Flask(__name__)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "gsk_f6zK2l8iXgmAQVtSNw4VWGdyb3FYANgVGBbYaEdxJ3OkeRbrF4")

def init_db():
    conn = sqlite3.connect("screening_new.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS screenings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resume_name TEXT, score REAL, verdict TEXT,
        skills TEXT, explanation TEXT, job_description TEXT, created_at TEXT)""")
    conn.commit(); conn.close()

def save_to_db(name, score, verdict, skills, explanation):
    conn = sqlite3.connect("screening_new.db")
    c = conn.cursor()
    c.execute("""INSERT INTO screenings
        (resume_name, score, verdict, skills, explanation, created_at)
        VALUES (?,?,?,?,?,?)""",
        (name, score, verdict, skills, explanation,
         datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit(); conn.close()

def get_history():
    conn = sqlite3.connect("screening_new.db")
    c = conn.cursor()
    c.execute("SELECT * FROM screenings ORDER BY created_at DESC LIMIT 20")
    rows = c.fetchall(); conn.close()
    return rows

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>AI Resume Screener</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Arial,sans-serif;background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);min-height:100vh;color:#fff}
.app{display:flex;min-height:100vh}

/* SIDEBAR */
.sidebar{width:220px;background:rgba(255,255,255,0.05);backdrop-filter:blur(20px);border-right:1px solid rgba(255,255,255,0.1);padding:24px 16px;position:sticky;top:0;height:100vh}
.logo{font-size:16px;font-weight:700;margin-bottom:28px;padding-bottom:16px;border-bottom:1px solid rgba(255,255,255,0.1);text-align:center}
.logo span{color:#a78bfa}
.nav-item{display:flex;align-items:center;gap:10px;padding:11px 14px;border-radius:10px;color:rgba(255,255,255,0.6);font-size:13px;margin-bottom:6px;cursor:pointer;text-decoration:none}
.nav-item:hover{background:rgba(167,139,250,0.15);color:#fff}
.nav-dot{width:8px;height:8px;border-radius:50%}

/* MAIN */
.main{flex:1;padding:28px}
.topbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}
.topbar h1{font-size:20px;font-weight:700}
.topbar p{color:rgba(255,255,255,0.4);font-size:12px}

/* STAT CARDS */
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:24px}
.stat{background:rgba(255,255,255,0.07);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,0.1);border-radius:14px;padding:16px}
.stat-label{color:rgba(255,255,255,0.5);font-size:11px;margin-bottom:8px;text-transform:uppercase;letter-spacing:1px}
.stat-value{font-size:26px;font-weight:700;color:#fff}
.stat-value small{font-size:13px;color:#34d399;margin-left:6px}

/* GLASS CARDS */
.glass{background:rgba(255,255,255,0.07);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:22px;margin-bottom:20px}
.glass h2{font-size:14px;font-weight:600;color:rgba(255,255,255,0.9);margin-bottom:16px;padding-bottom:10px;border-bottom:1px solid rgba(255,255,255,0.08)}

/* FORM */
.upload-zone{border:1.5px dashed rgba(167,139,250,0.5);border-radius:12px;padding:20px;text-align:center;margin-bottom:14px;color:rgba(255,255,255,0.5);font-size:13px}
.upload-zone strong{display:block;color:#a78bfa;font-size:15px;margin-bottom:6px}
input[type=file]{color:rgba(255,255,255,0.7);font-size:13px;margin-top:8px}
textarea{width:100%;height:110px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.15);border-radius:10px;padding:12px;color:#fff;font-size:13px;resize:vertical;margin-top:8px}
textarea::placeholder{color:rgba(255,255,255,0.3)}
label{font-size:13px;color:rgba(255,255,255,0.7);font-weight:600}
.btn{background:linear-gradient(135deg,#7c3aed,#a78bfa);color:#fff;border:none;padding:13px;border-radius:10px;font-size:14px;cursor:pointer;width:100%;margin-top:14px;font-weight:600}
.btn:hover{opacity:0.9}

/* RANKING TABLE */
.rank-table{width:100%;border-collapse:collapse;font-size:13px}
.rank-table th{padding:10px 14px;text-align:left;color:rgba(255,255,255,0.4);font-size:11px;text-transform:uppercase;letter-spacing:1px;border-bottom:1px solid rgba(255,255,255,0.08)}
.rank-table td{padding:12px 14px;border-bottom:1px solid rgba(255,255,255,0.05)}
.rank-table tr:hover td{background:rgba(255,255,255,0.03)}
.badge{padding:4px 10px;border-radius:20px;font-size:11px;font-weight:600}
.badge.strong{background:rgba(52,211,153,0.2);color:#34d399}
.badge.moderate{background:rgba(251,191,36,0.2);color:#fbbf24}
.badge.low{background:rgba(248,113,113,0.2);color:#f87171}

/* SCORE BAR */
.bar-bg{background:rgba(255,255,255,0.08);border-radius:6px;height:8px;width:120px}
.bar{height:8px;border-radius:6px}

/* DETAIL */
.detail-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}
.detail-box{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:14px;font-size:12px;line-height:1.7;color:rgba(255,255,255,0.7)}
.detail-box h4{font-size:11px;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:1px;margin-bottom:8px}
.tip-box{background:rgba(167,139,250,0.1);border-left:3px solid #a78bfa;border-radius:0 10px 10px 0;padding:14px;font-size:12px;line-height:1.8;color:rgba(255,255,255,0.8);margin-top:14px;white-space:pre-wrap}

/* HISTORY */
.history-table{width:100%;border-collapse:collapse;font-size:12px}
.history-table th{padding:8px 12px;color:rgba(255,255,255,0.4);font-size:11px;text-transform:uppercase;letter-spacing:1px;text-align:left;border-bottom:1px solid rgba(255,255,255,0.08)}
.history-table td{padding:10px 12px;border-bottom:1px solid rgba(255,255,255,0.05);color:rgba(255,255,255,0.7)}

/* CHART */
.chart-wrap{max-width:500px;margin:0 auto}

/* SECTION ANCHOR */
.section-title{font-size:11px;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:2px;margin:28px 0 14px}
</style>
</head>
<body>
<div class="app">

  <!-- SIDEBAR -->
  <div class="sidebar">
    <div class="logo">🤖 <span>AI</span>Screen</div>
    <a class="nav-item" href="#upload">
      <div class="nav-dot" style="background:#a78bfa"></div> Upload
    </a>
    <a class="nav-item" href="#rankings">
      <div class="nav-dot" style="background:#34d399"></div> Rankings
    </a>
    <a class="nav-item" href="#chart">
      <div class="nav-dot" style="background:#60a5fa"></div> Chart
    </a>
    <a class="nav-item" href="#details">
      <div class="nav-dot" style="background:#fbbf24"></div> Details
    </a>
    <a class="nav-item" href="#history">
      <div class="nav-dot" style="background:#f87171"></div> History
    </a>
  </div>

  <!-- MAIN CONTENT -->
  <div class="main">
    <div class="topbar">
      <div>
        <h1>Resume Screener Dashboard</h1>
        <p>Powered by NLP + Generative AI</p>
      </div>
    </div>

    <!-- STATS -->
    {% if results %}
    <div class="stats">
      <div class="stat">
        <div class="stat-label">Resumes Screened</div>
        <div class="stat-value">{{ results|length }}<small>total</small></div>
      </div>
      <div class="stat">
        <div class="stat-label">Top Score</div>
        <div class="stat-value">{{ results[0].score }}%<small>↑</small></div>
      </div>
      <div class="stat">
        <div class="stat-label">Avg Match</div>
        <div class="stat-value">
          {{ ((results|sum(attribute='score')) / results|length)|round(1) }}%
        </div>
      </div>
    </div>
    {% endif %}

    <!-- UPLOAD FORM -->
    <div class="glass" id="upload">
      <h2>📤 Upload Resumes + Job Description</h2>
      <form method="POST" enctype="multipart/form-data">
        <div class="upload-zone">
          <strong>Drop PDF Resumes Here</strong>
          Select up to 5 resumes at once
          <br>
          <input type="file" name="resumes" accept=".pdf" multiple required>
        </div>
        <label>Paste Job Description:</label>
        <textarea name="job_description"
          placeholder="Paste the job description here...">{{ jd }}</textarea>
        <button class="btn" type="submit">🔍 Screen All Resumes</button>
      </form>
    </div>

    {% if results %}

    <!-- RANKINGS -->
    <div class="section-title" id="rankings">🏆 Candidate Rankings</div>
    <div class="glass">
      <h2>Ranked by AI Match Score</h2>
      <table class="rank-table">
        <tr>
          <th>Rank</th><th>Resume</th><th>Score</th>
          <th>Match Bar</th><th>Verdict</th>
        </tr>
        {% for r in results %}
        <tr>
          <td><b style="color:#a78bfa">#{{ loop.index }}</b></td>
          <td style="color:#fff">{{ r.name }}</td>
          <td><b>{{ r.score }}%</b></td>
          <td>
            <div class="bar-bg">
              <div class="bar" style="width:{{ r.score }}%;
                background:{{ '#34d399' if r.score>=70 else '#fbbf24' if r.score>=50 else '#f87171' }}">
              </div>
            </div>
          </td>
          <td>
            <span class="badge {{ 'strong' if r.score>=70 else 'moderate' if r.score>=50 else 'low' }}">
              {{ 'Strong' if r.score>=70 else 'Moderate' if r.score>=50 else 'Low' }}
            </span>
          </td>
        </tr>
        {% endfor %}
      </table>
    </div>

    <!-- CHART -->
    <div class="section-title" id="chart">📊 Score Comparison</div>
    <div class="glass">
      <h2>Visual Score Comparison</h2>
      <div class="chart-wrap">
        <canvas id="scoreChart"></canvas>
      </div>
    </div>

    <!-- DETAILS + TIPS -->
    <div class="section-title" id="details">📄 Detailed Analysis</div>
    {% for r in results %}
    <div class="glass">
      <h2>{{ r.name }} — {{ r.score }}%
        <span class="badge {{ 'strong' if r.score>=70 else 'moderate' if r.score>=50 else 'low' }}"
          style="margin-left:10px">
          {{ 'Strong Match' if r.score>=70 else 'Moderate Match' if r.score>=50 else 'Low Match' }}
        </span>
      </h2>
      <div class="detail-grid">
        <div class="detail-box">
          <h4>Skills Found</h4>
          {{ r.skills }}
        </div>
        <div class="detail-box">
          <h4>AI Assessment</h4>
          {{ r.explanation }}
        </div>
      </div>
      <div class="tip-box">
        💡 Improvement Tips:
{{ r.tips }}
      </div>
    </div>
    {% endfor %}

    <!-- HISTORY -->
    <div class="section-title" id="history">🕒 Screening History</div>
    <div class="glass">
      <h2>Past Screenings</h2>
      <table class="history-table">
        <tr>
          <th>Date</th><th>Resume</th>
          <th>Score</th><th>Verdict</th>
        </tr>
        {% for h in history %}
        <tr>
          <td>{{ h[6] }}</td>
          <td>{{ h[1] }}</td>
          <td><b style="color:#a78bfa">{{ h[2] }}%</b></td>
          <td>
            <span class="badge {{ 'strong' if h[2]>=70 else 'moderate' if h[2]>=50 else 'low' }}">
              {{ h[3] }}
            </span>
          </td>
        </tr>
        {% endfor %}
      </table>
    </div>

    {% endif %}
  </div>
</div>

{% if results %}
<script>
const ctx = document.getElementById('scoreChart').getContext('2d');
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: {{ labels|tojson }},
    datasets:[{
      label: 'Match Score (%)',
      data: {{ scores|tojson }},
      backgroundColor: {{ colors|tojson }},
      borderRadius: 8,
    }]
  },
  options:{
    responsive:true,
    plugins:{legend:{display:false}},
    scales:{
      y:{
        beginAtZero:true,max:100,
        ticks:{color:'rgba(255,255,255,0.5)',callback:v=>v+'%'},
        grid:{color:'rgba(255,255,255,0.05)'}
      },
      x:{
        ticks:{color:'rgba(255,255,255,0.5)'},
        grid:{color:'rgba(255,255,255,0.05)'}
      }
    }
  }
});
</script>
{% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def index():
    init_db()
    history = get_history()
    if request.method == "POST":
        files = request.files.getlist("resumes")
        jd    = request.form["job_description"]
        results = []
        for file in files:
            if file.filename == "": continue
            path = f"temp_{file.filename}"
            file.save(path)
            resume_text = parse_resume(path)
            keywords    = extract_keywords(resume_text)
            score       = match_resume_to_job(resume_text, jd)
            explanation = explain_match(resume_text, jd, score, keywords)
            client      = Groq(api_key=GROQ_API_KEY)
            tip_res     = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role":"user","content":f"""
Give 3 practical improvement tips for this resume.
Plain text only. No ** or markdown.
Skills: {keywords['skills']}
Score: {score}%
JD: {jd}"""}])
            tips    = tip_res.choices[0].message.content
            verdict = "Strong Match" if score>=70 else "Moderate Match" if score>=50 else "Low Match"
            save_to_db(file.filename, score, verdict,
                       ", ".join(keywords["skills"]), explanation)
            results.append({
                "name": file.filename, "score": score,
                "verdict": verdict,
                "skills": ", ".join(keywords["skills"]),
                "explanation": explanation, "tips": tips
            })
            os.remove(path)
        results = sorted(results, key=lambda x: x["score"], reverse=True)
        labels  = [r["name"] for r in results]
        scores  = [r["score"] for r in results]
        colors  = ["rgba(52,211,153,0.8)" if s>=70
                   else "rgba(251,191,36,0.8)" if s>=50
                   else "rgba(248,113,113,0.8)" for s in scores]
        return render_template_string(HTML,
            results=results, history=get_history(),
            labels=labels, scores=scores,
            colors=colors, jd=jd)
    return render_template_string(HTML,
        results=None, history=history, jd="")

if __name__ == "__main__":
    print("🚀 AI Resume Screener — Glassmorphism Dashboard")
    print("👉 Open: http://localhost:5000")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)