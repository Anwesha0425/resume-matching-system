import os
import docx2txt
import PyPDF2
from sentence_transformers import SentenceTransformer, util
import spacy
import json
from taxonomy import SKILLS_TAXONOMY

# Load the SentenceTransformer model
# all-MiniLM-L6-v2 provides a great balance of speed and performance for semantic search
print("Loading SentenceTransformer model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded successfully.")

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + " "
    except Exception as e:
        print(f"Error extracting PDF: {e}")
    return text

def extract_text_from_docx(file_path):
    try:
        return docx2txt.process(file_path)
    except Exception as e:
        print(f"Error extracting DOCX: {e}")
        return ""

def extract_text_from_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error extracting TXT: {e}")
        return ""

def extract_text(file_path):
    file_path_lower = file_path.lower()
    if file_path_lower.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path_lower.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path_lower.endswith('.txt'):
        return extract_text_from_txt(file_path)
    else:
        return ""

def get_similarity_scores(job_description, resumes_text):
    """
    Computes semantic similarity scores between a job description and a list of resumes.
    Returns a list of float scores.
    """
    if not job_description or not resumes_text:
        return []
        
    # Generate embeddings
    job_embedding = model.encode(job_description, convert_to_tensor=True)
    resume_embeddings = model.encode(resumes_text, convert_to_tensor=True)
    
    # Calculate cosine similarity
    cosine_scores = util.cos_sim(job_embedding, resume_embeddings)[0]
    
    # Return as list of floats
    return cosine_scores.tolist()

# Try to load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Fallback if model not downloaded yet
    nlp = None

def extract_skills_from_text(text):
    if nlp is None:
        return set()
    doc = nlp(text.lower())
    skills = set()
    for token in doc:
        # Extract meaningul nouns and cross-reference with strict taxonomy
        if token.pos_ in ['PROPN', 'NOUN', 'X'] and len(token.text) > 1:
            if token.text in SKILLS_TAXONOMY:
                skills.add(token.text)
                
    # Also check for multi-word skills in taxonomy (e.g., 'machine learning')
    text_lower = text.lower()
    for skill in SKILLS_TAXONOMY:
        if " " in skill and skill in text_lower:
            skills.add(skill)
            
    return skills

from rag_pipeline import generate_resume_insights

def analyze_resume_with_llm(job_description, resume_text):
    """
    Uses the Gemini LLM via LangChain to extract skills and provide matching reasoning.
    """
    return generate_resume_insights(job_description, resume_text)
