import json
from src.ai.client import AIClient
from src.prompts.skill_prompt import SKILL_PROMPT


class SkillService:

    def __init__(self):
        self.ai = AIClient()

    def analyze(
        self,
        resume_text: str,
        jd_text: str,
        job_title: str = "",
        company: str = ""
    ) -> dict:

        prompt = SKILL_PROMPT
        prompt = prompt.replace("<<RESUME_TEXT>>", resume_text[:3000])
        prompt = prompt.replace("<<JD_TEXT>>", jd_text[:2000])
        prompt = prompt.replace("<<JOB_TITLE>>", job_title)
        prompt = prompt.replace("<<COMPANY>>", company)

        response = self.ai.generate(
            system_prompt=(
                "You are CareerVector's Career Growth Advisor. "
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
                "job_fit_summary": "Could not generate analysis.",
                "skills_you_have": [],
                "skills_to_learn": [],
                "career_trajectory": [],
                "projects_to_build": [],
                "certifications_to_get": [],
                "resume_gaps": [],
                "quick_wins": []
            }