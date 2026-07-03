import requests
import os
from dotenv import load_dotenv

load_dotenv()


class JobFetchService:

    def __init__(self):
        self.api_key = os.getenv("JSEARCH_API_KEY")
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }

    def build_queries(self, resume: dict) -> list:
        """
        Build job search queries from resume skills and experience.
        """
        queries = []

        # Get skills from resume
        skills = resume.get("skills", [])

        # Get job titles from experience
        experience = resume.get("experience", [])
        titles = [
            e.get("title", "")
            for e in experience
            if isinstance(e, dict) and e.get("title")
        ]

        # Get education field
        education = resume.get("education", [])
        degrees = [
            e.get("degree", "")
            for e in education
            if isinstance(e, dict) and e.get("degree")
        ]

        # Build queries from titles
        for title in titles[:3]:
            if title:
                queries.append(f"{title} USA")

        # Build queries from top skills
        for skill in skills[:3]:
            if skill:
                queries.append(f"{skill} engineer USA")

        # Build queries from degree
        for degree in degrees[:2]:
            if degree:
                queries.append(f"{degree} USA")

        # Remove duplicates and limit
        seen = set()
        unique_queries = []
        for q in queries:
            if q.lower() not in seen:
                seen.add(q.lower())
                unique_queries.append(q)

        # Always have at least 3 queries
        if len(unique_queries) < 3:
            unique_queries.extend([
                "Software Engineer USA",
                "Data Analyst USA",
                "Engineer USA"
            ])

        return unique_queries[:8]  # max 8 queries to stay within free tier

    def fetch_jobs(self, queries: list) -> list:
        """
        Fetch real-time jobs from JSearch for given queries.
        """
        all_jobs = []

        for query in queries:
            try:
                response = requests.get(
                    "https://jsearch.p.rapidapi.com/search-v2",
                    headers=self.headers,
                    params={
                        "query": query,
                        "page": "1",
                        "num_pages": "1",
                        "date_posted": "all",
                        "country": "us"
                    },
                    timeout=20
                )

                data = response.json()

                if data.get("status") != "OK":
                    continue

                jobs = data.get("data", {}).get("jobs", [])

                for job in jobs:
                    if not isinstance(job, dict):
                        continue

                    raw_skills = job.get("job_required_skills") or ""
                    if isinstance(raw_skills, list):
                        skills = ", ".join([
                            s if isinstance(s, str) else str(s)
                            for s in raw_skills
                        ])
                    else:
                        skills = str(raw_skills)

                    city = job.get("job_city") or ""
                    state = job.get("job_state") or ""
                    country = job.get("job_country") or ""
                    location = f"{city} {state} {country}".strip()

                    all_jobs.append({
                        "id": str(job.get("job_id", "")),
                        "title": str(job.get("job_title", "")),
                        "company": str(job.get("employer_name", "")),
                        "location": location,
                        "full_description": str(
                            job.get("job_description", "")
                        ),
                        "required_skills": skills,
                        "employment_type": str(
                            job.get("job_employment_type", "")
                        ),
                        "is_remote": bool(
                            job.get("job_is_remote", False)
                        ),
                        "apply_link": str(
                            job.get("job_apply_link", "")
                        ),
                        "posted_at": str(
                            job.get("job_posted_at_datetime_utc", "")
                        )
                    })

            except Exception as e:
                print(f"Error fetching {query}: {e}")
                continue

        # Remove duplicates
        seen_ids = set()
        unique_jobs = []
        for job in all_jobs:
            if job["id"] not in seen_ids and job["full_description"]:
                seen_ids.add(job["id"])
                unique_jobs.append(job)

        return unique_jobs