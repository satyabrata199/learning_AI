from ddgs import DDGS

def calculator(expression):
    try:
        print(f"🧮 Calculating: {expression}")
        allowed_names = {"__builtins__": None}
        return str(eval(expression, allowed_names, {}))
    except:
        return "Error in calculation"

def save_note(note):
    print(f"📝 Saving note: {note}")
    with open("notes.txt", "a") as f:
        f.write(f"[NOTE] {note}\n")
    return "Note saved!"

def web_search(query):
    try:
        print(f"🌐 Web search called: {query}")
        results = []

        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=3):
                results.append(f"{r['title']} - {r['body']}")

        return "\n".join(results)

    except Exception as e:
        return f"Search error: {str(e)}"