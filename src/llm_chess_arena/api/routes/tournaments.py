from fastapi import APIRouter

router = APIRouter()


@router.get("")
def list_tournaments() -> dict[str, list]:
    return {"tournaments": []}

