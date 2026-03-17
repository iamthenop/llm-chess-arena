# LLM Chess Arena – Connector Guide (Draft)

This document describes how **LLM connectors** integrate agents with the
`llm-chess-arena` protocol.

A connector is a lightweight adapter that translates between:

```

arena protocol  ↔  LLM provider API

```

The connector is responsible for formatting prompts, parsing responses,
and enforcing protocol constraints.

---

# Role of a Connector

A connector acts as the interface between the arena and a specific model.

```

arena arbiter
│
▼
connector
│
▼
LLM provider

```

Responsibilities of a connector:

| Responsibility | Description |
|----------------|-------------|
| protocol handling | receive arena messages and respond correctly |
| prompt construction | convert turn payload into LLM prompt |
| response parsing | extract a single move from the model output |
| validation | ensure move format is valid before submission |
| retry handling | respond correctly to rejection messages |

The connector must ensure the model follows the arena protocol.

---

# Connector Loop

A typical connector loop looks like this:

```

receive TURN_PAYLOAD
↓
construct prompt
↓
call LLM API
↓
extract move
↓
submit MOVE
↓
handle response

```

The connector repeats this process until `GAME_OVER`.

---

# Prompt Construction

The connector converts the arena payload into a prompt suitable for the LLM.

Example prompt structure:

```

You are playing a game of chess.

The environment maintains the board state and enforces rules.

Choose exactly one move in UCI format.

Current position:
legal moves: e2e4 d2d4 g1f3

Move history:
d2d4 d7d5 c2c4 e7e6

Output only the move.

```

Connectors may add formatting improvements, but must not change the
information contained in the payload.

---

# Required Output Format

Agents must produce exactly one move in **UCI format**.

Examples:

```

e2e4
g1f3
c7c5

```

If the connector cannot extract a valid move, it should treat the response
as malformed and retry if allowed.

---

# Parsing Strategy

Connectors should use a strict parsing rule.

Recommended strategy:

1. search for a valid UCI move in the response
2. ignore additional commentary
3. submit only the move

Example model response:

```

I will play e2e4 to control the center.

```

Parsed move:

```

e2e4

```

If no valid move is found, the connector should return a malformed move
response.

---

# Handling Move Rejection

If the arbiter responds with:

```

MOVE_REJECTED

```

The connector should:

```

receive rejection
↓
update retry counter
↓
generate new prompt
↓
request new move from LLM

````

The connector must respect retry limits defined in the protocol.

---

# Optional Comments

Connectors may attach optional comments to move submissions.

Example:

```json
{
  "type": "MOVE",
  "move": "e2e4",
  "comment": "Taking central space."
}
````

Comments are ignored by the arbiter and are intended only for:

* spectator logs
* PGN annotations
* debugging

---

# Example Connector Types

The arena can support connectors for many LLM providers.

Examples:

| Provider     | Connector             |
| ------------ | --------------------- |
| OpenAI       | `openai_connector.py` |
| Anthropic    | `claude_connector.py` |
| Groq         | `groq_connector.py`   |
| Local models | `local_connector.py`  |

Each connector implements the same protocol but uses a different API.

---

# Minimal Connector Pseudocode

Example control loop:

```
while game_active:

    payload = receive_turn_payload()

    prompt = build_prompt(payload)

    response = call_llm(prompt)

    move = parse_move(response)

    submit_move(move)

    result = receive_response()

    if result == GAME_OVER:
        break
```

---

# Connector Goals

Connectors should aim for:

* protocol compliance
* reliable move extraction
* minimal prompt complexity
* deterministic behavior where possible

Connectors should avoid adding unnecessary logic that could bias
agent behavior.

---

# Future Connector Features

Future improvements may include:

* tool-enabled retrieval
* structured reasoning traces
* multi-step planning loops
* model-specific optimization strategies

These features should remain **connector-level**, not part of the arena protocol.