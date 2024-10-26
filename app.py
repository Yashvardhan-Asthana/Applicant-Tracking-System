
from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
import PyPDF2  # Using PyPDF2 to extract text from PDF
import google.generativeai as genai

load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv("API_KEY")

# Configure Google API with the provided key
genai.configure(api_key=api_key)

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model
    response = model.generate_content([input, pdf_content, prompt])  # Send strings
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the PDF and extract text
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text() + "\n"  # Concatenate text from each page
        return pdf_text.strip()  # Return cleaned text
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage match")

input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. 
Give me the percentage of match if the resume matches the job description. 
First the output should come as percentage, then keywords missing, and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)  # Extracted text from PDF
        response = get_gemini_response(input_prompt1, pdf_content, input_text)  # Use text
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)  # Extracted text from PDF
        response = get_gemini_response(input_prompt3, pdf_content, input_text)  # Use text
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
