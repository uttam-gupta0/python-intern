import re
import fitz  # PyMuPDF
from docx import Document
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Regex patterns
EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
PHONE_REGEXES = [
    r'(\+?\d{1,3}[\s-])?\d{10}',
    r'\(\d{3}\)\s*\d{3}[-.\s]\d{4}',
    r'\d{3}[-.\s]\d{3}[-.\s]\d{4}',
]

# Example skill list (you can expand)
SKILLS = [
    "python", "java", "c", "c++", "javascript", "sql", "html", "css",
    "pandas", "numpy", "machine learning", "deep learning", "nlp",
    "flask", "django", "react", "git", "docker", "aws", "matplotlib"
]


def read_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def read_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])


def preprocess_text(text):
    text = text.replace('\r', '\n')
    text = re.sub(r'\n\s+\n', '\n\n', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)
    return text.strip()


def extract_email(text):
    m = re.search(EMAIL_REGEX, text)
    return m.group(0) if m else None


def extract_phone(text):
    found = []
    for pat in PHONE_REGEXES:
        found.extend(re.findall(pat, text))
    phones = []
    for f in found:
        if isinstance(f, tuple):
            phones.append("".join(f))
        else:
            phones.append(f)
    phones = list({re.sub(r'\D', '', p) for p in phones if len(re.sub(r'\D', '', p)) >= 7})
    return phones[0] if phones else None


def extract_name(text):
    doc = nlp(text)
    lines = text.splitlines()
    top_text = "\n".join(lines[:8])
    doc_top = nlp(top_text)
    persons = [ent.text.strip() for ent in doc_top.ents if ent.label_ == "PERSON"]
    if persons:
        return persons[0]
    persons = [ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON"]
    return persons[0] if persons else None


def extract_skills(text, skills_list=SKILLS):
    text_lower = text.lower()
    found = set()
    for s in skills_list:
        if s.lower() in text_lower:
            found.add(s)
    return sorted(found)


def extract_education(text):
    edu_lines = []
    edu_keywords = [
        "b.tech", "b.e", "bachelor", "m.tech", "m.e", "master",
        "msc", "mba", "ph.d", "phd", "bsc", "mca", "bca"
    ]
    for line in text.splitlines():
        l = line.lower()
        if any(k in l for k in edu_keywords):
            edu_lines.append(line.strip())
    return edu_lines


def extract_experience(text):
    lowered = text.lower()
    if "experience" in lowered:
        parts = re.split(r'\n+', text)
        start = None
        for i, p in enumerate(parts):
            if "experience" in p.lower():
                start = i
                break
        if start is not None:
            block = parts[start + 1:start + 9]
            return "\n".join([b.strip() for b in block if b.strip()])
    ranges = re.findall(r'\b(20\d{2})\s*[-–]\s*(Present|20\d{2})\b', text)
    return ranges[:5] or None


def parse_resume(path):
    if path.lower().endswith(".pdf"):
        txt = read_pdf(path)
    elif path.lower().endswith(".docx"):
        txt = read_docx(path)
    else:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            txt = f.read()

    txt = preprocess_text(txt)
    return {
        "name": extract_name(txt),
        "email": extract_email(txt),
        "phone": extract_phone(txt),
        "skills": extract_skills(txt),
        "education": extract_education(txt),
        "experience": extract_experience(txt),
    }


if __name__ == "__main__":
    import sys, json
    if len(sys.argv) < 2:
        print("Usage: python parser.py <resume_file>")
    else:
        res = parse_resume(sys.argv[1])
        print(json.dumps(res, indent=2))
