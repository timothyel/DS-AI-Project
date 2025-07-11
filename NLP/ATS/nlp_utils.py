import re
import nltk
from nltk.tokenize import sent_tokenize
import spacy
from sentence_transformers import SentenceTransformer, util

# Load spaCy model untuk ekstraksi keyword
nlp_spacy = spacy.load("en_core_web_sm")

# Load pre-trained lightweight BERT model untuk semantic similarity
model_bert = SentenceTransformer("all-MiniLM-L6-v2")

def extract_keywords(text):
    """
    Ekstrak keyword dari CV/JD menggunakan noun chunks dari spaCy.
    Cocok untuk mendeteksi kata kunci seperti skill, role, tools.
    """
    doc = nlp_spacy(text)
    keywords = [chunk.text.lower() for chunk in doc.noun_chunks]
    return list(set(keywords))

def split_responsibilities_flexibly(text):
    """
    Pisahkan teks menjadi poin-poin berdasarkan:
    - Bullet point (•, -, *, ●)
    - Numbering (1., 2), dll
    - Kalimat panjang jika tidak terstruktur
    """
    lines = text.splitlines()
    points = []

    for line in lines:
        line = line.strip()

        if re.match(r"^(\d+[\.\)]|[-*•●])\s+", line) and len(line) > 5:
            points.append(line)
        elif len(line) > 40:
            points.extend(sent_tokenize(line))
        elif len(line) > 10:
            points.append(line)

    return [p.strip() for p in points if len(p.strip()) > 5]

def compute_similarity(cv_text, jd_text):
    """
    Hitung similarity antara full CV dan full JD.
    """
    cv_embedding = model_bert.encode(cv_text, convert_to_tensor=True)
    jd_embedding = model_bert.encode(jd_text, convert_to_tensor=True)
    score = util.cos_sim(cv_embedding, jd_embedding).item()
    return round(score * 100, 2)

def compute_similarity_per_point(cv_text, jd_text):
    """
    Hitung similarity antara setiap poin CV dengan JD.
    """
    points = split_responsibilities_flexibly(cv_text)
    jd_embedding = model_bert.encode(jd_text, convert_to_tensor=True)

    results = []
    for p in points:
        point_embedding = model_bert.encode(p, convert_to_tensor=True)
        score = util.cos_sim(point_embedding, jd_embedding).item()
        results.append((p, round(score * 100, 2)))

    return sorted(results, key=lambda x: -x[1])
