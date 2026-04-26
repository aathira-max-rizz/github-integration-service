from fastapi import APIRouter, Request, Body, Header
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import requests
import os

load_dotenv()

router = APIRouter(prefix="/github", tags=["GitHub Auth"])

CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")


# 🔹 Step 1: Redirect to GitHub
@router.get("/auth")
def github_login():
    github_url = f"https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&scope=repo"
    return RedirectResponse(github_url)


# 🔹 Step 2: Callback
@router.get("/callback")
def github_callback(request: Request):
    code = request.query_params.get("code")

    if not code:
        return {"error": "No code received from GitHub"}

    token_response = requests.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code
        },
        headers={"Accept": "application/json"}
    )

    token_json = token_response.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return {"error": token_json}

    # fetch repos
    repos_response = requests.get(
        "https://api.github.com/user/repos",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    repos = repos_response.json()

    clean_repos = [
        {"name": repo["name"], "url": repo["html_url"]}
        for repo in repos
    ]

    return {
        "message": "Authentication successful",
        "repo_count": len(clean_repos),
        "repos": clean_repos[:5],
        "note": "Token not stored yet (DB pending)"
    }


# 🔹 Step 3: Create Repo
@router.post("/create-repo")
def create_repo(
    repo_name: str = Body(...),
    authorization: str = Header(None)
):
    if not authorization:
        return {"error": "Missing Authorization header"}

    access_token = authorization.replace("Bearer ", "")

    repo_response = requests.post(
        "https://api.github.com/user/repos",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json"
        },
        json={
            "name": repo_name,
            "private": True
        }
    )

    return repo_response.json()