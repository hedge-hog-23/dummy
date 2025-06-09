import os
import sys
from io import StringIO
from pdfparse import extract_text_from_pdf
from scorellm import get_llm_score
from embeddings import get_gemini_embedding
from faiss_compare import compare_with_faiss_only
from comparator import compare_resumes
import mail  # Your existing mail.py

def run_system(jd_path, resumes_folder):
    buffer = StringIO()
    original_stdout = sys.stdout
    sys.stdout = buffer  # Redirect print to buffer

    jd_text = open(jd_path, 'r', encoding='utf-8').read()
    resumes = [f for f in os.listdir(resumes_folder) if f.endswith(".pdf")]

    print(f"Found {len(resumes)} resumes to process")
    print(f"Job Description loaded from: {jd_path}")
    print("-" * 80)

    resume_texts = []
    resume_names = []

    for resume in resumes:
        path = os.path.join(resumes_folder, resume)
        try:
            text = extract_text_from_pdf(path)
            resume_texts.append(text)
            resume_names.append(resume)
            print(f"Processed: {resume}")
        except Exception as e:
            print(f"Error processing {resume}: {e}")

    if not resume_texts:
        print("No resumes could be processed!")
        sys.stdout = original_stdout
        return ""

    print("\n" + "="*80)
    print("COMPARISON RESULTS")
    print("="*80)

    print("\n1. LLM-BASED SCORING:")
    print("-" * 40)
    for name, text in zip(resume_names, resume_texts):
        try:
            result = get_llm_score(jd_text, text)
            print(f"\n{name}:\n{result}")
            print("-" * 60)
        except Exception as e:
            print(f"Error scoring {name}: {e}")

    print("\n2. EMBEDDING-BASED SCORING (FAISS):")
    print("-" * 50)
    try:
        faiss_results = compare_with_faiss_only(jd_text, resume_texts, get_gemini_embedding)
        for result in faiss_results:
            name = resume_names[result["resume_index"]]
            print(f"{name}:\n  FAISS Score: {result['faiss_score']}")
            print("-" * 40)
    except Exception as e:
        print(f"Error with FAISS comparison: {e}")

    print("\n3. GENERAL COMPARISON:")
    print("-" * 30)
    try:
        general_results = compare_resumes(jd_text, resume_texts, resume_names)
        for result in general_results:
            print(f"{result['name']}: {result['score']}")
    except Exception as e:
        print(f"Error with general comparison: {e}")

    sys.stdout = original_stdout  # Restore print
    return buffer.getvalue()


if __name__ == "__main__":
    jd_path = "job_description.txt"
    resumes_folder = "resumes"

    if os.path.exists(jd_path) and os.path.exists(resumes_folder):
        output_text = run_system(jd_path, resumes_folder)
        print(output_text)  # Still prints to console
        mail.send_email_with_text(output_text)  # Send captured output
    else:
        print("Please ensure job_description.txt and resumes folder exist")
