import requests
import pandas as pd
import os
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("JSEARCH_API_KEY")

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

QUERIES = [
    "Data Engineer USA",
    "Machine Learning Engineer USA",
    "Data Scientist USA",
    "Data Analyst USA",
    "AI Engineer USA",
    "Analytics Engineer USA",
    "MLOps Engineer USA",
    "Python Data Engineer USA",
    "SQL Data Analyst USA",
    "NLP Engineer USA",
]

all_jobs = []

for query in QUERIES:
    print(f"Fetching: {query}")

    try:
        response = requests.get(
            "https://jsearch.p.rapidapi.com/search-v2",
            headers=headers,
            params={
                "query": query,
                "page": "1",
                "num_pages": "1",
                "date_posted": "all",
                "country": "us"
            },
            timeout=20
        )

        print(f"  Status: {response.status_code}")
        data = response.json()

        if data.get("status") != "OK":
            print(f"  API error: {data}")
            continue

        # ← Fixed: data["data"]["jobs"] not data["data"]
        jobs = data.get("data", {}).get("jobs", [])

        if not jobs:
            print(f"  No jobs found")
            continue

        print(f"  Found: {len(jobs)} jobs")

        for job in jobs:

            if not isinstance(job, dict):
                continue

            # Handle required_skills safely
            raw_skills = job.get("job_required_skills") or ""
            if isinstance(raw_skills, list):
                skills = ", ".join([
                    s if isinstance(s, str) else str(s)
                    for s in raw_skills
                ])
            else:
                skills = str(raw_skills)

            # Handle location safely
            city = job.get("job_city") or ""
            state = job.get("job_state") or ""
            country = job.get("job_country") or ""
            location = f"{city} {state} {country}".strip()

            all_jobs.append({
                "id": str(job.get("job_id", "")),
                "title": str(job.get("job_title", "")),
                "company": str(job.get("employer_name", "")),
                "location": location,
                "full_description": str(job.get("job_description", "")),
                "required_skills": skills,
                "employment_type": str(job.get("job_employment_type", "")),
                "is_remote": bool(job.get("job_is_remote", False)),
                "apply_link": str(job.get("job_apply_link", "")),
                "posted_at": str(job.get("job_posted_at_datetime_utc", ""))
            })

        time.sleep(1)

    except Exception as e:
        print(f"  Error: {e}")
        continue

print(f"\nTotal raw jobs: {len(all_jobs)}")

if not all_jobs:
    print("No jobs fetched.")
else:
    df = pd.DataFrame(all_jobs)
    df = df.drop_duplicates(subset=["id"])
    df = df[df["full_description"].notna()]
    df = df[df["full_description"].str.len() > 100]
    df = df.reset_index(drop=True)

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/jobs.csv", index=False)

    print(f"Saved {len(df)} unique jobs to data/jobs.csv")
    print("\nSample jobs:")
    print(df[["title", "company", "location"]].head(10).to_string())