import os
from pdfparse import extract_text_from_pdf
from scorellm import get_llm_score
from embeddings import get_gemini_embedding
from faiss_compare import compare_with_faiss_only
from comparator import compare_resumes


def run_system(jd_path, resumes_folder):
    """Run the complete resume comparison system"""
    jd_text = open(jd_path, 'r', encoding='utf-8').read()
    resumes = [f for f in os.listdir(resumes_folder) if f.endswith(".pdf")]
    
    print(f"Found {len(resumes)} resumes to process")
    print(f"Job Description loaded from: {jd_path}")
    print("-" * 80)
    
    # Extract text from all resumes
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
        return
    
    print("\n" + "="*80)
    print("COMPARISON RESULTS")
    print("="*80)
    
    # Method 1: LLM-based scoring
    print("\n1. LLM-BASED SCORING:")
    print("-" * 40)
    
    llm_results = []
    for i, (name, text) in enumerate(zip(resume_names, resume_texts)):
        try:
            result = get_llm_score(jd_text, text)
            llm_results.append((name, result))
            print(f"\n{name}:")
            print(result)
            print("-" * 60)
        except Exception as e:
            print(f"Error scoring {name}: {e}")
    
    # Method 2: FAISS + Cosine Similarity
    print("\n2. EMBEDDING-BASED SCORING (FAISS + Cosine):")
    print("-" * 50)
    
    try:
        faiss_results = compare_with_faiss_only(jd_text, resume_texts, get_gemini_embedding)
        
        for result in faiss_results:
            idx = result["resume_index"]
            name = resume_names[idx]
            print(f"{name}:")
            print(f"  FAISS Score: {result['faiss_score']}")
            print(f"  Cosine Score: {result['cosine_score']}")
            print("-" * 40)
    except Exception as e:
        print(f"Error with FAISS comparison: {e}")
    
    # Method 3: General comparison function
    print("\n3. GENERAL COMPARISON:")
    print("-" * 30)
    
    try:
        general_results = compare_resumes(jd_text, resume_texts, resume_names)
        for result in general_results:
            print(f"{result['name']}: {result['score']}")
    except Exception as e:
        print(f"Error with general comparison: {e}")


if __name__ == "__main__":
    # Example usage
    jd_path = "job_description.txt"  # Path to your job description file
    resumes_folder = "resumes"       # Folder containing PDF resumes
    
    if os.path.exists(jd_path) and os.path.exists(resumes_folder):
        run_system(jd_path, resumes_folder)
    else:
        print("Please ensure job_description.txt and resumes folder exist")
