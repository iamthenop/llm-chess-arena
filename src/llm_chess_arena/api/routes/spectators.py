from fastapi import APIRouter

router = APIRouter()


@router.get("")
def spectator_feed() -> dict[str, list]:
    return {"events": []}

