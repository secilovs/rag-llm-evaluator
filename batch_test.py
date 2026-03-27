from main import (
    get_param,
    get_source,
    get_ground_truth,
    retrieve_context,
    ask_llm,
    evaluate
)
import json

# 🔹 TEST SETİ
questions = [
    "BOD limit EPA?",
    "TSS limit EPA?",
    "pH limit EPA?",
    "COD limit SKKY?",
    "BOD limit SKKY?",
    "TSS limit Turkey?",
    "pH limit SKKY?",
    "What is BOD limit EPA?",
    "COD Turkey limit?",
    "ph skky???",
    "bod epa pls",
    "BOD limit Turkey EPA?"
]

correct = 0
total = len(questions)

results = []

for q in questions:
    print(f"\n Question: {q}")

    param = get_param(q)
    source = get_source(q)

    if not param:
        print("Parameter not recognized")
        continue

    gt_value = get_ground_truth(param, source)
    context = retrieve_context(q)
    llm_answer = ask_llm(context, q)
    score = evaluate(llm_answer, gt_value)

    if score == "correct":
        correct += 1

    result = {
        "question": q,
        "parameter": param,
        "source": source,
        "ground_truth": gt_value,
        "llm_answer": llm_answer,
        "evaluation": score
    }

    results.append(result)

    print(json.dumps(result, indent=2))

# 🔹 ACCURACY
accuracy = (correct / total) * 100

print("\n===================")
print(f"Total: {total}")
print(f"Correct: {correct}")
print(f"Accuracy: {accuracy:.2f}%")
print("===================")
