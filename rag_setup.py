from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="wastewater")

documents = ["BOD limit 30 mg/L", "pH 6-9 arası"]
