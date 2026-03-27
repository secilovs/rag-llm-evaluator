from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()
collection = client.create_collection(name="test")

documents = [
    "Effluent BOD5 limit is typically 30 mg/L.",
    "TSS limit is 30 mg/L.",
    "pH must be between 6 and 9."
]

embeddings = model.encode(documents)

collection.add(
    documents=documents,
    embeddings=embeddings.tolist(),
    ids=["1", "2", "3"]
)

query = "What is BOD limit?"

query_embedding = model.encode([query])

results = collection.query(
    query_embeddings=query_embedding.tolist(),
    n_results=2
)

print(results)
