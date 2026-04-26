from fastapi import FastAPI
from app.auth import router as auth_router
from app.webhook import router as webhook_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(webhook_router)

@app.get("/")
def root():
    return {"message": "Server is running 🚀"}