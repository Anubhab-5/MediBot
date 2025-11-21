import streamlit as st
import time
import google.generativeai as genai
import re
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key="AIzaSyAeDa9dpAF0GL91jxdYXapoNZIJ1Vab6mE")
model = genai.GenerativeModel('gemini-2.5-flash')

def clean_input(text):
    """Preserve medical punctuation while cleaning input"""
    if not text:
        return ""
    return re.sub(r'[^\w\s\-\'?]', '', text).strip()

@st.cache_data(show_spinner=False, ttl=3600)
def get_cached_advice(_model, qualification, question):
    return get_career_advice(qualification, question)

def get_career_advice(qualification, question):
    prompt = f"""
    You are an expert Doctor and professor mentoring and answering a {qualification} medical student's question. Provide high quality answer to this question: "{question}"

    Answering criteria:
    - Use the format of answering, which is required for the asked question for detailed explanation.
    - You have to provide high quality and in detailed explanation answer of the question, The answer should be in simple words which is easy to understand for a medical student.
    - Always each points of the answer should be informative and in-depth explanation.
    - Always do research on existing medical knowledge or studies from top medical journals and textbooks, to provide the best answer, and ensure the answer is accurate and reliable.
    - Always each points and sub-points should be detailed explained, which helps the student to know and understand everything about that topic in depth.
    - Always provide examples or case studies to illustrate your points, which helps the student to understand the topic better.
    - Format with clear headings(##) and bullet points for readability.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"## ⚠️ Service Error\nPlease check your internet connection. Technical details: {str(e)}"

# App Configuration
st.set_page_config(
    page_title="MediBot",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Simple Clean CSS
st.markdown("""
<style>
    /* Simple Reset */
    .main {
        background: #ffffff;
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Header */
    .header {
        text-align: center;
        padding: 2rem 1rem 1rem;
        background: white;
        border-radius: 8px;
    }
    
    .title {
        font-size: 50px;
        font-weight: 700;
        color: #000B80;
        margin-bottom: 0.2rem;
    }
    
    .subtitle {
        font-size: 20px;
        color: #FF0000;
        font-weight: 700;
        margin-bottom: 0.1rem;
    }
    
    /* Simple Stats */
    .stats {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 1rem 0;
        font-size: 18px;
        font-weight: 600;
        color: #0015FF;
    }
    
    .stat {
        text-align: center;
    }
    
    .stat-value {
        font-weight: 700;
        color: #0015FF;
    }
    
    /* Input Section */
    .input-section {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #e5e7eb;
    }
    
    .section-title {
        font-size: 30px;
        font-weight: 700;
        text-align: center;
        color: #000B80;
    }
    
    /* Form Elements */
    .input-label {
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #FFFFFF;
        display: block;
    }
    
    .stTextInput>div>div>input {
        border-radius: 8px !important;
        
        padding: 0.75rem !important;
        font-size: 16px !important;
    }
    
    .stTextArea>div>textarea {
        border-radius: 8px !important;
        
        padding: 0.75rem !important;
        font-size: 16px !important;
        min-height: 100px !important;
    }
    
    .stTextInput>div>div>input:focus, 
    .stTextArea>div>textarea:focus {
        border-color: 2px solid #2563eb !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1) !important;
    }
    
    /* Button */
    .stButton>button {
        background: #2563eb !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        margin-top: 1rem !important;
    }
    
    .stButton>button:hover {
        background: #1d4ed8 !important;
    }
    
    /* Response Section */
    .response-section {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #2563eb;
    }
    
    .response-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
        color: #000B80;
    }
    
    .response-meta {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #e5e7eb;
        font-size: 0.9rem;
        color: #666;
        display: flex;
        gap: 1rem;
    }
    
    /* History Section */
    .history-section {
        margin: 2rem 0 1rem;
    }
    
    .history-item {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.75rem;
        border: 1px solid #e5e7eb;
    }
    
    .history-question {
        font-weight: 500;
        margin-bottom: 0.5rem;
        color: #374151;
    }
    
    .history-info {
        display: flex;
        justify-content: space-between;
        font-size: 0.8rem;
        color: #6b7280;
    }
    
    .history-badge {
        background: #dbeafe;
        color: #1e40af;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
    }
    
    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 2rem;
        color: #9ca3af;
        font-style: italic;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 2rem;
        padding: 1rem;
        color: #6b7280;
        font-size: 0.9rem;
        border-top: 1px solid #e5e7eb;
    }
    
    /* Mobile Optimizations */
    @media (max-width: 768px) {
        .header {
            padding: 1.5rem 1rem 0.5rem;
        }
        
        .title { 
        font-size: 40px;
        font-weight: 800;
        color: #000B80;
        margin-bottom: 0.2rem;
        }
        
        .input-section {
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .stats {
            gap: 1.5rem;
            font-size: 0.85rem;
        }
        
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'history' not in st.session_state:
    st.session_state.history = []
if 'last_question' not in st.session_state:
    st.session_state.last_question = ""
if 'total_queries' not in st.session_state:
    st.session_state.total_queries = 0

# Simple Header
st.markdown("""
<div class="header">
    <div class="title">🩺 MediBot</div>
    <div class="subtitle">AI Medical Assistant</div>
    <div class="stats">
        <div class="stat">
            <div class="stat-value">{}</div>
            <div>Queries</div>
        </div>
        <div class="stat">
            <div class="stat-value">{}</div>
            <div>Specialties</div>
        </div>
        <div class="stat">
            <div class="stat-value">{}</div>
            <div>Total</div>
        </div>
    </div>
</div>
""".format(
    len(st.session_state.history),
    len(set([h['inputs']['qualification'] for h in st.session_state.history])),
    st.session_state.total_queries
), unsafe_allow_html=True)

# Main Content Container
container = st.container()

with container:
    # Input Section
    st.markdown("""
    <div class="input-section">
        <div class="section-title ">Ask a Medical Questions</div>
    """, unsafe_allow_html=True)
    
    with st.form("medical_query"):
        # Qualification Input
        st.markdown('<div class="input-label">Your Educational Background📖</div>', unsafe_allow_html=True)
        qualification = st.text_input(
            "Qualification",
            placeholder="E.g., MBBS Student, Nursing, Medical Resident...",
            label_visibility="collapsed"
        )
        
        # Question Input
        st.markdown('<div class="input-label">Your Question❔</div>', unsafe_allow_html=True)
        question = st.text_area(
            "Question",
            placeholder="Ask your medical question here...",
            label_visibility="collapsed",
            height=120
        )
        
        # Submit Button
        submit_button = st.form_submit_button("Get Answer😊", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Handle Form Submission
    if submit_button:
        if not qualification or not question:
            st.error("Please fill in both fields")
        else:
            cleaned_qualification = clean_input(qualification)
            cleaned_question = clean_input(question)
            
            # Check for duplicate
            if cleaned_question == st.session_state.last_question:
                st.info("Showing cached response")
            else:
                st.session_state.last_question = cleaned_question
                st.session_state.total_queries += 1
            
            # Generate Response
            with st.spinner("Generating answer..."):
                start_time = time.time()
                answer = get_cached_advice(model, cleaned_qualification, cleaned_question)
                response_time = time.time() - start_time
                
                # Display Response
                st.markdown("""
                    <div class="response-section">
                        <div class="response-header">
                            <strong>👨‍⚕️ Expert's Answer</strong>
                        </div>
                """, unsafe_allow_html=True)
                
                st.markdown(answer)
                
                st.markdown("""
                        <div class="response-meta">
                            <div>Generated in {:.1f}s</div>
                            <div>{} words</div>
                            <div>For: {}</div>
                        </div>
                    </div>
                """.format(response_time, len(answer.split()), cleaned_qualification), unsafe_allow_html=True)
                
                # Add to History
                st.session_state.history.append({
                    "inputs": {
                        "qualification": cleaned_qualification,
                        "question": cleaned_question
                    },
                    "answer": answer,
                    "timestamp": time.time(),
                    "response_time": response_time,
                    "date": datetime.now().strftime("%H:%M")
                })
    
    # History Section
    st.markdown("""
    <div class="history-section">
        <div class="section-title" style="color: white;">Recent Questions🙋‍♀️</div>
    """, unsafe_allow_html=True)
    
    if st.session_state.history:
        for i, entry in enumerate(reversed(st.session_state.history[:6])):
            question_preview = entry['inputs']['question']
            if len(question_preview) > 80:
                question_preview = question_preview[:80] + '...'
            
            st.markdown(f"""
                <div class="history-item">
                    <div class="history-question">{question_preview}</div>
                    <div class="history-info">
                        <div class="history-badge">{entry['inputs']['qualification']}</div>
                        <div>{entry['date']} • {entry['response_time']:.1f}s</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="empty-state">
                No questions yet. Ask your first question above.
            </div>
        """, unsafe_allow_html=True)
    
    # Clear History Button
    if st.session_state.history:
        if st.button("Clear History", use_container_width=True):
            st.session_state.history = []
            st.session_state.last_question = ""
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# Simple Footer
st.markdown("""
<div class="footer">
    <div>MediBot • Medical Education Assistant</div>
    <div style="margin-top: 0.5rem; font-size: 0.8rem;">
        Made by Anubhab • Consult professionals for medical decisions
    </div>
</div>
""", unsafe_allow_html=True)