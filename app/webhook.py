from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/github/webhook")
async def github_webhook(request: Request):
    payload = await request.json()
    return {"received": payload}