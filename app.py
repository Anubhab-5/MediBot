import streamlit as st
import google.generativeai as genai
import re
import os
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key="AIzaSyDYUmwXVoy1OXV7cnt5oDovGw3E7b6kYjc")
model = genai.GenerativeModel('gemini-1.5-flash')


def clean_input(text):
    return re.sub(r'[^\w\s]', '', text).strip() if text else ""


def get_career_advice(qualification, question,):
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
        return f"Error: Unable to fetch advice ({str(e)}). Check your internet or API key."


st.set_page_config(page_title="MediBot", page_icon="🩺", layout="centered")
st.markdown("""
    <style>
    .main {background-color: #ffff; padding: 20px; border-radius: 12px;}
    .stButton>button {background-color: #0055b3; color: white; border-radius: 10px; padding: 10px; font-weight: bold;}
    .stButton>button:hover {background-color: #003d82;}
    .stTextInput>div>input {border: 2px solid #0055b3; border-radius: 10px; padding: 8px;}
    h1 {color: #001f5c; text-align: center; font-size: 36px;}
    .stSpinner {text-align: center;}
    .response-box {background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);}
    </style>
""", unsafe_allow_html=True)

st.title("MediBot 🩺")
st.markdown("***Find all your answers..***")


if 'history' not in st.session_state:
    st.session_state.history = []


with st.form("student_form"):
    qualification = st.text_input("Qualification: ", placeholder="Enter your education background")
    question = st.text_input("Question: ", placeholder="Enter your question")
    submit = st.form_submit_button("Get Answer")


if submit:
    if not all([qualification, question]):
        st.error("Please fill all fields to continue.")
    else:
        qualification = clean_input(qualification)
        question = clean_input(question)

       
        st.subheader("Your Profile")
        st.markdown(f"- **Qualification**: {qualification}")
        st.markdown(f"- **Question**: {question}")

        
        with st.spinner("Finding your answers..."):
            answer = get_career_advice(qualification, question)
            st.markdown("<div class='response-box'>", unsafe_allow_html=True)
            st.markdown(answer, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        
        st.session_state.history.append({
            "inputs": {"qualification": qualification, "question": question},
            "answer": answer
        })


if st.session_state.history:
    st.subheader("Your Answers")
    for i, entry in enumerate(st.session_state.history):
        with st.expander(f"Answer {i+1}, {question}"):
            st.markdown(f"- **Qualification**: {entry['inputs']['qualification']}")
            st.markdown(f"- **Question**: {entry['inputs']['question']}")
            st.markdown(entry['answer'], unsafe_allow_html=True)
