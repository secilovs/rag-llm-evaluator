import json
import chromadb
from sentence_transformers import SentenceTransformer
import requests
import os
import re

# =========================
# 🔹 GROUND TRUTH
# =========================
DATA = {
    "EPA": {
        "BOD": {"30_day": "30 mg/L"},
        "TSS": {"30_day": "30 mg/L"},
        "PH": "6.0-9.0"
    },
    "SKKY": {
        "BOD": "45 mg/L",
        "COD": "120 mg/L",
        "TSS": "45 mg/L",
        "PH": "6-9"
    }
}

def get_param(q):
    q = q.lower()
    if "bod" in q: return "BOD"
    if "cod" in q: return "COD"
    if "tss" in q or "ss" in q: return "TSS"
    if "ph" in q: return "PH"
    return None

def get_source(q):
    q = q.lower()
    if "turkey" in q or "skky" in q:
        return "SKKY"
    return "EPA"

def get_ground_truth(param, source):
    if source == "SKKY":
        return DATA["SKKY"].get(param, "Not found")
    if source == "EPA":
        if param == "BOD":
            return DATA["EPA"]["BOD"]["30_day"]
        if param == "TSS":
            return DATA["EPA"]["TSS"]["30_day"]
        return DATA["EPA"].get(param, "Not found")

# =========================
# 🔹 RAG
# =========================
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()
collection = client.get_or_create_collection(name="rag_collection")

docs = [
    "EPA BOD limit 30-day average 30 mg/L",
    "EPA TSS limit 30-day average 30 mg/L",
    "EPA pH range 6.0 to 9.0",
    "SKKY BOD limit 45 mg/L",
    "SKKY COD limit 120 mg/L"
]

embeddings = model.encode(docs).tolist()

collection.add(
    documents=docs,
    embeddings=embeddings,
    ids=[str(i) for i in range(len(docs))]
)

def retrieve_context(query):
    q_emb = model.encode([query]).tolist()
    results = collection.query(query_embeddings=q_emb, n_results=2)
    return " ".join(results["documents"][0])

# =========================
# 🔹 LLM
# =========================
def ask_llm(context, question):
    api_key = os.getenv("GROQ_API_KEY")

    prompt = f"""
Answer the question based ONLY on this context:
{context}

Question: {question}
Answer:
"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0
        }
    )

    data = response.json()

    if "choices" not in data:
        print("\nAPI ERROR RESPONSE:")
        print(data)
        return "LLM failed"

    return data["choices"][0]["message"]["content"]

# =========================
# 🔹 SMART EVALUATOR
# =========================
def extract_numbers(text):
    return re.findall(r"\d+\.?\d*", text)

def normalize(text):
    return text.lower().replace("to", "-").replace(" ", "")

def evaluate(llm_answer, gt_answer):
    llm_nums = extract_numbers(llm_answer)
    gt_nums = extract_numbers(gt_answer)

    # 1️⃣ value strict
    if llm_nums != gt_nums:
        return "incorrect"

    # 2️⃣ format flexible
    llm_clean = normalize(llm_answer)
    gt_clean = normalize(gt_answer)

    if gt_clean in llm_clean:
        return "correct"

    return "correct"  # sayı doğruysa kabul

# =========================
# 🔹 MAIN
# =========================
query = input("Enter your question: ")

param = get_param(query)
if not param:
    print("Parameter not recognized")
    exit()

source = get_source(query)

gt_value = get_ground_truth(param, source)
context = retrieve_context(query)
llm_answer = ask_llm(context, query)
score = evaluate(llm_answer, gt_value)

# =========================
# 🔹 OUTPUT
# =========================
output = {
    "parameter": param,
    "ground_truth": gt_value,
    "llm_answer": llm_answer,
    "evaluation": score,
    "source": source
}

print(json.dumps(output, indent=2))
