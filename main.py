import argparse
import json
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import pandas as pd

nltk.download('punkt')
nltk.download('stopwords')

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"Error: The file '{file_path}' was not found."
    except Exception as e:
        return f"Error: An error occurred while reading the file: {e}"

def parse_resume(resume_text):
    sections = extract_sections(resume_text)
    
    # Further process each section if needed
    if 'contact_info' in sections:
        sections['contact_info'] = parse_contact_info(sections['contact_info'])
    if 'education' in sections:
        sections['education'] = parse_education(sections['education'])
    if 'experience' in sections:
        sections['experience'] = parse_experience(sections['experience'])
    if 'skills' in sections:
        sections['skills'] = parse_skills(sections['skills'])
    if 'projects' in sections:
        sections['projects'] = parse_projects(sections['projects'])

    return json.dumps(sections, indent=4)

def extract_sections(text):
    patterns = {
        "contact_info": r"(?P<contact_info>(\w+.+\n)+\s*\n)",
        "education": r"(?P<education>Education\n(.+\n)+\s*\n)",
        "experience": r"(?P<experience>Experience\n(.+\n)+\s*\n)",
        "skills": r"(?P<skills>Skills\n(.+\n)+\s*\n)",
        "projects": r"(?P<projects>Projects\n(.+\n)+\s*\n)"
    }

    sections = {}
    for section, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            sections[section] = match.group(section).strip()

    return sections

def parse_contact_info(text):
    contact_info = {}
    lines = text.split('\n')
    contact_info['name'] = lines[0]
    contact_info['email'] = next((line for line in lines if '@' in line), '')
    contact_info['phone'] = next((line for line in lines if re.search(r'\+?\d[\d -]{8,12}\d', line)), '')
    return contact_info

def parse_education(text):
    education = []
    entries = text.split('\n\n')
    for entry in entries:
        lines = entry.split('\n')
        if lines:
            education.append({
                "institution": lines[0],
                "degree": lines[1] if len(lines) > 1 else '',
                "dates": lines[2] if len(lines) > 2 else ''
            })
    return education

def parse_experience(text):
    experience = []
    entries = text.split('\n\n')
    for entry in entries:
        lines = entry.split('\n')
        if lines:
            experience.append({
                "company": lines[0],
                "role": lines[1] if len(lines) > 1 else '',
                "dates": lines[2] if len(lines) > 2 else '',
                "details": lines[3:] if len(lines) > 3 else []
            })
    return experience

def parse_skills(text):
    skills = text.split('\n')[1:]  # Skip the "Skills" heading
    return [skill.strip() for skill in skills if skill.strip()]

def parse_projects(text):
    projects = []
    entries = text.split('\n\n')
    for entry in entries:
        lines = entry.split('\n')
        if lines:
            projects.append({
                "title": lines[0],
                "description": ' '.join(lines[1:])
            })
    return projects

def tokenize_and_filter(text):
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_words = [w for w in words if w.lower() not in stop_words]
    return filtered_words

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read resume content from a file and convert it to JSON format.")
    parser.add_argument('file_path', type=str, help="The path to the resume file to be read.")
    args = parser.parse_args()

    resume_text = read_file(args.file_path)
    if "Error" in resume_text:
        print(resume_text)
    else:
        filtered_text = ' '.join(tokenize_and_filter(resume_text))
        parsed_resume_json = parse_resume(filtered_text)
        print(parsed_resume_json)
