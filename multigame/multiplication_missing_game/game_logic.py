
import random

def generate_question():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    c = a * b

    hide = random.choice(["a", "b", "c"])

    if hide == "a":
        question = f"_ × {b} = {c}"
        answer = a
    elif hide == "b":
        question = f"{a} × _ = {c}"
        answer = b
    else:
        question = f"{a} × {b} = _"
        answer = c

    return question, answer

def check_answer(user_answer, correct_answer):
    return user_answer == correct_answer
