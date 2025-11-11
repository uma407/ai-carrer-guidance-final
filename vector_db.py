"""
Simple, robust vector DB abstraction with two modes:
- Preferred: sentence-transformers + FAISS (if installed)
- Fallback: scikit-learn TfidfVectorizer + cosine similarity (no heavy deps)

Provides:
- populate_sample_data(): loads demo resources
- query_vector_db(query, top_k=5): returns list of text matches
- add_documents(docs): add docs to the in-memory DB
"""
from typing import List
import os

# Try preferred libraries first
TRY_SENTE = True
try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    HAS_SENTE = True
except Exception:
    HAS_SENTE = False

try:
    import faiss
    HAS_FAISS = True
except Exception:
    HAS_FAISS = False

# Fallback to scikit-learn
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SKLEARN = True
except Exception:
    HAS_SKLEARN = False

# In-memory store
_DOCS: List[str] = []
_EMBEDDINGS = None
_VECTOR_MODEL = None
_TFIDF_VECT = None


def _ensure_vectorizer():
    global _VECTOR_MODEL, _TFIDF_VECT, _EMBEDDINGS
    if HAS_SENTE:
        if _VECTOR_MODEL is None:
            _VECTOR_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
            # compute embeddings if docs exist
            if _DOCS:
                _EMBEDDINGS = _VECTOR_MODEL.encode(_DOCS, convert_to_numpy=True)
    elif HAS_SKLEARN:
        if _TFIDF_VECT is None:
            _TFIDF_VECT = TfidfVectorizer(stop_words='english')
            if _DOCS:
                _EMBEDDINGS = _TFIDF_VECT.fit_transform(_DOCS)
    else:
        # very lightweight fallback: store docs only and return naive substring matches
        pass


def add_documents(docs: List[str]):
    """Add documents to the in-memory store and update embeddings/index."""
    global _DOCS, _EMBEDDINGS, _VECTOR_MODEL, _TFIDF_VECT
    docs = [d for d in docs if d]
    if not docs:
        return
    _DOCS.extend(docs)
    # Recompute embeddings/index
    if HAS_SENTE:
        if _VECTOR_MODEL is None:
            _VECTOR_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
        _EMBEDDINGS = _VECTOR_MODEL.encode(_DOCS, convert_to_numpy=True)
    elif HAS_SKLEARN:
        if _TFIDF_VECT is None:
            _TFIDF_VECT = TfidfVectorizer(stop_words='english')
        _EMBEDDINGS = _TFIDF_VECT.fit_transform(_DOCS)


def populate_sample_data():
    """Populate demo documents used by the frontend and tests."""
    sample_docs = [
        "Intro to Python: Learn programming basics and data structures.",
        "Statistics for Data Science: Descriptive stats, probability, and inference.",
        "Machine Learning Foundations: Supervised learning, evaluation, and feature engineering.",
        "Deep Learning Specialization: Neural networks, CNNs, RNNs.",
        "Career Tips: How to write a resume, prepare for interviews, and build a portfolio.",
        "Cloud Computing Basics: AWS, Azure, GCP fundamentals and deployment.",
        "Data Engineering: ETL pipelines, databases, and scalable systems.",
        "Research & Publications: How to prepare a research paper and publish findings.",
        "Project-based learning: Build real-world applications and showcase them in a portfolio.",
    ]
    add_documents(sample_docs)


def query_vector_db(query: str, top_k: int = 5) -> List[str]:
    """Return up to top_k matching documents (strings). Works in fallback modes.

    If real embedding libs (sentence-transformers + faiss/sklearn) exist, use them.
    Otherwise perform naive substring matching.
    """
    query = (query or "").strip()
    if not query:
        return []

    # If sentence-transformers available
    if HAS_SENTE and _EMBEDDINGS is not None:
        q_emb = _VECTOR_MODEL.encode([query], convert_to_numpy=True)
        # cosine similarity
        from numpy import dot
        from numpy.linalg import norm
        sims = np.dot(_EMBEDDINGS, q_emb.T).squeeze() / (
            (np.linalg.norm(_EMBEDDINGS, axis=1) * np.linalg.norm(q_emb)) + 1e-10
        )
        idx = sims.argsort()[::-1][:top_k]
        return [ _DOCS[i] for i in idx if i < len(_DOCS) ]

    # If TF-IDF fallback
    if HAS_SKLEARN and _EMBEDDINGS is not None:
        q_vec = _TFIDF_VECT.transform([query])
        sims = cosine_similarity(_EMBEDDINGS, q_vec).squeeze()
        idx = sims.argsort()[::-1][:top_k]
        return [ _DOCS[i] for i in idx if i < len(_DOCS) ]

    # Minimal substring match fallback
    hits = [d for d in _DOCS if query.lower() in d.lower()]
    # If none, provide partial matches by words
    if not hits:
        tokens = query.lower().split()
        scored = []
        for d in _DOCS:
            score = sum(1 for t in tokens if t in d.lower())
            if score > 0:
                scored.append((score, d))
        scored.sort(reverse=True)
        hits = [d for s,d in scored]
    return hits[:top_k]


# Module convenience
__all__ = ["populate_sample_data", "query_vector_db", "add_documents"]
