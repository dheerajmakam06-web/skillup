import io
import re


ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt'}


def extract_text(uploaded_file, extension):
    """Extract text in memory so uploaded resumes are not publicly stored."""
    content = uploaded_file.read()
    if extension == '.txt':
        return content.decode('utf-8', errors='ignore')
    if extension == '.pdf':
        from pypdf import PdfReader
        return '\n'.join(page.extract_text() or '' for page in PdfReader(io.BytesIO(content)).pages)
    if extension == '.docx':
        from docx import Document
        document = Document(io.BytesIO(content))
        return '\n'.join(paragraph.text for paragraph in document.paragraphs)
    raise ValueError('Unsupported resume type')


def extract_resume_profile(text):
    text = text or ''
    email = re.search(r'[\w.+-]+@[\w-]+(?:\.[\w-]+)+', text)
    phone = re.search(r'(?<!\d)(?:\+?91[\s-]?)?[6-9]\d{9}(?!\d)', text)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    sections = {'projects': [], 'certifications': [], 'experience': []}
    current = None
    headings = {
        'project': 'projects', 'projects': 'projects', 'certification': 'certifications',
        'certifications': 'certifications', 'experience': 'experience',
        'internship': 'experience', 'internships': 'experience',
    }
    for line in lines:
        key = headings.get(re.sub(r'[^a-z]', '', line.lower()))
        if key:
            current = key
        elif current:
            sections[current].append(line)
    return {
        'name': lines[0] if lines else '',
        'email': email.group(0) if email else '',
        'phone': phone.group(0) if phone else '',
        'projects': sections['projects'],
        'certifications': sections['certifications'],
        'experience': sections['experience'],
    }