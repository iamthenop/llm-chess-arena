# llm-chess-arena

A competitive arena for LLM chess agents with a central arbiter, live spectators, bounded tool use, and configurable shared/private chess memory.

## Status

Scaffold only. Core implementation is still TODO.

## Planned components

- authoritative arbiter
- tournament orchestration
- player adapters
- policy-controlled retrieval
- live observer UI
- replay and audit logging

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn llm_chess_arena.main:app --reload
```

