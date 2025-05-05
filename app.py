from dotenv import load_dotenv

load_dotenv()
import base64
from gtts import gTTS
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai
from pdf2image import convert_from_bytes


# Text-to-Speech function
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    audio_file = "response.mp3"
    tts.save(audio_file)
    return audio_file

# Load environment variables from .env file
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_cotent,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path='/opt/homebrew/bin')
       
        # Save the first page as an image
        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

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
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""
input_prompt2 = """
Create a tailored resume for the following job description. Highlight the most relevant experience, skills, and achievements that align with the role. The resume should be concise, professional, and use action-oriented bullet points.
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
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
         # Add audio player
        audio_file = text_to_speech(response)
        st.audio(audio_file)
    else:
        st.write("Please uplaod the resume")
        
if submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
       
    else:
        st.write("Please uplaod the resume")