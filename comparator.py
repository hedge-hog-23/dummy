from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def compare_resumes(jd_text, resume_texts, resume_names, get_embedding_func=None):
    """General function to compare resumes with job description"""
    if get_embedding_func is None:
        from embeddings import get_gemini_embedding
        get_embedding_func = get_gemini_embedding
    
    results = []
    
    try:
        # Get job description embedding
        jd_embedding = get_embedding_func(jd_text)
        jd_vector = np.array([jd_embedding])
        
        # Compare each resume
        for i, (resume_text, resume_name) in enumerate(zip(resume_texts, resume_names)):
            try:
                resume_embedding = get_embedding_func(resume_text)
                resume_vector = np.array([resume_embedding])

                similarity = cosine_similarity(jd_vector, resume_vector)[0][0]
                score = round(similarity * 100, 2)
                
                results.append({
                    "name": resume_name,
                    "score": score,
                    "similarity": similarity
                })
                
            except Exception as e:
                print(f"Error processing {resume_name}: {e}")
                results.append({
                    "name": resume_name,
                    "score": 0,
                    "similarity": 0,
                    "error": str(e)
                })
    
    except Exception as e:
        print(f"Error getting job description embedding: {e}")
        return []
    
    results.sort(key=lambda x: x["score"], reverse=True)
    return results