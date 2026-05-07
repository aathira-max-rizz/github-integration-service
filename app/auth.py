import base64
import os
import requests

from dotenv import load_dotenv
from fastapi import APIRouter, Request, Body, Header
from fastapi.responses import RedirectResponse

from app.db import get_connection

load_dotenv()

# ✅ Router
router = APIRouter(
    prefix="/github",
    tags=["GitHub Auth"]
)

# ✅ GitHub OAuth credentials
CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")


# =========================================================
# 🔹 STEP 1: GitHub Login
# =========================================================
@router.get("/auth")
def github_login():

    github_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={CLIENT_ID}&scope=repo"
    )

    return RedirectResponse(github_url)


# =========================================================
# 🔹 STEP 2: GitHub Callback
# =========================================================
@router.get("/callback")
def github_callback(request: Request):

    code = request.query_params.get("code")

    if not code:
        return {"error": "No code received from GitHub"}

    # ✅ Exchange code for access token
    token_response = requests.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code
        },
        headers={
            "Accept": "application/json"
        }
    )

    token_json = token_response.json()

    access_token = token_json.get("access_token")

    if not access_token:
        return {
            "error": "Failed to get access token",
            "details": token_json
        }

    # =====================================================
    # ✅ Encode token before storing
    # =====================================================
    encoded_token = base64.b64encode(
        access_token.encode()
    ).decode()

    # =====================================================
    # ✅ Store token in PostgreSQL
    # =====================================================
    try:

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO github_tokens (token)
            VALUES (%s)
            """,
            (encoded_token,)
        )

        conn.commit()

        cur.close()
        conn.close()

        print("✅ Token stored in DB")

    except Exception as e:
        print("❌ Database error:", e)

    # =====================================================
    # ✅ Fetch user repositories
    # =====================================================
    repos_response = requests.get(
        "https://api.github.com/user/repos",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    repos = repos_response.json()

    clean_repos = []

    for repo in repos:
        clean_repos.append({
            "name": repo["name"],
            "url": repo["html_url"]
        })

    return {
        "message": "Authentication successful",
        "repo_count": len(clean_repos),
        "repos": clean_repos[:5],
        "note": "Token stored in PostgreSQL (encoded)"
    }


# =========================================================
# 🔹 STEP 3: Create New Private Repo
# =========================================================
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


# =========================================================
# 🔹 STEP 4: Get User Repositories
# =========================================================
@router.get("/repos")
def get_repos(
    authorization: str = Header(None)
):

    if not authorization:
        return {"error": "Missing Authorization header"}

    access_token = authorization.replace("Bearer ", "")

    response = requests.get(
        "https://api.github.com/user/repos",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    repos = response.json()

    return [
        {
            "name": repo["name"],
            "url": repo["html_url"]
        }
        for repo in repos
    ]