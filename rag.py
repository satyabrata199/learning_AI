from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = [
    "Python is a programming language",
    "AI agents can use tools",
    "RAG improves LLM accuracy",
    "my name is satya"
]

embeddings = model.encode(documents, normalize_embeddings=True)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

def retrieve(query, k=2):
    query_embedding = model.encode([query], normalize_embeddings=True)

    distances, indices = index.search(query_embedding, k)

    results = []
    for i, dist in zip(indices[0], distances[0]):
        results.append((documents[i], dist))

    return results


