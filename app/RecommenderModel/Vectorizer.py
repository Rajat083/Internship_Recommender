import pickle
from pathlib import Path
from typing import Iterable, List, Union

from sklearn.feature_extraction.text import TfidfVectorizer

from Constants.config import MODEL_CONFIG
from DB.Postgres import fetch_all

_vectorizer: TfidfVectorizer | None = None
_VECTORIZER_PATH = Path(MODEL_CONFIG["vectorizer_path"])


def _fetch_internship_corpus() -> List[str]:
    """Pull internship text fields to build the TF-IDF corpus."""
    query = (
        "SELECT internship_title, company, domain, required_skills "
        "FROM internships WHERE is_active = true"
    )
    rows = fetch_all(query)

    corpus: List[str] = []
    for title, company, domain, skills in rows:
        parts: List[str] = []
        for field in (title, company, domain, skills):
            if field:
                parts.append(str(field))
        if parts:
            corpus.append(" ".join(parts))

    return corpus


def train_and_save_vectorizer(force: bool = False) -> TfidfVectorizer:
    """Train a TF-IDF vectorizer on DB data and persist it."""
    global _vectorizer

    if _VECTORIZER_PATH.exists() and not force:
        return load_vectorizer()

    corpus = _fetch_internship_corpus()
    if not corpus:
        raise RuntimeError("No internship records found to train the vectorizer.")

    vectorizer = TfidfVectorizer(stop_words="english")
    vectorizer.fit(corpus)

    _VECTORIZER_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(_VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)

    _vectorizer = vectorizer
    return vectorizer


def load_vectorizer(retrain_if_missing: bool = True) -> TfidfVectorizer:
    """Load the vectorizer from disk, training if absent."""
    global _vectorizer

    if _vectorizer is not None:
        return _vectorizer

    if _VECTORIZER_PATH.exists():
        with open(_VECTORIZER_PATH, "rb") as f:
            _vectorizer = pickle.load(f)
        return _vectorizer

    if retrain_if_missing:
        return train_and_save_vectorizer(force=True)

    raise FileNotFoundError(f"Vectorizer not found at {_VECTORIZER_PATH}")


def _to_text(skills: Union[str, Iterable[str]]) -> str:
    if isinstance(skills, str):
        return skills
    return " ".join(skills)


def vectorize_skills(skills: Union[str, Iterable[str]]):
    vectorizer = load_vectorizer()
    return vectorizer.transform([_to_text(skills)])


def vectorize_multiple_skills(skills_list: List[Union[str, Iterable[str]]]):
    vectorizer = load_vectorizer()
    texts = [_to_text(skills) for skills in skills_list]
    return vectorizer.transform(texts)
