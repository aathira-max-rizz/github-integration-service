# GitHub Integration Microservice

## 🚀 Features
- GitHub OAuth Login
- Fetch user repositories
- Create new repositories

## 🛠 Tech Stack
- Python
- FastAPI
- Requests

## ▶️ How to Run

1. Install dependencies:
pip install fastapi uvicorn requests python-dotenv

2. Run server:
uvicorn app.main:app --reload

3. Open in browser:
http://127.0.0.1:8000/github/auth

## 📌 Endpoints

- /github/auth → Login with GitHub
- /github/callback → Get token & repos
- /github/create-repo → Create repo