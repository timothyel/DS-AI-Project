import re

# === NLTK Setup ===
import subprocess
import sys

# Paksa install nltk jika belum tersedia
try:
    import nltk
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "nltk"])
    import nltk

# Pastikan resource tokenizer 'punkt' tersedia
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# === spaCy Setup ===
# Load model bahasa Inggris untuk ekstraksi keyword
import spacy
nlp_spacy = spacy.load("en_core_web_sm")

# === BERT Model ===
# Gunakan pre-trained SentenceTransformer untuk similarity scoring
from sentence_transformers import SentenceTransformer, util
model_bert = SentenceTransformer("all-MiniLM-L6-v2")
# Download data NLTK untuk tokenizing kalimat (sekali saja)
nltk.download("punkt")

# Load spaCy untuk ekstraksi keyword
nlp_spacy = spacy.load("en_core_web_sm")

# Load pre-trained BERT model untuk semantic similarity
model_bert = SentenceTransformer("all-MiniLM-L6-v2")

def extract_keywords(text):
    """
    Ekstrak keyword dari CV/JD menggunakan noun chunks dari spaCy.
    Cocok untuk mendeteksi kata kunci seperti skill, role, tools.
    """
    doc = nlp_spacy(text)
    keywords = [chunk.text.lower() for chunk in doc.noun_chunks]
    return list(set(keywords))  # hapus duplikat

def split_responsibilities_flexibly(text):
    """
    Pisahkan teks menjadi poin-poin berdasarkan:
    - Bullet point (•, -, *, ●)
    - Numbering (1., 2), dll
    - Kalimat panjang (>40 karakter) jika tidak terstruktur
    """
    lines = text.splitlines()
    points = []

    for line in lines:
        line = line.strip()

        # Deteksi bullet atau numbering
        if re.match(r"^(\d+[\.\)]|[-*•●])\s+", line) and len(line) > 5:
            points.append(line)

        # Jika kalimat panjang tanpa bullet, pecah jadi kalimat
        elif len(line) > 40:
            points.extend(sent_tokenize(line))

        # Tangkap baris pendek tapi relevan
        elif len(line) > 10:
            points.append(line)

    # Bersihkan & filter
    return [p.strip() for p in points if len(p.strip()) > 5]

def compute_similarity(cv_text, jd_text):
    """
    Hitung similarity antara full CV dan full JD sebagai baseline.
    """
    cv_embedding = model_bert.encode(cv_text, convert_to_tensor=True)
    jd_embedding = model_bert.encode(jd_text, convert_to_tensor=True)

    score = util.cos_sim(cv_embedding, jd_embedding).item()
    return round(score * 100, 2)  # nilai dalam persen

def compute_similarity_per_point(cv_text, jd_text):
    """
    Hitung similarity antara setiap poin CV dengan JD.
    Tujuannya adalah analisis granular per bullet point.
    """
    points = split_responsibilities_flexibly(cv_text)
    jd_embedding = model_bert.encode(jd_text, convert_to_tensor=True)

    results = []
    for p in points:
        point_embedding = model_bert.encode(p, convert_to_tensor=True)
        score = util.cos_sim(point_embedding, jd_embedding).item()
        results.append((p, round(score * 100, 2)))

    # Urutkan berdasarkan skor tertinggi
    return sorted(results, key=lambda x: -x[1])
