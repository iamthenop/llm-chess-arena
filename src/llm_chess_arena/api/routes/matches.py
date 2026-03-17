from fastapi import APIRouter

router = APIRouter()


@router.get("")
def list_matches() -> dict[str, list]:
    return {"matches": []}

