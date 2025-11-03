import PyPDF2

def extract_text_from_pdf(pdf_file):
    text = ""
    # The pdf_file object from Gradio has a .name attribute (which is the temp file path)
    reader = PyPDF2.PdfReader(pdf_file.name)
    for page in reader.pages:
        text += page.extract_text()
    return text