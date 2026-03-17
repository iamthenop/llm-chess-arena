from fastapi import FastAPI

from llm_chess_arena.api.routes import health, matches, players, spectators, tournaments, admin

app = FastAPI(title="llm-chess-arena", version="0.1.0")

app.include_router(health.router)
app.include_router(matches.router, prefix="/matches", tags=["matches"])
app.include_router(tournaments.router, prefix="/tournaments", tags=["tournaments"])
app.include_router(players.router, prefix="/players", tags=["players"])
app.include_router(spectators.router, prefix="/spectators", tags=["spectators"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

