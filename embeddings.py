from google.generativeai import embeddings

def get_gemini_embedding(text):
    return embeddings.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="retrieval_document"
    )["embedding"]
