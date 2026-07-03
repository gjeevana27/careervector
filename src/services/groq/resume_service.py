from src.ai.client import AIClient
from src.ai.prompt_manager import PromptManager
from src.ai.response_parser import ResponseParser


class ResumeService:

    def __init__(self):
        self.ai = AIClient()

    def analyze(self, resume_text: str):

        prompt = PromptManager.resume_prompt()
        prompt = prompt.replace("<<RESUME_TEXT>>", resume_text)

        response = self.ai.generate(
            system_prompt=(
                "You are CareerVector's Resume Information Extractor.\n"
                "Return ONLY valid JSON.\n"
                "Do not use markdown."
            ),
            user_prompt=prompt,
        )

        data = ResponseParser.parse(response)

        # Normalize to expected schema if Groq returned flat structure
        if "candidate" not in data:
            data = {
                "candidate": {
                    "name": data.get("name", ""),
                    "email": data.get("email", ""),
                    "phone": data.get("phone", ""),
                    "location": data.get("location", ""),
                    "linkedin": data.get("linkedin", ""),
                },
                "summary": data.get("summary", ""),
                "skills": data.get("skills", []),
                "education": data.get("education", []),
                "experience": data.get("experience", []),
                "projects": data.get("projects", []),
                "certifications": data.get("certifications", []),
            }

        # Safety: ensure these are always lists, never None
        for key in ["skills", "education", "experience", "projects", "certifications"]:
            if not isinstance(data.get(key), list):
                data[key] = []

        # Safety: ensure projects always have a title key
        for project in data["projects"]:
            if "title" not in project:
                project["title"] = (
                    project.pop("project_name", None)
                    or project.pop("name", None)
                    or "Untitled Project"
                )
            if "technologies" not in project:
                tech = project.pop("tech_stack", None) or project.pop("tech", None) or []
                if isinstance(tech, str):
                    tech = [t.strip() for t in tech.split(",")]
                project["technologies"] = tech

        # Safety: ensure certifications always have a name key
        for cert in data["certifications"]:
            if "name" not in cert:
                cert["name"] = (
                    cert.pop("certification_name", None)
                    or cert.pop("title", None)
                    or "Untitled Certification"
                )

        return data