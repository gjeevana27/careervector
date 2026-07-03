from src.ai.client import AIClient
from src.ai.prompt_manager import PromptManager
from src.ai.response_parser import ResponseParser
from src.ai.json_validator import JSONValidator


class ATSService:

    def __init__(self):
        self.ai = AIClient()

    def analyze(
        self,
        resume_text: str,
        jd_text: str = "",
        job_title: str = ""
    ):

        prompt = PromptManager.ats_prompt()

        prompt = prompt.replace("<<RESUME_TEXT>>", resume_text[:3000])
        prompt = prompt.replace(
            "<<JD_TEXT>>",
            jd_text[:2000] if jd_text else "Not provided"
        )
        prompt = prompt.replace(
            "<<JOB_TITLE>>",
            job_title if job_title else "Not provided"
        )

        response = self.ai.generate(
            system_prompt=(
                "You are CareerVector's ATS Resume Expert. "
                "Return ONLY valid JSON. No markdown."
            ),
            user_prompt=prompt,
        )

        data = ResponseParser.parse(response)

        JSONValidator.validate(
            data,
            required_keys=[
                "overall_score",
                "format_score",
                "keyword_score",
                "section_score",
                "strengths",
                "missing_keywords",
                "recommendations",
            ],
        )

        return data