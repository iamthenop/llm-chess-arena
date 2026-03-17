from fastapi import APIRouter

router = APIRouter()


@router.get("")
def admin_status() -> dict[str, str]:
    return {"status": "todo"}

