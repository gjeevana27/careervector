import fitz
from docx import Document


class ResumeParser:
    """
    Extracts text from PDF and DOCX resumes.
    """

    @staticmethod
    def read_pdf(uploaded_file):

        pdf = fitz.open(
            stream=uploaded_file.read(),
            filetype="pdf",
        )

        text = ""

        for page in pdf:
            text += page.get_text()

        pdf.close()

        return text

    @staticmethod
    def read_docx(uploaded_file):

        document = Document(uploaded_file)

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

        return text

    @staticmethod
    def extract_text(uploaded_file):

        extension = uploaded_file.name.split(".")[-1].lower()

        if extension == "pdf":
            return ResumeParser.read_pdf(uploaded_file)

        elif extension == "docx":
            return ResumeParser.read_docx(uploaded_file)

        raise ValueError(
            "Unsupported file type. Please upload a PDF or DOCX resume."
        )