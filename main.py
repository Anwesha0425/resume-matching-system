from flask import Flask, request, render_template
import os
import numpy as np
from utils import extract_text, get_similarity_scores

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route("/")
def matchresume():
    return render_template('matchresume.html')

@app.route('/matcher', methods=['POST'])
def matcher():
    if request.method == 'POST':
        job_description = request.form.get('job_description', '')
        resume_files = request.files.getlist('resumes')

        resumes_text = []
        valid_resume_files = []
        
        # Make sure uploads directory exists
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        for resume_file in resume_files:
            if resume_file.filename == '':
                continue
            filename = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
            resume_file.save(filename)
            resumes_text.append(extract_text(filename))
            valid_resume_files.append(resume_file)

        if not resumes_text or not job_description.strip():
            return render_template('matchresume.html', message="Please upload resumes and enter a job description.")

        # Calculate semantic similarities using SentenceTransformers
        similarity_scores = get_similarity_scores(job_description, resumes_text)

        # Get top resumes and their similarity scores
        similarities = np.array(similarity_scores)
        # Sort indices in descending order
        top_indices = similarities.argsort()[-5:][::-1]
        
        top_resumes = [valid_resume_files[i].filename for i in top_indices]
        
        # Convert similarities to percentages (0 to 100)
        similarity_percentages = [round(min(100.0, max(0.0, similarities[i] * 100)), 1) for i in top_indices]

        return render_template('matchresume.html', 
                               message="Top Matching Candidates", 
                               top_resumes=top_resumes, 
                               similarity_scores=similarity_percentages)

    return render_template('matchresume.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True, port=5000)
