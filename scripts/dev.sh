#!/usr/bin/env bash
set -euo pipefail
uvicorn llm_chess_arena.main:app --reload

