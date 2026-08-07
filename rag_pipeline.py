import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.chains import LLMChain

# Make sure GEMINI_API_KEY is available in the environment before this is called
def get_llm():
    # We use gemini-1.5-flash as it is fast and efficient for these tasks
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

def get_embeddings():
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def generate_resume_insights(job_description, resume_text):
    """
    Uses Gemini LLM to analyze the resume against the job description.
    Returns a dictionary with extracted_skills, missing_skills, and match_reasoning.
    """
    llm = get_llm()
    
    prompt = PromptTemplate.from_template("""
    You are an expert technical recruiter. You are evaluating a candidate's resume against a job description.
    
    Job Description:
    {job_description}
    
    Candidate Resume:
    {resume_text}
    
    Analyze the resume against the job description and output ONLY a valid JSON object with the following structure:
    {{
        "extracted_skills": ["List of up to 10 key skills the candidate possesses that are relevant to the job"],
        "missing_skills": ["List of up to 8 key skills mentioned in the job description that the candidate lacks"],
        "match_reasoning": "A short, 2-3 sentence paragraph explaining why this candidate is or isn't a good fit based on the skills."
    }}
    
    Output strictly JSON, without any markdown formatting blocks like ```json.
    """)
    
    chain = prompt | llm
    
    try:
        response = chain.invoke({"job_description": job_description, "resume_text": resume_text})
        response_text = response.content.strip()
        # Clean up in case the LLM wrapped it in markdown anyway
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        return json.loads(response_text)
    except Exception as e:
        print(f"Error generating insights with LLM: {e}")
        return {
            "extracted_skills": [],
            "missing_skills": [],
            "match_reasoning": f"Error communicating with LLM: {str(e)}"
        }

def ask_candidates_question(query, candidates):
    """
    Builds a FAISS vector store from the candidates and performs a RAG query to answer the user's question.
    """
    if not candidates:
        return "No candidates available in the database to search."
        
    try:
        # Create LangChain Documents
        documents = []
        for c in candidates:
            # We append the filename to the content so the LLM knows who the resume belongs to
            content = f"Candidate Name/Filename: {c['filename']}\n\nResume Content:\n{c['content']}"
            metadata = {"filename": c['filename'], "id": c['id']}
            documents.append(Document(page_content=content, metadata=metadata))
            
        # Initialize embeddings
        embeddings = get_embeddings()
        
        # Create FAISS vector store on the fly
        vectorstore = FAISS.from_documents(documents, embeddings)
        
        # Retrieve the most relevant documents (e.g., top 3)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        relevant_docs = retriever.invoke(query)
        
        # Construct context for the LLM
        context = "\n\n---\n\n".join([doc.page_content for doc in relevant_docs])
        
        llm = get_llm()
        
        prompt = PromptTemplate.from_template("""
        You are an HR Assistant helping a recruiter find the best candidates.
        Use the following extracted resume contexts to answer the recruiter's question. 
        Always mention the candidate's name (filename) when discussing their qualifications.
        If the answer is not in the context, just say that you cannot find the answer based on the current candidates.
        
        Context (Relevant Resumes):
        {context}
        
        Recruiter's Question:
        {query}
        
        Answer:
        """)
        
        chain = prompt | llm
        response = chain.invoke({"context": context, "query": query})
        
        return response.content
        
    except Exception as e:
        print(f"Error during RAG pipeline execution: {e}")
        return f"Sorry, an error occurred while searching the candidates: {str(e)}"
