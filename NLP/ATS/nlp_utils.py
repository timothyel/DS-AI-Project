import re
import nltk
import spacy
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer, util
from datetime import datetime

# Download resource NLTK jika belum tersedia
nltk.download('punkt')

# Load spaCy model (untuk ekstraksi keyword)
nlp_spacy = spacy.load("en_core_web_sm")

# Load lightweight BERT model (untuk semantic similarity)
model_bert = SentenceTransformer("all-MiniLM-L6-v2")


def extract_keywords(text):
    """
    Ekstrak keyword dari noun chunks (frase benda) dalam teks.
    Digunakan untuk mendeteksi skill, tools, dan role.
    """
    doc = nlp_spacy(text)
    return list(set(chunk.text.lower() for chunk in doc.noun_chunks))


def split_responsibilities_flexibly(text):
    """
    Pisahkan teks menjadi poin-poin tanggung jawab dari CV.
    Deteksi berdasarkan bullet points, numbering, atau kalimat panjang.
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


def compute_similarity(text_a, text_b):
    """
    Hitung cosine similarity antara dua teks (misal: CV vs JD).
    Return skor dalam bentuk persentase.
    """
    emb_a = model_bert.encode(text_a, convert_to_tensor=True)
    emb_b = model_bert.encode(text_b, convert_to_tensor=True)
    return round(util.cos_sim(emb_a, emb_b).item() * 100, 2)


def compute_similarity_per_point(cv_text, jd_text):
    """
    Hitung similarity setiap poin dari CV terhadap JD.
    Berguna untuk granular analysis per kalimat/tanggung jawab.
    """
    points = split_responsibilities_flexibly(cv_text)
    jd_embedding = model_bert.encode(jd_text, convert_to_tensor=True)

    results = []
    for point in points:
        point_emb = model_bert.encode(point, convert_to_tensor=True)
        score = util.cos_sim(point_emb, jd_embedding).item()
        results.append((point, round(score * 100, 2)))

    return sorted(results, key=lambda x: -x[1])


def estimate_years_of_experience(text):
    """
    Estimasi total pengalaman kerja (dalam tahun) dari rentang tanggal di CV.
    Format yang dideteksi:
    - Jan 2020 - Mar 2023
    - 2019 - 2021
    - 2020 - Present
    """
    patterns = [
        r'(\w{3,9})\s(\d{4})\s*[-–]\s*(\w{3,9})\s(\d{4}|present|Present)',
        r'(\d{4})\s*[-–]\s*(\d{4}|present|Present)'
    ]

    total_months = 0
    for pattern in patterns:
        for match in re.findall(pattern, text):
            try:
                start = convert_to_date(match[0], match[1])
                end = convert_to_date(match[2], match[3]) if len(match) == 4 else convert_to_date(match[1])
                if start and end:
                    months = (end.year - start.year) * 12 + (end.month - start.month)
                    total_months += max(0, months)
            except:
                continue

    return round(total_months / 12, 1)


def convert_to_date(month_or_year, year=None):
    """
    Konversi teks ke objek datetime.
    Bisa menangani format: "Jan 2020", "March 2022", "2020", dan "Present"
    """
    try:
        if year is None:
            return datetime(int(month_or_year), 1, 1)
        elif "present" in year.lower():
            return datetime.now()
        else:
            try:
                return datetime.strptime(f"{month_or_year} {year}", "%b %Y")
            except:
                return datetime.strptime(f"{month_or_year} {year}", "%B %Y")
    except:
        return None


def detect_required_experience(jd_text):
    """
    Deteksi minimum tahun pengalaman dari teks JD.
    Contoh yang dideteksi:
    - "2+ years of experience"
    - "at least 3 years"
    - "minimal 5 tahun pengalaman"
    """
    match = re.search(
        r'(\d{1,2})\s*(\+?\s*years?|tahun)[\w\s]*(experience|pengalaman)?',
        jd_text, re.IGNORECASE
    )
    if match:
        return int(match.group(1))
    return None
