import fitz  # PyMuPDF

class DocumentParser:
    @staticmethod
    def parse_pdf(file_bytes: bytes) -> str:
        """Extracts text from a PDF file."""
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    @staticmethod
    def parse_txt(file_bytes: bytes) -> str:
        """Extracts text from a TXT file."""
        return file_bytes.decode("utf-8")

    @staticmethod
    def parse_file(file_content: bytes, filename: str) -> str:
        """Determines file type and parses accordingly."""
        if filename.lower().endswith(".pdf"):
            return DocumentParser.parse_pdf(file_content)
        elif filename.lower().endswith(".txt"):
            return DocumentParser.parse_txt(file_content)
        else:
            raise ValueError("Unsupported file format. Please upload PDF or TXT.")
