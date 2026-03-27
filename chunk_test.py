def chunk_text(text, chunk_size=100, overlap=20):   
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


# test text
text = """
Effluent limitations for secondary treatment require BOD5 to be 30 mg/L.
Total Suspended Solids must also be 30 mg/L.
pH should be maintained between 6.0 and 9.0.
"""

chunks = chunk_text(text, chunk_size=10, overlap=2)
for i, c in enumerate(chunks):
    print(f"\n--- CHUNK {i} ---")
    print(c)
