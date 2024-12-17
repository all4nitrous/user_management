from fastapi import APIRouter

router = APIRouter()

@router.get("/invitations", tags=["invitations"])
async def get_invitations():
    return {"message": "Here are the invitations"}
