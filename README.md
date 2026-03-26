# 💼 AI Resume Analyzer

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=flat-square&logo=streamlit)
![NLP](https://img.shields.io/badge/NLP-TF--IDF-purple?style=flat-square)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange?style=flat-square)

An intelligent **Resume Analyzer** that uses NLP to extract skills, calculate ATS compatibility scores, and match resumes to job descriptions using TF-IDF cosine similarity.

## 🚀 Features

- 🔍 **Skill Extraction**: Auto-detects skills across 6 categories (Python, AI/ML, Data, Web, Cloud, NLP)
- 📊 **ATS Score**: Scores your resume on ATS compatibility (0-100) with detailed feedback
- 🎯 **Job Matching**: Matches your resume to 5 job roles using TF-IDF cosine similarity
- 💡 **Improvement Tips**: Actionable feedback for each ATS check
- 📤 **PDF Support**: Works with any PDF resume

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| NLP | TF-IDF, Cosine Similarity |
| ML Library | scikit-learn |
| PDF Parsing | PyPDF2 |
| Text Processing | regex, Python stdlib |

## 📸 Screenshots

### Skills Tab - Categorized skill detection
### ATS Score Tab - Detailed compatibility report  
### Job Match Tab - Role similarity scores

## 💻 Installation

```bash
git clone https://github.com/Arawn-D/ai-resume-analyzer.git
cd ai-resume-analyzer
pip install -r requirements.txt
streamlit run app.py
```

## 🏃 Usage

1. Upload your PDF resume in the sidebar
2. Browse **Skills** tab to see detected technologies
3. Check **ATS Score** for compatibility rating + feedback
4. See **Job Match** to find best-fit roles

## 📊 ATS Scoring Criteria

| Check | Points |
|-------|--------|
| Resume Length (300+ words) | 20 |
| Email Address | 15 |
| Phone Number | 10 |
| Education Section | 10 |
| Experience Section | 10 |
| Skills Section | 10 |
| Projects Section | 10 |
| Action Verbs (3+) | 15 |

## 💡 Key Concepts Demonstrated

- **TF-IDF Vectorization**: Text feature extraction for job matching
- **Cosine Similarity**: Measuring semantic closeness between documents
- **NLP Preprocessing**: Text cleaning, keyword extraction
- **Streamlit Multi-tab UI**: Professional app layout

## 👨‍💻 Author

**Vijay Dokka** - Python Developer | AI/ML Engineer
- GitHub: [@Arawn-D](https://github.com/Arawn-D)
- Email: helloaavijay@gmail.com

---

> Built with ❤️ using scikit-learn + Streamlit
