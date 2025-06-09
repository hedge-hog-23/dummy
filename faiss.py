import numpy as np
import faiss
from sklearn.metrics.pairwise import cosine_similarity

def build_faiss_index(docs, get_embedding):
    vectors = [get_embedding(doc) for doc in docs]
    dim = len(vectors[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(vectors).astype("float32"))
    return index, vectors

def compare_with_faiss_and_cosine(jd_text, resume_texts, get_embedding):
    # Build FAISS index on resume embeddings
    index, resume_vectors = build_faiss_index(resume_texts, get_embedding)
    
    # Embed the JD text
    jd_vector = np.array([get_embedding(jd_text)]).astype("float32")

    # FAISS search - get distances and indices of closest resumes
    D, I = index.search(jd_vector, k=min(5, len(resume_texts)))

    results = []
    for rank, idx in enumerate(I[0]):
        faiss_distance = D[0][rank]
        faiss_score = 100 - faiss_distance  # heuristic
        
        # Compute cosine similarity score (0 to 1)
        cos_sim = cosine_similarity(
            jd_vector,
            np.array([resume_vectors[idx]]).astype("float32")
        )[0][0]
        cosine_score = cos_sim * 100  # scale to 0-100

        results.append({
            "resume_index": idx,
            "faiss_score": round(faiss_score, 2),
            "cosine_score": round(cosine_score, 2)
        })
    return results
