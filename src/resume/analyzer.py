from src.resume.resume_parser import ResumeParser
from src.services.groq.resume_service import ResumeService


class ResumeAnalyzer:

    def __init__(self):

        self.resume_service = ResumeService()

    def analyze(self, uploaded_file):

        resume_text = ResumeParser.extract_text(uploaded_file)

        resume = self.resume_service.analyze(resume_text)

        return resume, resume_text