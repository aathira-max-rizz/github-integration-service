from fastapi import APIRouter
from pydantic import BaseModel
import os
from git import Repo

router = APIRouter(prefix="/github", tags=["GitHub Repo"])


class CloneRequest(BaseModel):
    repo_url: str


@router.post("/clone")
def clone_repo(data: CloneRequest):
    try:
        repo_url = data.repo_url

        repo_name = repo_url.split("/")[-1].replace(".git", "")
        clone_path = f"./cloned_repos/{repo_name}"

        os.makedirs("cloned_repos", exist_ok=True)

        Repo.clone_from(repo_url, clone_path)

        return {
            "message": "Repository cloned successfully",
            "path": clone_path
        }

    except Exception as e:
        return {"error": str(e)}