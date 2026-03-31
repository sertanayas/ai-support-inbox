# AI Support Inbox

AI Support Inbox is a bilingual customer support message analysis dashboard built with FastAPI and SQLite.

## Features
- Customer message submission form
- Category detection
- Sentiment analysis
- Priority tagging
- Suggested reply generation
- English / Turkish language support
- Filter by category
- Filter by priority
- Delete single record
- Delete all records

## Tech Stack
- Python
- FastAPI
- SQLite
- SQLAlchemy
- Jinja2
- HTML
- CSS

## Project Structure
- app/
- templates/
- static/
- requirements.txt
- README.md

## Run the Project
1. Install dependencies:
   pip install -r requirements.txt

2. Start the server:
   python -m uvicorn app.main:app --reload

3. Open in browser:
   http://127.0.0.1:8000

## Purpose
This project was developed as a portfolio project to demonstrate backend development, dashboard design, bilingual support workflows, and customer support process automation.

## Future Improvements
- Real AI API integration
- Automatic language detection
- Export records as CSV
- Dashboard analytics