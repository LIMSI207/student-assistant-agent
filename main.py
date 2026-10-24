
import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.google import Gemini

from database import (
    init_db,
    add_student,
    search_student,
    list_students,
    count_students,
    update_student,
    delete_student,
)

load_dotenv()
init_db()

api_key = os.getenv("GOOGLE_API_KEY")
model_id = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not api_key:
    raise ValueError("GOOGLE_API_KEY .env file ma set karo.")

agent = Agent(
    model=Gemini(id=model_id, api_key=api_key),
    tools=[
        add_student,
        search_student,
        list_students,
        count_students,
        update_student,
        delete_student,
    ],
    instructions=[
        "You are a helpful Student Assistant.",
        "Answer general questions naturally.",
        "For student questions, use database tools and never invent data.",
        "Before deleting or editing a record, ask the user to confirm the student ID and changes.",
        "Never claim an operation succeeded unless the tool result confirms it.",
        "Reply in the same language as the user.",
    ],
    markdown=True,
)

print("Student Assistant is ready. Type 'exit' to stop.")

while True:
    question = input("\nYou: ").strip()

    if question.lower() in {"exit", "quit"}:
        print("Goodbye!")
        break

    if not question:
        continue

    try:
        agent.print_response(question, stream=False)
    except Exception as error:
        print("Request failed:", type(error).__name__, str(error))
