# LLM Chess Arena Protocol (Draft)

This document defines the communication protocol between **LLM agents** and the **llm-chess-arena arbiter**.

The protocol describes:

* match initialization
* turn payload delivery
* move submission
* error handling
* game termination

The protocol is designed to be simple, deterministic, and easy to implement in connectors for different LLM providers.

---

# Protocol Overview

A match follows this message sequence.

```

AGENT_CONNECT
↓
MATCH_INIT
↓
AGENT_READY
↓
TURN_PAYLOAD
↓
MOVE_SUBMISSION
↓
MOVE_ACCEPTED or MOVE_REJECTED
↓
(next TURN_PAYLOAD)

````

The sequence repeats until the game ends.

---

# Message Transport

The protocol does not require a specific transport.

Possible implementations include:

* HTTP request/response
* WebSocket
* message queues
* local process communication

Regardless of transport, message semantics remain the same.

All messages are structured JSON objects.

---

# Match Initialization

The arbiter begins by sending a `MATCH_INIT` message describing the game environment.

Example:

```json
{
  "type": "MATCH_INIT",
  "protocol_version": "0.1",
  "match_id": "match_001",
  "game_id": "game_001",
  "agent_color": "white",
  "output_format": "uci",
  "retry_policy": {
    "per_turn": 1,
    "per_game": 5
  },
  "budgets": {
    "query_limit": 40
  },
  "tools": [
    "query_similar_positions",
    "query_player_examples"
  ]
}
````

The agent must respond with:

```json
{
  "type": "READY",
  "agent_name": "example-agent",
  "connector_version": "0.1"
}
```

This confirms the agent is ready to begin the game.

---

# Turn Payload

For each move, the arbiter sends a `TURN_PAYLOAD`.

Example:

```json
{
  "type": "TURN_PAYLOAD",
  "match_id": "match_001",
  "turn_index": 17,
  "state": {
    "state_hash": "abc123",
    "side_to_move": "white",
    "legal_moves": ["e2e4", "d2d4", "g1f3"]
  },
  "history": {
    "moves_uci": ["d2d4", "d7d5", "c2c4", "e7e6"]
  },
  "budgets": {
    "turn_retries_used": 0,
    "game_retries_used": 1,
    "queries_used": 9
  }
}
```

The payload always represents the **authoritative game state**.

Agents must rely on this payload rather than reconstructing the board from memory.

---

# Move Submission

Agents respond with a move submission.

Minimal format:

```json
{
  "type": "MOVE",
  "move": "e2e4"
}
```

Optional comment metadata may be included:

```json
{
  "type": "MOVE",
  "move": "e2e4",
  "comment": "Taking central space."
}
```

Rules:

* `move` must be valid **UCI notation**
* exactly one move must be provided
* comments are optional and ignored by the arbiter

---

# Move Acceptance

If the move is legal, the arbiter responds:

```json
{
  "type": "MOVE_ACCEPTED",
  "move": "e2e4",
  "state_hash": "def456"
}
```

The game then proceeds to the next `TURN_PAYLOAD`.

---

# Move Rejection

If the move is illegal or malformed, the arbiter responds:

```json
{
  "type": "MOVE_REJECTED",
  "reason": "illegal_move",
  "submitted_move": "e2e5",
  "retry_allowed": true,
  "retries_remaining": 0
}
```

The agent may retry if allowed.

The authoritative game state does not change.

---

# Retry Policy

Default retry policy:

```
1 retry per turn
global retry limit per game
```

Retries are counted for metrics such as:

* protocol stability
* state drift
* connector reliability

Exceeding retry limits results in **loss by legality failure**.

---

# Game Termination

The arbiter sends `GAME_OVER` when the match ends.

Example:

```json
{
  "type": "GAME_OVER",
  "result": "checkmate",
  "winner": "black",
  "final_state_hash": "xyz789"
}
```

Possible results:

### Chess outcomes

```
checkmate
resignation
draw
```

### Administrative outcomes

```
timeout
protocol_failure
legality_failure
retry_exhaustion
budget_exhaustion
```

---

# State Identity

Every position includes a `state_hash`.

This identifier:

* uniquely represents the board state
* allows deterministic logging
* enables reproducible game records
* supports retrieval queries

State hashes originate from the `chess-gpt` substrate.

---

# Optional Retrieval Tools

Agents may optionally use retrieval tools if enabled.

Examples:

```
query_similar_positions
query_player_examples
query_style_summary
```

Tool invocation mechanisms will be defined separately.

Tool usage may consume query budget.

---

# Protocol Goals

The protocol is designed to ensure:

* deterministic chess state
* minimal ambiguity for agents
* easy connector implementation
* observable agent behavior

The arbiter guarantees chess correctness while agents focus solely on **move selection**.

---

# Versioning

The protocol includes a `protocol_version` field.

Agents should verify compatibility during `MATCH_INIT`.

Breaking changes will increment the major version.