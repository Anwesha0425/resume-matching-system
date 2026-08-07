---
title: Resume Matching System
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Resume Matching System 🚀

An advanced, AI-powered Resume Matching System built to seamlessly match candidate resumes against job descriptions. It utilizes **Semantic Vector Search**, an **embedded SQLite database**, and a **Retrieval-Augmented Generation (RAG)** pipeline powered by Google Gemini to analyze candidates and answer natural language questions about your talent pool.

## Key Features ✨

* **Retrieval-Augmented Generation (RAG):** Built with `LangChain` and `FAISS` to dynamically vectorize your candidate pool. You can use the built-in Chat UI to ask natural language questions (e.g., "Who has 3 years of React experience?").
* **AI-Powered Insights:** Employs the `Google Gemini` LLM to evaluate top candidates against the job description, automatically extracting matching skills, missing skills, and generating human-readable reasoning for the match.
* **Semantic Matching:** Uses Hugging Face's `SentenceTransformers` (`all-MiniLM-L6-v2`) to perform deep contextual matching and initial ranking between job descriptions and resumes.
* **Embedded Database:** Uses `SQLite` to automatically save every uploaded resume. You can search through thousands of past candidates instantly without needing to re-upload files.

## Tech Stack 🛠️

* **Backend Framework:** Python Flask
* **AI & LLM Integration:** LangChain, Google Gemini API
* **Vector Store:** FAISS
* **Semantic Search Engine:** `SentenceTransformers` (PyTorch)
* **NLP & Extraction:** `spaCy`
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

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your Gemini API Key:
   ```env
   GEMINI_API_KEY=your_google_gemini_api_key_here
   ```

5. **Run the Application:**
   ```bash
   python main.py
   ```
   *The SQLite database (`candidates.db`) will be automatically created on the first run.*

6. **Access the Web Interface:**
   Open your browser and navigate to: `http://127.0.0.1:5000`

## Usage Workflow 📈

1. **Add Candidates:** Upload PDF, DOCX, or TXT resumes. The system will parse the text and save them permanently to the database.
2. **Search Database:** Paste a Job Description into the text area. The system will semantically rank all candidates in your database and display the top 5 matches, along with AI-generated reasoning from Gemini.
3. **Chat with Candidate Pool:** Use the chat box at the bottom of the screen to ask dynamic questions about the candidates in your database using the RAG pipeline.

## License 📄
This project is open-source and available under the MIT License.
