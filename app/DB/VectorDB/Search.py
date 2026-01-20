import faiss
import numpy as np
import pickle
from pathlib import Path
from typing import List, Tuple

_index = None
_ids = None
_vectorizer = None

INDEX_PATH = Path("DB/vectordb/faiss.index")
IDS_PATH = Path("DB/vectordb/internship_ids.npy")
VECTORIZER_PATH = Path("Constants/vectorizer.pkl")


def _load_artifacts():
    """Lazy load FAISS index, IDs, and vectorizer."""
    global _index, _ids, _vectorizer
    
    if _index is None:
        if not INDEX_PATH.exists():
            raise FileNotFoundError(
                f"FAISS index not found at {INDEX_PATH}. "
                "Run DB/VectorDB/BuildIndex.py first."
            )
        _index = faiss.read_index(str(INDEX_PATH))
    
    if _ids is None:
        if not IDS_PATH.exists():
            raise FileNotFoundError(f"Internship IDs not found at {IDS_PATH}")
        _ids = np.load(str(IDS_PATH))
    
    if _vectorizer is None:
        if not VECTORIZER_PATH.exists():
            raise FileNotFoundError(f"Vectorizer not found at {VECTORIZER_PATH}")
        with open(VECTORIZER_PATH, "rb") as f:
            _vectorizer = pickle.load(f)
    
    return _index, _ids, _vectorizer


def recommend_top_5(student_text: str):
    index, ids, vectorizer = _load_artifacts()
    
    query_vec = vectorizer.transform([student_text]).toarray().astype("float32")
    faiss.normalize_L2(query_vec)

    scores, idx = index.search(query_vec, 5)
    return ids[idx[0]].tolist()


def search_with_scores(student_text: str, k: int = 5) -> List[Tuple[int, float]]:
    """Return (internship_id, similarity_score) pairs sorted by score desc."""
    index, ids, vectorizer = _load_artifacts()
    
    query_vec = vectorizer.transform([student_text]).toarray().astype("float32")
    faiss.normalize_L2(query_vec)
    scores, idx = index.search(query_vec, k)
    top_ids = ids[idx[0]].tolist()
    top_scores = scores[0].tolist()
    return list(zip(top_ids, top_scores))

