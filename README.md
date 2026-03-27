# 🔍 RAG + LLM Evaluation System

![LLM Evaluation Engine](llm_evaluation_engine_800x600.png)

A deterministic evaluation framework that tests whether an LLM provides correct answers based on environmental regulation data (EPA & SKKY).


## 🚨 Why This Project Exists

LLMs often generate answers that sound correct but are factually wrong (hallucinations).  
This makes them unreliable in domains where accuracy is critical, such as environmental regulations.

This project addresses a key question:

**"Is the model actually correct — or just sounding correct?"**

---

## 🎯 What This System Does

This is not a chatbot.

It is an **evaluation engine** that:
- generates answers using an LLM
- validates them against real-world regulatory data
- produces an objective correctness decision

---

## 🧠 System Architecture

User Question  
↓  
RAG Pipeline (ChromaDB + Sentence Transformers)  
↓  
LLM (Groq API – Llama 3.1)  
↓  
Ground Truth Engine (rule-based, deterministic)  
↓  
Evaluator (numeric + semantic comparison)

---

## ⚙️ Core Capabilities

- Deterministic ground truth validation (no LLM bias)
- Numeric extraction using regex
- Rule-based correctness checking
- RAG-based context retrieval
- Batch evaluation for scalability
- Quantitative accuracy metrics

---

## 🧠 Evaluation Pipeline

1. **Ground Truth Retrieval**  
   Regulatory values (EPA & SKKY) are retrieved via RAG

2. **Answer Parsing**  
   Extract key parameters (BOD, COD, pH) using regex

3. **Deterministic Comparison**  
   - Exact match → correct  
   - Mismatch → incorrect  

4. **Semantic Validation**  
   - Relevance to question  
   - Consistency with retrieved context  

5. **Final Decision**  
   Output: `correct` / `incorrect`

---

## 📊 Example Output

Input:
pH limit EPA?

Output:
{
  "parameter": "PH",
  "ground_truth": "6.0-9.0",
  "llm_answer": "The pH limit according to the EPA is 6.0 to 9.0.",
  "evaluation": "correct",
  "source": "EPA"
}

Batch Result:
Total: 12 | Correct: 11 | Accuracy: 91.67%

---

## 📦 Tech Stack

| Component       | Technology                  |
|----------------|---------------------------|
| Language        | Python 3.10+              |
| Vector Store    | ChromaDB                  |
| Embeddings      | Sentence Transformers     |
| LLM             | Groq (Llama 3.1)          |
| Parsing         | Regex                     |

---

## 🚀 Getting Started

git clone https://github.com/secilovs/rag-llm-evaluator.git  
cd rag-llm-evaluator  
pip install -r requirements.txt  
python main.py  

Set API key:

export GROQ_API_KEY=your_key_here

---

## ⚠️ Limitations

- Ambiguous queries may fail (e.g., missing source)
- Limited to EPA and SKKY datasets
- Basic source detection logic

---

## 🔮 Roadmap

- Improved query understanding (NER / intent detection)
- Multi-source conflict resolution
- Expanded regulatory datasets
- Advanced evaluation metrics (RAGAS)

---

## 💡 Key Insight

Fluency ≠ correctness.

This system enforces **deterministic evaluation using ground truth data**, ensuring that LLM outputs are not only relevant but factually accurate.

Unlike typical evaluation approaches:
- it does not rely on LLM self-judgment  
- it provides objective, rule-based validation  

---

## 🎯 Why It Matters

This project demonstrates the ability to:

- evaluate LLM outputs beyond surface-level fluency
- design deterministic validation systems
- build reliable pipelines for high-stakes domains

Applicable to:
- AI evaluation roles
- LLM QA / benchmarking systems
- regulatory and compliance-focused AI applications
