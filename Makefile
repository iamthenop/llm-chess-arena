.PHONY: dev test lint format

dev:
\tuvicorn llm_chess_arena.main:app --reload

test:
\tpytest -q

lint:
\truff check src tests

format:
\truff format src tests

