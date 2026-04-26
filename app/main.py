from fastapi import FastAPI
from app.auth import router as auth_router
from app.github import router as github_router
from app.webhook import router as webhook_router

app = FastAPI()

# include routers
app.include_router(auth_router)
app.include_router(github_router)
app.include_router(webhook_router)

# root check
@app.get("/")
def root():
    return {"message": "Server is running 🚀"}