import json
from src.ai.client import AIClient
from src.prompts.optimizer_prompt import OPTIMIZER_PROMPT


class OptimizerService:

    def __init__(self):
        self.ai = AIClient()

    def optimize(
        self,
        resume_text: str,
        jd_text: str,
        job_title: str = "",
        company: str = ""
    ) -> dict:

        prompt = OPTIMIZER_PROMPT
        prompt = prompt.replace("<<RESUME_TEXT>>", resume_text[:3000])
        prompt = prompt.replace("<<JD_TEXT>>", jd_text[:2000])
        prompt = prompt.replace("<<JOB_TITLE>>", job_title)
        prompt = prompt.replace("<<COMPANY>>", company)

        response = self.ai.generate(
            system_prompt=(
                "You are CareerVector's Resume Writing Expert. "
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
                "summary_rewrite": {
                    "original": "",
                    "rewritten": "",
                    "improvements_made": []
                },
                "bullet_rewrites": [],
                "weak_verbs_found": [],
                "skills_to_highlight": [],
                "headline_options": [],
                "tone_analysis": {
                    "current_tone": "",
                    "recommended_tone": "",
                    "tone_tips": []
                },
                "jd_language_to_mirror": [],
                "overall_boost_score": 0,
                "estimated_score_after": 0,
                "boost_summary": "Could not generate optimization."
            }