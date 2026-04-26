from fastapi import APIRouter, Request

router = APIRouter(prefix="/github", tags=["Webhook"])


@router.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    return {
        "message": "Webhook received",
        "data": payload
    }