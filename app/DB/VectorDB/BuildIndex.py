# Build FAISS vector index from database
import numpy as np
import faiss
from pathlib import Path
from DB.Postgres import fetch_all
from RecommenderModel.Vectorizer import load_vectorizer

INDEX_PATH = "DB/vectordb/faiss.index"
IDS_PATH = "DB/vectordb/internship_ids.npy"

def build_index():
    # load or train vectorizer
    vectorizer = load_vectorizer(retrain_if_missing=True)

    # fetch active internships
    rows = fetch_all(
        """
        SELECT internship_id, internship_title, company, domain, required_skills
        FROM internships
        WHERE is_active = true
        """
    )

    ids = []
    texts = []
    for iid, title, company, domain, skills in rows:
        parts = [str(p) for p in (title, company, domain, skills) if p]
        if not parts:
            continue
        ids.append(iid)
        texts.append(" ".join(parts))

    if not texts:
        raise RuntimeError("No internship records to index.")

    # vectorize to dense float32
    mat = vectorizer.transform(texts).toarray().astype("float32")

    # L2 normalize for cosine/IP search
    faiss.normalize_L2(mat)

    # build index
    index = faiss.IndexFlatIP(mat.shape[1])
    index.add(mat)

    # persist
    Path("DB/vectordb").mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    np.save(IDS_PATH, np.array(ids))
    print(f"Built index with {index.ntotal} items -> {INDEX_PATH}")

if __name__ == "__main__":
    build_index()