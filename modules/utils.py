import PyPDF2
import io

def parse_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        if not text.strip():
            return "[Note: PDF appears to be scanned – no selectable text found.]"
        return text
    except Exception as e:
        return f"[Error reading PDF: {e}]"

def parse_txt(file):
    try:
        file.seek(0)
        return file.read().decode('utf-8')
    except UnicodeDecodeError:
        file.seek(0)
        return file.read().decode('latin-1')
    except Exception as e:
        return f"[Error reading text file: {e}]"

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return parse_pdf(uploaded_file)
    elif uploaded_file.type == "text/plain":
        return parse_txt(uploaded_file)
    else:
        return ""