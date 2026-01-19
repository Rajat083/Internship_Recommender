from typing import Iterable, List, Union

from DB.Postgres import fetch_all
from DB.VectorDB.Search import recommend_top_5


def _to_text(skills: Union[str, Iterable[str]]) -> str:
	if isinstance(skills, str):
		return skills
	return " ".join(skills)


def get_internship_details(internship_ids: List[int]):
	"""Fetch internship details for the given ids and preserve the original order."""
	if not internship_ids:
		return []

	id_to_rank = {iid: rank for rank, iid in enumerate(internship_ids)}
	rows = fetch_all(
		"""
		SELECT internship_id, internship_title, company, domain, required_skills
		FROM internships
		WHERE internship_id = ANY(%s)
		""",
		(internship_ids,),
	)

	results = []
	for iid, title, company, domain, skills in rows:
		results.append(
			{
				"internship_id": iid,
				"internship_title": title,
				"company": company,
				"domain": domain,
				"required_skills": skills,
				"rank": id_to_rank.get(iid, len(internship_ids)),
			}
		)

	return sorted(results, key=lambda r: r["rank"])


def recommend_internships(skills: Union[str, Iterable[str]], top_k: int = 5):
	"""Return the top-k internships via semantic search on the FAISS index."""
	query_text = _to_text(skills)
	ids = recommend_top_5(query_text)[:top_k]
	return get_internship_details(ids)
