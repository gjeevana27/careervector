from src.prompts.resume_info_prompt import RESUME_INFO_PROMPT
from src.prompts.ats_prompt import ATS_PROMPT


class PromptManager:

    @staticmethod
    def resume_prompt():
        return RESUME_INFO_PROMPT

    @staticmethod
    def ats_prompt():
        return ATS_PROMPT