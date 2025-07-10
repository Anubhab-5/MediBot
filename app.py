import streamlit as st
import google.generativeai as genai
import re
import os
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key="AIzaSyAlSxCxVXHOnGCT4nHftjBiCFAo46DM1iM")
model = genai.GenerativeModel('gemini-1.5-flash')


def clean_input(text):
    """Preserve medical punctuation while cleaning input"""
    if not text:
        return ""
    # Allow hyphens, apostrophes, and question marks
    return re.sub(r'[^\w\s\-\'?]', '', text).strip()

# Cache responses to avoid duplicate API calls
@st.cache_data(show_spinner=False, ttl=3600)
def get_cached_advice(_model, qualification, question):
    return get_career_advice(qualification, question)

def get_career_advice(qualification, question):
    """Original prompt preserved"""
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

# UI Configuration
st.set_page_config(
    page_title="MediBot",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for responsive design
st.markdown("""
    <style>
    /* Main container */
    .main {padding: 2rem 1rem; max-width: 1200px; margin: 0 auto;}
    
    /* Header styling */
    .header {text-align: center; padding: 1rem 0 2rem;}
    .title {color: #1a73e8; font-size: 2.5rem; margin-bottom: 0.5rem;}
    .subtitle {color: #BAECFF; font-size: 1.2rem;}
    
    /* Form styling */
    .form-container {background: white; border-radius: 12px; padding: 2rem; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 2rem;}
    .input-label {font-weight: 600; margin-bottom: 0.5rem; color: #FFFFFF;}
    .input-field {border: 1px solid #dadce0 !important; border-radius: 8px !important; padding: 12px !important;}
    .input-field:focus {border-color: #1a73e8 !important; box-shadow: 0 0 0 2px #e8f0fe;}
    .submit-btn {background: #1a73e8 !important; color: white !important; border: none !important; border-radius: 8px !important; padding: 12px 24px !important; font-weight: 600 !important; width: 100%; transition: all 0.3s;}
    .submit-btn:hover {background: #1557b0 !important; transform: translateY(-2px); box-shadow: 0 4px 8px rgba(26,115,232,0.25);}
    .submit-btn:active {transform: translateY(0);}
    
    /* Response styling */
    .response-header {display: flex; align-items: center; margin-bottom: 1rem;}
    .response-box {background: white; border-radius: 12px; padding: 2rem; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-left: 4px solid #1a73e8;}
    .response-content {line-height: 1.6;}
    
    /* History styling */
    .history-card {background: white; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 2px 6px rgba(0,0,0,0.05); border-left: 3px solid #1a73e8; transition: all 0.3s;}
    .history-card:hover {transform: translateY(-3px); box-shadow: 0 4px 12px rgba(0,0,0,0.1);}
    .history-question {font-weight: 600; margin-bottom: 0.5rem; color: #202124;}
    .history-qualification {color: #5f6368; font-size: 0.9rem;}
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main {padding: 1rem;}
        .form-container {padding: 1.5rem;}
        .title {font-size: 2rem;}
    }
    @media (max-width: 480px) {
        .title {font-size: 1.8rem;}
        .subtitle {font-size: 1rem;}
    }
    
    /* Utility classes */
    .spinner {color: #1a73e8 !important;}
    .divider {border-top: 1px solid #e8eaed; margin: 2rem 0;}
    .footer {text-align: center; margin-top: 2rem; color: #BAECFF; font-size: 0.9rem;}
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown("""
    <div class="header">
        <h1 class="title">MediBot 🩺</h1>
        <p class="subtitle">AI-powered medical education assistant</p>
    </div>
""", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'last_question' not in st.session_state:
    st.session_state.last_question = ""

# Main content container
with st.container():
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        # History Section
        st.subheader("Recent Queries")
        if st.session_state.history:
            for i, entry in enumerate(reversed(st.session_state.history[:5])):
                with st.container():
                    st.markdown(f"""
                        <div class="history-card">
                            <div class="history-question">{entry['inputs']['question'][:60]}{'...' if len(entry['inputs']['question']) > 60 else ''}</div>
                            <div class="history-qualification">{entry['inputs']['qualification']}</div>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Your recent questions will appear here")
            
        # Clear history button
        if st.session_state.history and st.button("Clear History", use_container_width=True):
            st.session_state.history = []
            st.session_state.last_question = ""
            st.rerun()
            
    
    with col2:
        # Input Form
        with st.form("student_form", border=False):
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            
            st.markdown('<div class="input-label">Your Educational Level📖</div>', unsafe_allow_html=True)
            qualification = st.text_input(
                "Qualification", 
                placeholder="Eg: 3rd Year MBBS, Nursing, Phisio, etc",
                label_visibility="collapsed"
            )
            
            st.markdown('<div class="input-label">Your Question❓</div>', unsafe_allow_html=True)
            question = st.text_area(
                "Question", 
                placeholder="Feel free to ask any type of medical question...",
                label_visibility="collapsed",
                height=120
            )
            
            submit = st.form_submit_button("Get Answer✨", type="primary", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Handle form submission
        if submit:
            if not qualification or not question:
                st.error("Please fill in both fields")
            else:
                cleaned_qualification = clean_input(qualification)
                cleaned_question = clean_input(question)
                
                # Prevent duplicate queries
                if cleaned_question == st.session_state.last_question:
                    st.warning("Same as previous question. Showing cached response.")
                else:
                    st.session_state.last_question = cleaned_question
                
                # Display response
                with st.spinner("Researching medical literature..."):
                    start_time = time.time()
                    answer = get_cached_advice(model, cleaned_qualification, cleaned_question)
                    response_time = time.time() - start_time
                    
                    st.markdown("""
                        <div class="response-box">
                            <div class="response-header">
                                <h3>Expert Answer</h3>
                            </div>
                            <div class="response-content">
                    """, unsafe_allow_html=True)
                    
                    st.markdown(answer, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                            </div>
                            <div style="margin-top: 1.5rem; color: #5f6368; font-size: 0.9rem;">
                                Generated in {response_time:.1f}s
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Add to history
                    st.session_state.history.append({
                        "inputs": {
                            "qualification": cleaned_qualification,
                            "question": cleaned_question
                        },
                        "answer": answer
                    })

    # Footer
    st.markdown("""
        <div class="footer">
            <hr style="margin: 2rem 0; border: 0; border-top: 1px solid #eee;">
            <p>MediBot v1.5 | AI-powered medical education assistant</p>
            <p><small>Made with ❤️ by Anubhab</small></p>
        </div>
    """, unsafe_allow_html=True)
