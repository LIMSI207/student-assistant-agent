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
    get_student_statistics,
    export_students_csv,
)

from auth import init_auth_db, register_user, login_user
from database import init_db, add_student, search_student, list_students, count_students, update_student, delete_student, get_student_statistics

load_dotenv()

init_db()
init_auth_db()

api_key = os.getenv("GOOGLE_API_KEY")
model_id = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not api_key:
    raise ValueError("GOOGLE_API_KEY .env file ma set karo.")


def create_agent():
    return Agent(
        model=Gemini(id=model_id, api_key=api_key),
        tools=[
            add_student,
            search_student,
            list_students,
            count_students,
            update_student,
            delete_student,
            get_student_statistics,
            export_students_csv,
        ],
        instructions=[
            "You are a helpful Student Assistant.",
            "Answer general questions naturally.",
            "For student questions, use database tools and never invent data.",
            "Before deleting or editing a record, ask the user to confirm the student ID and changes.",
            "Never claim an operation succeeded unless the tool result confirms it.",
            "Reply in the same language as the user.",
            "Always export student records to students_report.csv",
            "create a different filename for CSV export."
        ],
        markdown=True,
    )


def assistant_session(user):
    agent = create_agent()
    print(f"\nWelcome, {user['name']}!")
    print("Student Assistant ready. Type 'logout' to log out.")

    while True:
        question = input("\nYou: ").strip()

        if question.lower() == "logout":
            print("Logged out successfully.")
            break

        if question.lower() in {"exit", "quit"}:
            print("Please type 'logout' to return to the login menu.")
            continue

        if not question:
            continue

        try:
            agent.print_response(question, stream=False)
        except Exception as error:
            print("Request failed:", type(error).__name__, str(error))


def main():
    while True:
        print("\n===== Student Assistant =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose (1-3): ").strip()

        if choice == "1":
            name = input("Name: ").strip()
            email = input("Email: ").strip()
            password = input("Password (minimum 8 characters): ")

            success, message = register_user(name, email, password)
            print(message)

        elif choice == "2":
            email = input("Email: ").strip()
            password = input("Password: ")

            user = login_user(email, password)

            if user:
                assistant_session(user)
            else:
                print("Invalid email or password.")

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()