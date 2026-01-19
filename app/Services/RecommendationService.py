from typing import List

from Schemas.StudentDetails import StudentDetails
from Schemas.StudentRecommendation import RecommendationResponse, StudentRecommendation
from DB.VectorDB.Search import search_with_scores
from DB.Postgres import fetch_all


def _build_query_text(student: StudentDetails) -> str:
    parts: List[str] = []
    if student.domain:
        parts.append(student.domain)
    if student.skills:
        parts.extend(student.skills)
    return " ".join(parts)


def _fetch_internships_by_ids(ids: List[int]):
    if not ids:
        return []

    rows = fetch_all(
        """
        SELECT internship_id, internship_title, company, domain, required_skills, stipend
        FROM internships
        WHERE internship_id = ANY(%s)
        """,
        (ids,),
    )
    return rows


def recommend_for_student(student: StudentDetails, top_k: int = 5) -> StudentRecommendation:
    """Generate internship recommendations for a student using the FAISS vector DB."""
    query_text = _build_query_text(student)
    scored = search_with_scores(query_text, k=top_k)
    if not scored:
        return StudentRecommendation(
            student_id=student.student_id,
            student_name=student.name,
            student_skills=student.skills,
            recommendatons=[],
            total_recommendations=0,
        )

    ids = [iid for iid, _ in scored]
    score_map = {iid: score for iid, score in scored}

    rows = _fetch_internships_by_ids(ids)

    recs: List[RecommendationResponse] = []
    for iid, title, company, domain, skills, stipend in rows:
        recs.append(
            RecommendationResponse(
                rank=0,  # temporary; will sort and fill ranks next
                internship_id=str(iid),
                internship_title=title,
                company=company,
                similarity_score=float(score_map.get(iid, 0.0)),
                required_skills=[s.strip() for s in str(skills).split(",") if s.strip()],
                stipend=float(stipend) if stipend is not None else 0.0,
                domain=domain,
            )
        )

    recs.sort(key=lambda r: r.similarity_score, reverse=True)
    for idx, rec in enumerate(recs, start=1):
        rec.rank = idx

    return StudentRecommendation(
        student_id=student.student_id,
        student_name=student.name,
        student_skills=student.skills,
        recommendatons=recs,
        total_recommendations=len(recs),
    )
