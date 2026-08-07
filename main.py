from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
load_dotenv()

import numpy as np
from utils import extract_text, get_similarity_scores, analyze_resume_with_llm, extract_skills_from_text
from db import init_db, add_candidate, get_all_candidates
from rag_pipeline import ask_candidates_question

app = Flask(__name__, template_folder='.')
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize DB on startup
init_db()

@app.route("/")
def matchresume():
    return render_template('matchresume.html')

@app.route('/matcher', methods=['POST'])
def matcher():
    if request.method == 'POST':
        job_description = request.form.get('job_description', '')
        resume_files = request.files.getlist('resumes')

        # 1. Process any NEW uploaded resumes and save to DB
        for file in resume_files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Extract text
                text = extract_text(filepath)
                
                # Extract skills and save to DB
                skills = extract_skills_from_text(text)
                add_candidate(filename, text, skills)
                
                # Clean up the file to save disk space on ephemeral cloud storage
                try:
                    os.remove(filepath)
                except Exception as e:
                    print(f"Error removing file {filepath}: {e}")

        # 2. Fetch ALL candidates from the database
        all_candidates = get_all_candidates()
        
        if not all_candidates:
            return render_template('matchresume.html', message="No candidates in database and no new files uploaded.")

        # Prepare lists for scoring
        resumes_text = [c['content'] for c in all_candidates]
        filenames = [c['filename'] for c in all_candidates]

        # 3. Calculate semantic similarity scores against ALL candidates
        similarity_scores = get_similarity_scores(job_description, resumes_text)

        # Get top resumes and their similarity scores
        similarities = np.array(similarity_scores)
        # Sort indices in descending order
        top_indices = similarities.argsort()[-5:][::-1]
        
        top_resumes = [filenames[i] for i in top_indices]
        top_resumes_text = [resumes_text[i] for i in top_indices]
        
        # Convert similarities to percentages (0 to 100)
        similarity_percentages = [round(min(100.0, max(0.0, similarities[i] * 100)), 1) for i in top_indices]

        # Fetch AI Insights for top candidates
        ai_insights = []
        for i in range(len(top_resumes)):
            # Only analyze top 3 to save time/tokens if there are many
            if i < 3:
                insight = analyze_resume_with_llm(job_description, top_resumes_text[i])
            else:
                insight = {"error": "Skipped LLM analysis (only top 3)"}
            ai_insights.append(insight)

        return render_template('matchresume.html', 
                               message="Top Matching Candidates", 
                               top_resumes=top_resumes, 
                               similarity_scores=similarity_percentages,
                               ai_insights=ai_insights)

    return render_template('matchresume.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return {"answer": "Please ask a valid question."}
        
    all_candidates = get_all_candidates()
    answer = ask_candidates_question(query, all_candidates)
    
    return {"answer": answer}

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True, port=5000)
