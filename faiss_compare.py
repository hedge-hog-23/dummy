import numpy as np
import faiss

def build_faiss_index(docs, get_embedding):
    """Build FAISS index from document embeddings"""
    vectors = []
    for doc in docs:
        try:
            embedding = get_embedding(doc)
            vectors.append(embedding)
        except Exception as e:
            print(f"Error getting embedding: {e}")
            vectors.append([0.0] * 768)  # fallback: zero vector

    if not vectors:
        raise Exception("No valid embeddings generated")
    
    dim = len(vectors[0])
    index = faiss.IndexFlatL2(dim)
    vectors_array = np.array(vectors).astype("float32")
    index.add(vectors_array)
    return index, vectors

def compare_with_faiss_only(jd_text, resume_texts, get_embedding):
    """Compare JD with resumes using FAISS only (no cosine)"""
    if not resume_texts:
        return []
    

    index, resume_vectors = build_faiss_index(resume_texts, get_embedding)
    
    try:
        jd_embedding = get_embedding(jd_text)
        jd_vector = np.array([jd_embedding]).astype("float32")
    except Exception as e:
        raise Exception(f"Failed to embed job description: {e}")

    # Search all resumes
    k = len(resume_texts)
    D, I = index.search(jd_vector, k=k)

    all_distances = D[0]
    min_distance = np.min(all_distances)
    max_distance = np.max(all_distances)
    
    print(f"Distance range: {min_distance:.4f} to {max_distance:.4f}")

    results = []
    for rank, idx in enumerate(I[0]):
        faiss_distance = D[0][rank]

        if max_distance > min_distance:
            normalized_score = (max_distance - faiss_distance) / (max_distance - min_distance)
            faiss_score = normalized_score * 100
        else:
            faiss_score = 100  # all distances equal
        
        results.append({
            "resume_index": idx,
            "faiss_distance": round(faiss_distance, 4),
            "faiss_score": round(faiss_score, 2)
        })

    results.sort(key=lambda x: x["faiss_score"], reverse=True)
    return results
