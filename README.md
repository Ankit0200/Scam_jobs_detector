# Scam_jobs_detector
# 🚫 Scam Jobs Detector

**Scam Jobs Detector** is an intelligent tool built with FastAPI that helps users identify and avoid scam or fake job listings. It uses rule-based heuristics, domain analysis (via WHOIS), email checks (MX records), and optionally integrates AI to analyze job descriptions and flag suspicious ones.

---

## 🔍 Features

- ✅ Analyze job listings and descriptions for scam signals
- 🌐 Verify domains with WHOIS and MX record checks
- 🤖 Optionally uses AI (e.g., Google Gemini) to interpret language patterns
- 🛡 Trust score and scam verdict with detailed reasoning
- 🧪 RESTful API built with FastAPI
- 🧰 Frontend integration ready (React/Vue/etc.)

---

## 🏗 Tech Stack

- **Backend**: FastAPI (Python)
- **AI/NLP**: Google Gemini (optional)
- **Data Sources**: WHOIS API, DNS/MX records
- **Frontend**: HTML, CSS, JS , 

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Ankit0200/Scam_jobs_detector
cd Scam_jobs_detector

**Sample output **

{
  "Scam_Verdict": "Yes",
  "Trust_Score": 25,
  "Reasoning": [
    "Generic job titles used",
    "Suspicious Gmail contact",
    "Domain age is too new",
    "No clear compensation or program structure"
  ]
}
