import streamlit as st
import PyPDF2
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="💼",
    layout="wide"
)

# --- Skill database ---
SKILL_KEYWORDS = {
    "Programming Languages": ["python", "java", "c++", "javascript", "typescript", "go", "rust", "scala", "r", "kotlin"],
    "AI/ML": ["machine learning", "deep learning", "nlp", "computer vision", "pytorch", "tensorflow", "keras", "scikit-learn", "transformers", "llm", "rag", "embeddings", "fine-tuning"],
    "Data": ["sql", "pandas", "numpy", "data preprocessing", "dbms", "data analysis", "spark"],
    "Web/APIs": ["flask", "fastapi", "django", "streamlit", "rest api", "html", "css", "react"],
    "Cloud & DevOps": ["aws", "gcp", "azure", "docker", "kubernetes", "ci/cd", "git"],
    "NLP Specific": ["spacy", "nltk", "bert", "gpt", "huggingface", "text classification", "sentiment analysis", "ner"]
}

JOB_DESCRIPTIONS = {
    "ML Engineer": "machine learning deep learning python pytorch tensorflow scikit-learn model deployment mlops feature engineering data pipeline cloud aws",
    "NLP Engineer": "nlp natural language processing transformers bert gpt huggingface text classification ner sentiment analysis python spacy nltk",
    "AI Engineer": "llm rag embeddings fine-tuning langchain prompt engineering python api deployment openai huggingface",
    "Data Scientist": "python r sql data analysis machine learning statistics pandas numpy visualization tableau",
    "Backend Developer": "python flask fastapi django rest api sql docker kubernetes microservices"
}


def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def extract_skills(text):
    text_lower = text.lower()
    found_skills = {}
    for category, skills in SKILL_KEYWORDS.items():
        found = [skill for skill in skills if skill in text_lower]
        if found:
            found_skills[category] = found
    return found_skills


def calculate_ats_score(text):
    score = 0
    feedback = []

    # Check length
    word_count = len(text.split())
    if word_count > 200:
        score += 20
        feedback.append(("OK", f"Good length: {word_count} words"))
    else:
        feedback.append(("WARN", f"Resume too short: {word_count} words. Aim for 300+"))

    # Check contact info
    if re.search(r'[\w.]+@[\w.]+', text):
        score += 15
        feedback.append(("OK", "Email address found"))
    else:
        feedback.append(("FAIL", "No email address detected"))

    if re.search(r'\+?[0-9]{10,}', text):
        score += 10
        feedback.append(("OK", "Phone number found"))
    else:
        feedback.append(("FAIL", "No phone number detected"))

    # Check sections
    sections = ["education", "experience", "skills", "project"]
    for section in sections:
        if section in text.lower():
            score += 10
            feedback.append(("OK", f"Section '{section.title()}' found"))
        else:
            feedback.append(("WARN", f"Missing section: {section.title()}"))

    # Check action verbs
    action_verbs = ["built", "developed", "implemented", "designed", "led", "improved", "achieved"]
    found_verbs = [v for v in action_verbs if v in text.lower()]
    if len(found_verbs) >= 3:
        score += 15
        feedback.append(("OK", f"Good use of action verbs: {', '.join(found_verbs)}"))
    else:
        feedback.append(("WARN", "Add more action verbs (built, developed, implemented, etc.)"))

    return min(score, 100), feedback


def match_jobs(resume_text):
    results = {}
    vectorizer = TfidfVectorizer(stop_words='english')
    all_texts = [resume_text] + list(JOB_DESCRIPTIONS.values())
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    resume_vec = tfidf_matrix[0]
    for i, (job_title, _) in enumerate(JOB_DESCRIPTIONS.items()):
        similarity = cosine_similarity(resume_vec, tfidf_matrix[i + 1])[0][0]
        results[job_title] = round(similarity * 100, 2)
    return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))


# --- UI ---
st.title("💼 AI Resume Analyzer")
st.markdown("**NLP-powered Resume Analysis | ATS Score | Job Matching**")

with st.sidebar:
    st.header("Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF Resume", type="pdf")
    st.markdown("---")
    st.markdown("### Features")
    st.markdown("""
    - 🔍 Skill Extraction
    - 📊 ATS Compatibility Score
    - 🎯 Job Role Matching
    - 💡 Improvement Tips
    """)
    st.markdown("---")
    st.markdown("Built by **Vijay Dokka** | [GitHub](https://github.com/Arawn-D)")

if uploaded_file:
    with st.spinner("Analyzing resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    tab1, tab2, tab3 = st.tabs(["🔍 Skills", "📊 ATS Score", "🎯 Job Match"])

    with tab1:
        st.subheader("Detected Skills")
        skills = extract_skills(resume_text)
        if skills:
            for category, skill_list in skills.items():
                st.markdown(f"**{category}**")
                cols = st.columns(4)
                for i, skill in enumerate(skill_list):
                    cols[i % 4].success(skill.title())
        else:
            st.warning("No matching skills found. Make sure to include relevant keywords.")

    with tab2:
        st.subheader("ATS Compatibility Score")
        score, feedback = calculate_ats_score(resume_text)
        col1, col2 = st.columns([1, 2])
        with col1:
            color = "normal" if score >= 70 else "inverse"
            st.metric("ATS Score", f"{score}/100", delta=f"{'Good' if score >= 70 else 'Needs Work'}")
            st.progress(score / 100)
        with col2:
            st.markdown("### Feedback")
            for status, msg in feedback:
                if status == "OK":
                    st.success(msg)
                elif status == "WARN":
                    st.warning(msg)
                else:
                    st.error(msg)

    with tab3:
        st.subheader("Job Role Match Analysis")
        matches = match_jobs(resume_text)
        for job, score in matches.items():
            col1, col2 = st.columns([2, 3])
            col1.markdown(f"**{job}**")
            col2.progress(min(score / 100, 1.0), text=f"{score}% match")
else:
    st.info("👆 Upload your PDF resume from the sidebar to get started!")
