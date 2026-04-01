def calculator(expression):
    try:
        return str(eval(expression))
    except:
        return "Error in calculation"

def save_note(note):
    with open("notes.txt", "a") as f:
        f.write(note + "\n")
    return "Note saved!"