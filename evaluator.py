import os
import re
from crewai import Agent, Task, Crew, LLM
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable.")

job_post_text = """(default placeholder text)"""

def set_job_post_text(new_text: str):
    global job_post_text
    job_post_text = new_text

llm = LLM(
    provider="google",
    model="gemini/gemini-1.5-flash",
    api_key=API_KEY
)

resume_evaluator_agent = Agent(
    role="Resume Evaluator",
    goal="Evaluate a resume against a job description and give a compatibility score out of 10 with a brief explanation.",
    backstory="An experienced tech recruiter who compares resumes with job posts and gives objective feedback and scores based on qualifications and relevance.",
    llm=llm,
    verbose=True
)

def extract_text_from_document(document_path: str) -> str:
    if document_path.lower().endswith(".pdf"):
        loader = PyPDFLoader(document_path)
        pages = loader.load_and_split()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.split_documents(pages)
        return "\n\n".join([doc.page_content for doc in docs])
    elif document_path.lower().endswith(".txt"):
        with open(document_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        raise ValueError("Unsupported document format. Use .pdf or .txt")

def extract_name(text: str) -> str:
    lines = text.strip().split("\n")[:20]
    for line in lines:
        line = line.strip()
        if len(line.split()) > 4 or any(keyword in line.lower() for keyword in ['développeur', 'programmeur', 'engineer', 'analyste', 'stack']):
            continue
        if re.match(r"^[A-Z][a-zA-Zéèêàçïî]+(?:\s[A-Z][a-zA-Zéèêàçïî]+)+$", line):
            return line
    match = re.search(r"(?:Nom|Name)\s*:\s*([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)", text)
    return match.group(1) if match else "Unknown Candidate"

def fallback_name_from_filename(filename):
    name_part = os.path.splitext(filename)[0]
    return name_part.replace("_", " ").replace("-", " ").title()

def make_evaluation_task(resume_text: str) -> Task:
    description = f"""You are an experienced tech recruiter. Evaluate the resume below based on the job description provided.

Scoring (out of 10):
1. Core Technical Skills (.NET, C#, SQL) – 4 points  
2. Supporting Tech Stack (ReactJS, JS, NodeJS, VueJS, Python) – 2 points  
3. Soft Skills (Agile, Teamwork, Curiosity, Security Awareness) – 2 points  
4. Language & Education (French, English, Bachelor's in IT) – 2 points

Resume:
{resume_text}

Job Description:
{job_post_text}
"""
    return Task(
        name="Evaluate Resume",
        description=description,
        agent=resume_evaluator_agent,
        expected_output="""Score: X/10

Breakdown:
Core Technical Skills: X/4
Supporting Tech Stack: X/2
Soft Skills & Attitude: X/2
Language & Education: X/2

Explanation: [Your brief explanation]""",
        context=[]
    )

def parse_score(output: str) -> float:
    match = re.search(r"Score:\s*(\d+(?:\.\d*)?)/10", output)
    return float(match.group(1)) if match else 0.0

def run_resume_evaluation_crew(document_path: str):
    extracted_text = extract_text_from_document(document_path)
    if not extracted_text.strip():
        return "No text extracted.", "Unknown Candidate"

    candidate_name = extract_name(extracted_text)
    if candidate_name == "Unknown Candidate":
        candidate_name = fallback_name_from_filename(os.path.basename(document_path))

    resume_evaluation_task = make_evaluation_task(extracted_text)
    crew = Crew(agents=[resume_evaluator_agent], tasks=[resume_evaluation_task], verbose=True)
    result = crew.kickoff()
    output_text = result.output if hasattr(result, "output") else str(result)
    return output_text, candidate_name


def parse_score(output: str) -> float:
    match = re.search(r"Score:\s*(\d+(?:\.\d*)?)/10", output)
    return float(match.group(1)) if match else 0.0

