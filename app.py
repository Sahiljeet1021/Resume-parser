from dotenv import load_dotenv
load_dotenv()
import streamlit as st 
import os 
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Page configuration with custom theme
st.set_page_config(
    page_title="ATS Resume Expert 🎯",
    page_icon="📄",
    layout="wide"
)

# Custom CSS for styling with improved text visibility
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Fix text color for all elements */
    .stMarkdown, .stTextArea label, .stFileUploader label, p, span, div {
        color: #2d3748 !important;
    }
    
    /* Header styling */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #1a202c !important;
    }
    
    .big-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: fadeIn 1s ease-in;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #4a5568 !important;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    /* Upload section styling */
    .upload-section {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .upload-section h3 {
        color: #2d3748 !important;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        background-color: #f7fafc !important;
        color: #2d3748 !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #a0aec0 !important;
    }
    
    /* File uploader styling */
    .stFileUploader {
        background-color: #f7fafc;
        padding: 1rem;
        border-radius: 8px;
        border: 2px dashed #cbd5e0;
    }
    
    .stFileUploader label {
        color: #2d3748 !important;
        font-weight: 600 !important;
    }
    
    .success-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
        margin: 1rem 0;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideIn {
        from { transform: translateX(-100%); }
        to { transform: translateX(0); }
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Info card styling */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .info-card h4 {
        color: #2d3748 !important;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .info-card p {
        color: #4a5568 !important;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* Response text styling */
    .element-container p {
        color: #2d3748 !important;
    }
    
    /* Spinner text */
    .stSpinner > div {
        color: #667eea !important;
    }
    
    /* Error message */
    .stAlert {
        background-color: #fff5f5 !important;
        color: #c53030 !important;
        border-left: 4px solid #fc8181 !important;
    }
    
    /* Horizontal rule */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #cbd5e0, transparent);
    }
    </style>
""", unsafe_allow_html=True)

# Header with emoji and gradient
st.markdown('<h1 class="big-title">🎯 ATS Resume Expert</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">✨ Optimize your resume and land your dream job with AI-powered insights ✨</p>', unsafe_allow_html=True)

# Create two columns for better layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("### 📝 Job Description")
    input_text = st.text_area(
        "",
        placeholder="Paste the job description here...",
        height=200,
        key="input",
        help="Copy and paste the complete job description from the job posting"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("### 📄 Upload Your Resume")
    uploaded_file = st.file_uploader(
        "",
        type=["pdf"],
        help="Upload your resume in PDF format"
    )
    
    if uploaded_file is not None:
        st.markdown(
            '<div class="success-message">✅ Resume uploaded successfully! Ready for analysis.</div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

# Information cards
st.markdown("---")
st.markdown("### 🚀 Choose Your Analysis")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("#### 👤 Professional Resume Review")
    st.markdown("Get expert HR feedback on your resume's alignment with the job requirements")
    submit1 = st.button("🔍 Analyze Resume", key="btn1")
    st.markdown('</div>', unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("#### 📊 ATS Match Score")
    st.markdown("See your ATS compatibility score and get keyword recommendations")
    submit3 = st.button("📈 Get Match Score", key="btn3")
    st.markdown('</div>', unsafe_allow_html=True)

# Prompts
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First the output should come as percentage, then keywords missing, and last final thoughts.
"""

# Handle button clicks
if submit1:
    if uploaded_file is not None and input_text:
        with st.spinner('🔄 Analyzing your resume... Please wait!'):
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt1, pdf_content, input_text)
            st.markdown("---")
            st.markdown("### 📋 Professional Review Results")
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.write(response)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("⚠️ Please upload your resume and enter a job description to continue!")

elif submit3:
    if uploaded_file is not None and input_text:
        with st.spinner('🔄 Calculating your ATS match score... Please wait!'):
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt3, pdf_content, input_text)
            st.markdown("---")
            st.markdown("### 🎯 ATS Match Score Results")
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.write(response)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("⚠️ Please upload your resume and enter a job description to continue!")

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #718096; font-size: 0.9rem;">💡 Tip: Make sure your resume is in PDF format and the job description is complete for best results!</p>',
    unsafe_allow_html=True
)
