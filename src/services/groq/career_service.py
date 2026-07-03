import json
from src.ai.client import AIClient
from src.prompts.career_prompt import CAREER_GAP_PROMPT


class CareerService:

    def __init__(self):
        self.ai = AIClient()

    def gap_analysis(
        self,
        resume_text: str,
        jd_text: str,
        job_title: str = ""
    ) -> dict:

        prompt = CAREER_GAP_PROMPT
        prompt = prompt.replace("<<JOB_TITLE>>", job_title)
        prompt = prompt.replace("<<RESUME_TEXT>>", resume_text[:3000])
        prompt = prompt.replace("<<JD_TEXT>>", jd_text[:2000])

        response = self.ai.generate(
            system_prompt=(
                "You are CareerVector's Career Advisor. "
                "Return ONLY valid JSON. No markdown."
            ),
            user_prompt=prompt
        )

        raw = response.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        try:
            return json.loads(raw.strip())
        except json.JSONDecodeError:
            return {
                "match_summary": "Could not generate analysis.",
                "matching_skills": [],
                "missing_skills": [],
                "keywords_to_add": [],
                "suggested_bullet": "",
                "interview_talking_points": [],
                "overall_fit": "Unknown"
            }