---
title: Resume Matching System
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Resume Matching System 🚀

An advanced, machine-learning-powered Resume Matching System built to seamlessly match candidate resumes against job descriptions. It utilizes a **local NLP pipeline**, **semantic vector search**, and an **embedded SQLite database** to ensure 100% offline functionality, data privacy, and zero API costs.

## Key Features ✨

* **Semantic Matching:** Uses Hugging Face's `SentenceTransformers` (`all-MiniLM-L6-v2`) to perform deep contextual matching between job descriptions and resumes, going beyond simple keyword matching.
* **Intelligent Skill Extraction:** Employs `spaCy` combined with a strict, custom **Skill Taxonomy** (100+ industry-standard tech & soft skills) to guarantee accurate skill extraction while ignoring hallucinated noise.
* **Embedded Database:** Uses `SQLite` to automatically save every uploaded resume and its extracted skills. You can search through thousands of past candidates instantly without needing to re-upload files.
* **Fully Local & Offline:** No external API keys (OpenAI, Gemini, etc.) required. The NLP models run entirely on your local machine, ensuring strict data privacy and zero usage limits.

## Tech Stack 🛠️

* **Backend Framework:** Python Flask
* **NLP & Extraction:** `spaCy` (en_core_web_sm)
* **Semantic Search Engine:** `SentenceTransformers` (PyTorch)
* **Database:** SQLite
* **Document Parsing:** `PyPDF2` (PDFs), `docx2txt` (Word Docs)
* **Frontend:** HTML5, Vanilla CSS

## Setup & Installation ⚙️

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Anwesha0425/resume-matching-system.git
   cd resume-matching-system
   ```

2. **Install dependencies:**
   It is highly recommended to use a virtual environment.
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the local spaCy AI model:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Run the Application:**
   ```bash
   python main.py
   ```
   *The SQLite database (`candidates.db`) will be automatically created on the first run.*

5. **Access the Web Interface:**
   Open your browser and navigate to: `http://127.0.0.1:5000`

## Usage Workflow 📈

1. **Add Candidates:** Upload PDF, DOCX, or TXT resumes. The system will automatically parse the text, extract their skills, and save them permanently to the database.
2. **Search Database:** Paste a Job Description into the text area. You do *not* need to upload files again. The system will semantically rank all candidates in your database and display the top 5 matches.
3. **Review Results:** See percentage-based match scores along with exactly which skills the candidate possesses and which ones they are missing for the role.

## License 📄
This project is open-source and available under the MIT License.
