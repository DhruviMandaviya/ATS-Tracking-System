from dotenv import load_dotenv

load_dotenv()

import base64
from gtts import gTTS
import streamlit as st
import os
import io
from PIL import Image 
import google.generativeai as genai
import fitz  # PyMuPDF

def extract_text_from_pdf(uploaded_file):
    if uploaded_file is not None:
        pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        full_text = ""
        for page in pdf_doc:
            full_text += page.get_text()
        return full_text
    else:
        raise FileNotFoundError("No file uploaded")

# Text-to-Speech function
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    audio_file = "response.mp3"
    tts.save(audio_file)
    return audio_file

# Load environment variables from .env file
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_text, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_text, prompt])
    return response.text


## Streamlit App
st.set_page_config(page_title="ATS Resume EXpert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("Tailor the Resume")

submit3 = st.button("Percentage match")

input_prompt1 = """
you are an exprinced HR manager with deep tech exprince in the field of any one role from Data analyst, Mobile application developer, android Application developer,
iOS Application developer, Fluter developer, React native developer and deep ATS functionality.
your task is to evaluate the resume against the provided job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""
input_prompt2 = """
you are an exprinced HR manager with deep tech exprince in the field of any one role from Data analyst, Mobile application developer, android Application developer,
iOS Application developer, Fluter developer, React native developer and deep ATS functionality.
your task is to evaluate the resume against the provided job description.
Based on your analysis Create a tailored resume for the following job description. 
Highlight the most relevant experience, skills, and achievements that align with the role. The resume should be concise, professional, and use action-oriented bullet points.
Candidate Information:get the candidate information from the resume
Job Description:get the job description from the input text

"""
input_prompt3 = """
you are an exprinced HR manager with deep tech exprince in the field of any one role from Data analyst, Mobile application developer, android Application developer,
iOS Application developer, Fluter developer, React native developer and deep ATS functionality.
your task is to evaluate the resume against the provided job description. 
give me the percentage of match if the resume matches the job description. 
Also provide me a suggetion of strong project with strong keywords that are realted to project and missing in the resume.
Give me tailored resume for the following job description. Highlight the most relevant experience, skills, and achievements that align with the role. 
The resume should be concise, professional, and use action-oriented bullet points.
First the output should come as percentage and then keywords missing, tailored resume and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_text, input_text)
        st.subheader("The Response is")
        st.write(response)

        audio_file = text_to_speech(response)
        st.audio(audio_file)
    else:
        st.write("Please upload the resume")


if submit2:
    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_text, input_text)
        st.subheader("The Response is")
        st.write(response)

        audio_file = text_to_speech(response)
        st.audio(audio_file)
    else:
        st.write("Please upload the resume")
        
if submit3:
    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_text, input_text)
        st.subheader("The Response is")
        st.write(response)

        audio_file = text_to_speech(response)
        st.audio(audio_file)
    else:
        st.write("Please upload the resume")

