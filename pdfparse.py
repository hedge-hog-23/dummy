import fitz  # PyMuPDF

def extract_text_from_pdf(path):
    """Extract text from a PDF file"""
    try:
        doc = fitz.open(path)
        text = "\n".join([page.get_text() for page in doc])
        doc.close()
        return text
    except Exception as e:
        raise Exception(f"Failed to extract text from {path}: {e}")