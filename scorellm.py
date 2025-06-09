import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_llm_score(jd, resume):
    """Get LLM-based score for resume against job description"""
    prompt = f"""
Compare the following resume to the job description.
Return a JSON object with:
- A score out of 100 (integer)
- A one-line justification (string)

Format your response as valid JSON like this:
{{"score": 85, "justification": "Strong match with required skills but lacks leadership experience"}}

Job Description:
{jd}

Resume:
{resume}
"""
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Try to parse as JSON
        try:
            json_response = json.loads(response_text)
            return f"Score: {json_response.get('score', 'N/A')}/100\nJustification: {json_response.get('justification', 'No justification provided')}"
        except json.JSONDecodeError:
            # If JSON parsing fails, return the raw response
            return response_text
            
    except Exception as e:
        return f"Error getting LLM score: {e}"
