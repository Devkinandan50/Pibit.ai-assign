import argparse
import json
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import pandas as pd
import PyPDF2
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')



import argparse
import PyPDF2

def read_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            content = ""
            for i in range(num_pages):
                page = reader.pages[i]
                content += page.extract_text()
        return content
    except FileNotFoundError:
        return f"Error: The file '{file_path}' was not found."
    except Exception as e:
        return f"Error: An error occurred while reading the file: {e}"


def fix_text_spacing(text):
    # Insert spaces between words where needed
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'(\d)([A-Z])', r'\1 \2', text)
    text = re.sub(r'([a-z])(\d)', r'\1 \2', text)
    text = re.sub(r'([A-Z])([A-Z][a-z])', r'\1 \2', text)
    return text

def parse_resume(text):
    # text = fix_text_spacing(text)
    data = {}

    # Extract contact information
    contact_info = re.search(r"(\(\+91\)-[\d\-]+)\n([a-zA-Z0-9\.]+@[a-zA-Z0-9]+\.[a-zA-Z]+)\n(\w+\s\w+)\n(linkedin)", text, re.IGNORECASE)
    if contact_info:
        data['contact_info'] = {
            'phone': contact_info.group(1),
            'email': contact_info.group(2),
            'name': contact_info.group(3),
            'linkedin': contact_info.group(4)
        }

    # Extract education
    education = re.search(r"EDUCATION\n(.+?)(?=\n[A-Z])", text, re.IGNORECASE | re.DOTALL)
    if education:
        data['education'] = education.group(1).strip()

    # Extract experience
    experience = re.search(r"EXPERIENCE\n(.+?)(?=\n[A-Z])", text, re.IGNORECASE | re.DOTALL)
    if experience:
        data['experience'] = experience.group(1).strip()

    # Extract projects
    projects = re.search(r"PROJECTS\n(.+?)(?=\n[A-Z])", text, re.IGNORECASE | re.DOTALL)
    if projects:
        data['projects'] = projects.group(1).strip()

    # Extract skills
    skills = re.search(r"SKILLS\n(.+?)(?=\n[A-Z])", text, re.IGNORECASE | re.DOTALL)
    if skills:
        data['skills'] = skills.group(1).strip()

    # Extract responsibilities and achievements
    responsibilities = re.search(r"RESPONSIBILITIES & ACHIEVEMENTS\n(.+?)(?=\nPROFILES|$)", text, re.IGNORECASE | re.DOTALL)
    if responsibilities:
        data['responsibilities_achievements'] = responsibilities.group(1).strip()

    # Extract profiles
    profiles = re.search(r"PROFILES\n(.+?)(?=\n[A-Z]|$)", text, re.IGNORECASE | re.DOTALL)
    if profiles:
        data['profiles'] = profiles.group(1).strip()

    return data



def tokenize_and_filter(text):
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_words = [w for w in words if w.lower() not in stop_words]
    return filtered_words


if __name__ == "__main__":
    print("""to run this code you need to add file path as arguments like this
          
          python "d:\Project\Pibit.ai-assign\main.py" D:/Project/Pibit.ai-assign/Devkinandan_resume_ds.pdf
          
          \n \n""")
    parser = argparse.ArgumentParser(description="Read content from a PDF file.")
    parser.add_argument('file_path', type=str, help="The path to the PDF file to be read.")
    args = parser.parse_args()

    pdf_content = read_pdf(args.file_path)

    if "Error" in pdf_content:
        print(pdf_content)
    else:
        # filtered_text = ' '.join(tokenize_and_filter(pdf_content))
        parsed_data = parse_resume(pdf_content)
        parsed_json = json.dumps(parsed_data, indent=4)
        print(parsed_json)
    # print(pdf_content)





