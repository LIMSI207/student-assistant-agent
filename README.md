# Student Assistant Agent

An AI-powered Student Assistant built using Python, Agno, Google Gemini, and SQLite.

## Features
- Answers general questions using Google Gemini.
- Searches student records.
- Lists students and counts student records.
- Supports adding, updating, and deleting student records through database tools.
- Stores student data in an SQLite database.

## Technologies Used
- Python
- Agno
- Google Gemini
- SQLite
- python-dotenv

## Setup Instructions

1. Clone this repository:
   `git clone https://github.com/LIMSI207/student-assistant-agent.git`

2. Open the project folder:
   `cd student-assistant-agent`

3. Create and activate a virtual environment:
   `python -m venv .venv`

   Windows PowerShell:
   `.\.venv\Scripts\Activate.ps1`

4. Install dependencies:
   `pip install -r requirements.txt`

5. Create a `.env` file in the project folder and add your Gemini API key:
   `GOOGLE_API_KEY=your_api_key_here`

6. Run the application:
   `python main.py`

## Security
Never upload your API key or `.env` file to GitHub.

## Author
LIMSI207