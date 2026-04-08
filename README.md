# AI-Based Student Counseling Assistant 🎓

A modern, professional web application built with Streamlit, MongoDB, and the OpenAI API. It provides AI-driven career recommendations and 24/7 interactive chat counseling to students.

## Features
- **User Authentication**: Secure Registration and Login mapped to MongoDB.
- **AI Career Mapping**: Parses user skills and interests to suggest the top 3 best-fit careers using GPT-3.5 Turbo.
- **Course Recommendations**: Suggests relevant certifications and courses to match career goals.
- **Chat Counselor**: An interactive ChatGPT-like interface built into the dashboard with conversation history saved securely to MongoDB.
- **Modern UI**: Custom CSS injects gradient buttons, styled cards, and fluid layouts for an impressive User Experience.

## Tech Stack
- Frontend: Streamlit
- Backend / Logic: Python
- Database: MongoDB (Compatible with MongoDB Compass)
- AI Integration: OpenAI API (`gpt-3.5-turbo`)

## Prerequisites
1. **Python 3.9+** installed.
2. **MongoDB** installed and running locally on port 27017, or a remote cluster URI (e.g. MongoDB Atlas).
3. **OpenAI API Key**. Get one from [OpenAI Platform](https://platform.openai.com/).

## Installation & Setup

1. **Navigate to the project folder:**
   Make sure you are in the `K:\PROJECT` directory.

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   - Copy `.env.example` to `.env`:
     ```bash
     copy .env.example .env
     ```
   - Open `.env` and configure your `MONGO_URI` and `OPENAI_API_KEY`:
     ```env
     MONGO_URI="mongodb://localhost:27017/"
     OPENAI_API_KEY="sk-YOUR-API-KEY-HERE"
     ```

5. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

## Database Details
If you open **MongoDB Compass** and connect to `mongodb://localhost:27017/`, you will see a database named `student_counseling_db` containing two collections once you use the app:
1. `users`: Stores registered students (passwords are hashed using bcrypt).
2. `chat_history`: Stores the conversations between students and the AI counselor.
