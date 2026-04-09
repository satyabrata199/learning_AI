import json 
import os

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r") as f:
            content = f.read().strip()

            if not content:  # ✅ empty file
                return []

            return json.loads(content)

    except json.JSONDecodeError:
        print("⚠️ Memory file corrupted, resetting...")
        return []

    
def save_memory(data):
    with open(MEMORY_FILE,"w") as f:
        json.dump(data , f, indent = 2)

def add_memory(entry):
    memory = load_memory()
    memory.append(entry)
    save_memory(memory)
    
def search_memory(query, k=3):
    memory = load_memory()

    if not memory:
        return []

    scored = []

    query_words = set(query.lower().split())

    for entry in memory:
        entry_words = set(entry.lower().split())
        score = len(query_words & entry_words)

        if score > 0:
            scored.append((score, entry))

    # sort by relevance
    scored.sort(reverse=True, key=lambda x: x[0])

    return [entry for _, entry in scored[:k]]
