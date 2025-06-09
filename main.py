import os


def run_system(jd_path, resumes_folder):
    jd_text = open(jd_path).read()
    resumes = [f for f in os.listdir(resumes_folder) if f.endswith(".pdf")]

    results = []
    for resume in resumes:
        path = os.path.join(resumes_folder, resume)
        text = extract_text_from_pdf(path)
        result = get_llm_score(jd_text, text)
        results.append((resume, result))

    for name, res in results:
        print(f"\n{name}:\n{res}\n{'-'*60}")
