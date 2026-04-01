import requests
import json
from tools import calculator , save_note 
from memory import load_memory , add_memory

Ollma_url = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = """
You are an AI assistant with access to tools.

Available tools:
1. calculator(expression)
2. save_note(note)

STRICT RULES:
- You MUST ALWAYS return a valid JSON object.
- Do NOT include any text before or after the JSON.
- Do NOT use markdown, code blocks, or explanations.
- The response MUST be parseable by json.loads().
- Use double quotes (") for all keys and string values.
- Do NOT use trailing commas.
- The JSON must follow EXACTLY this schema:

{
  "action": "respond OR calculator OR save_note",
  "input": "string"
}

Action rules:
- Use "calculator" ONLY for mathematical expressions.
- Use "save_note" ONLY when the user asks to remember something.
- Use "respond" for all other cases.

Input rules:
- "input" must ALWAYS be a string.
- For calculator, input must be a valid mathematical expression.
- For save_note, input must be the exact note to save.
- For respond, input must be a natural language reply.

ERROR HANDLING:
- If unsure, default to:
  {"action": "respond", "input": "I’m not sure how to help with that."}

VALIDATION CHECKLIST (before responding):
- Is it valid JSON?
- Are all keys present? ("action", "input")
- Is "action" one of the allowed values?
- Is "input" a string?

Examples:

User: what is 2+2
Output:
{"action": "calculator", "input": "2+2"}

User: remember I like python
Output:
{"action": "save_note", "input": "I like python"}

User: hello
Output:
{"action": "respond", "input": "Hello! How can I help?"}
"""

def ask(prompt):
    response = requests.post(Ollma_url, json={
        "model":"gemma2:2b",
        "prompt":prompt,
        "stream":False,
    })

    return response.json()["response"]

def clean_output(output):
    output = output.strip()

    if output.startswith("```"):
        parts = output.split("```")
        if len(parts) >= 2:
            output = parts[1]
            if output.startswith("json"):
                output = output[4:]

    return output.strip()

def run_agent(user_input):

    memory = load_memory()
    memory_contetxt = "\n".join(memory[-5:])

    full_prompt = f"{SYSTEM_PROMPT}\n previous context: {memory_contetxt}\nUser: {user_input}\nOutput:"

    for _ in range(2):
        output = ask(full_prompt)
        cleaned = clean_output(output)
        try:
            action_data = json.loads(cleaned)
            break
        except:
            continue

    else:
        print("RAW OUTPUT:", output)
        return "Error: Model didn't return valid JSON"

    action = action_data.get("action")
    inp = action_data.get("input")

    if not action or inp is None:
        return "Error: Missing fields in JSON"

    if action == "calculator":
        result = calculator(inp)
    elif action == "save_note":
        result = save_note(inp)
    elif action == "respond":
        result = inp
    else:
        result = "unknown action"
    
    add_memory(f"User: {user_input}")
    add_memory(f"Agent: {result}")

    return result

while True :
    user_input = input("you: ")

    if user_input.lower() == "bye":
        break

    reply = run_agent(user_input)
    print("agent:", reply)

