import json
from src.ai.client import AIClient
from src.prompts.interview_prompt import (
    INTERVIEW_SYSTEM_PROMPT,
    INTERVIEW_FEEDBACK_PROMPT
)


class InterviewService:

    def __init__(self):
        self.ai = AIClient()

    def get_system_prompt(
        self,
        resume_text: str,
        jd_text: str,
        job_title: str,
        company: str
    ) -> str:
        prompt = INTERVIEW_SYSTEM_PROMPT
        prompt = prompt.replace("<<RESUME_TEXT>>", resume_text[:1500])
        prompt = prompt.replace("<<JD_TEXT>>", jd_text[:1000])
        prompt = prompt.replace("<<JOB_TITLE>>", job_title)
        prompt = prompt.replace("<<COMPANY>>", company)
        return prompt

    def chat(
        self,
        messages: list,
        system_prompt: str
    ) -> str:
        from groq import Groq
        from src.core.config import settings

        client = Groq(api_key=settings.GROQ_API_KEY)

        response = client.chat.completions.create(
            # Use smaller model for chat to save tokens
            model=settings.INTERVIEW_MODEL,
            messages=[
                {"role": "system", "content": system_prompt}
            ] + messages,
            temperature=0.7,
            max_tokens=300  # keep responses short
        )

        return response.choices[0].message.content

    def generate_feedback(
        self,
        transcript: str,
        resume_text: str,
        jd_text: str,
        job_title: str,
        company: str
    ) -> dict:
        prompt = INTERVIEW_FEEDBACK_PROMPT
        prompt = prompt.replace("<<RESUME_TEXT>>", resume_text[:1500])
        prompt = prompt.replace("<<JD_TEXT>>", jd_text[:1000])
        prompt = prompt.replace("<<JOB_TITLE>>", job_title)
        prompt = prompt.replace("<<COMPANY>>", company)
        # Trim transcript to save tokens
        prompt = prompt.replace("<<TRANSCRIPT>>", transcript[:3000])

        response = self.ai.generate(
            system_prompt=(
                "You are CareerVector's Interview Analyst. "
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
                "overall_score": 0,
                "hiring_recommendation": "Unknown",
                "overall_summary": "Could not generate feedback.",
                "answer_evaluations": [],
                "strengths": [],
                "areas_to_improve": [],
                "skills_demonstrated": [],
                "skills_not_demonstrated": [],
                "best_answer": "",
                "weakest_answer": "",
                "next_steps": []
            }