from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "llm-chess-arena"
    env: str = "dev"
    log_level: str = "INFO"

