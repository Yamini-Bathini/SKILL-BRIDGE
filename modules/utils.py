import PyPDF2

def parse_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return parse_pdf(uploaded_file)
    elif uploaded_file.type == "text/plain":
        return uploaded_file.read().decode('utf-8')
    else:
        # Unsupported file type
        return ""