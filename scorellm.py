def get_llm_score(jd, resume):
    prompt = f"""
Compare the following resume to the job description.
Return a JSON object with:
- A score out of 100
- A one-line justification

Job Description:
{jd}

Resume:
{resume}
"""
    response = model.generate_content(prompt)
    return response.text.strip()
