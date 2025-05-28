# 🛡️ Job Scam Detector 🔍

**Job Scam Detector** is an intelligent tool that helps users analyze job listings and detect potential scams using a combination of rule-based scraping and AI-powered language analysis. Users simply input a job listing URL, and the app provides a **scam verdict**, **trust score**, and a list of red flags, all in seconds.

---

## ✨ Features

- ✅ Analyze job URLs and detect potential scam patterns
- 🧠 Uses a language model (LLM) to explain why a job might be fake
- 📉 Generates a **Trust Score** (0–100) for each listing
- 📌 Lists detailed **Reasoning** and **Suggestions** for the user
- 🧩 Built with a FastAPI backend and a clean frontend interface
- 🌐 Can be used as a **web app** or **Chrome extension**

---

## 🛠️ Tech Stack

| Layer        | Technology             |
|--------------|------------------------|
| Frontend     | HTML, CSS, Vanilla JS  |
| Backend      | Python, FastAPI        |
| Web Scraping | BeautifulSoup          |
| AI Analysis  | Google Gemini API (or LLM of choice) |
| Deployment   | Works on localhost or cloud server |
| Extension    | Chrome Extension Support |

---

## 🚀 How It Works

1. **User** inputs a job listing URL.
2. The **backend** scrapes relevant text (e.g., job title, description).
3. The text is passed to an **AI model**, which evaluates:
   - Language patterns
   - Red flags (e.g., free internships, vague roles)
   - Email domain credibility
   - Domain WHOIS data (optional)
4. The response includes:
   - **Scam Verdict** (Yes / No)
   - **Trust Score**
   - **Reasoning**
   - **Suggestions**

---

## 📦 Installation

### 1. Clone the Repo

```bash
git clone https://github.com/Ankit0200/Scam_jobs_detector.git
cd job-scam-detector
