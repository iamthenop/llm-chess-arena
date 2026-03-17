# LLM Chess Arena – Design Overview (Draft)

This document describes the architectural design and guiding principles of **llm-chess-arena**.

The arena is an environment where LLM agents compete in chess games while an external substrate (`chess-gpt`) maintains authoritative game state.

This document focuses on **system design and responsibilities**, not the exact message protocol.

---

# Core Philosophy

The arena separates **chess reality** from **agent decision-making**.

```

chess-gpt      → authoritative chess state machine
arena arbiter  → match orchestration
LLM agents     → move selection

```

Responsibilities are intentionally minimal and clearly separated.

| Component | Responsibility |
|----------|---------------|
| chess-gpt | board state, legality, deterministic transitions |
| arena arbiter | match control, turn sequencing, retry rules |
| LLM agent | choose a move |

Agents never need to reconstruct board state or enforce chess rules themselves.

---

# System Architecture

The arena sits between agents and the chess substrate.

```

LLM Agent
│
▼
Arena Arbiter
│
▼
chess-gpt

```

Flow of control:

```

agent proposes move
↓
arbiter validates through chess-gpt
↓
new canonical state
↓
next agent receives updated payload

```

The arbiter ensures all state transitions are valid.

---

# Agent Model

Agents are treated as **external decision modules**.

Each agent:

* receives a structured game state
* optionally accesses additional context or retrieval tools
* outputs exactly one move

Agents are **not responsible for rule enforcement**.

---

# Match Lifecycle

A match proceeds through several stages.

### 1. Agent Registration

Agents connect to the arena and identify themselves.

### 2. Match Initialization

The arena sends configuration describing:

* match identifier
* player color
* retry limits
* resource budgets
* available tools

### 3. Turn Loop

Each turn follows this pattern:

```

TURN_PAYLOAD
↓
agent selects move
↓
arbiter validates move
↓
state update
↓
next TURN_PAYLOAD

```

### 4. Game End

A game ends due to:

* checkmate
* resignation
* draw
* administrative failure

Results are recorded for analysis.

---

# Illegal Move Handling

The arena tracks agent stability.

If an agent submits an illegal move:

```

illegal move → rejected
state remains unchanged
agent receives retry opportunity

```

Default policy:

* 1 retry per turn
* global retry limit per game

Exceeding retry limits results in **loss by legality failure**.

This mechanism allows measurement of **state drift and protocol errors**.

---

# Resource Budgets

Matches may enforce limits on agent behavior.

Examples:

* retries per turn
* retries per game
* retrieval queries
* computation time

Resource usage is tracked for later analysis of agent strategies.

---

# State Authority

The arena does not maintain chess rules internally.

All chess legality and state transitions are delegated to **chess-gpt**.

The arena trusts the substrate for:

* legal move generation
* board transitions
* canonical state identity

This guarantees that:

* game state is always correct
* agents cannot corrupt the board
* retries do not modify state

---

# Information Channels

Agents receive two types of information.

### State Channel (mandatory)

Information required to play the game:

* board state
* legal moves
* move history
* current budgets

### Policy Channel (optional)

Additional information that may influence decision making:

* player style corpora
* historical examples
* opening context
* statistical priors

These sources may be delivered through retrieval tools.

---

# Spectator Support

The arena may support spectators.

Spectators can observe:

* game state
* move sequence
* optional agent comments

Agent comments are considered **non-authoritative metadata** and do not affect gameplay.

---

# Goals of the Arena

The arena is designed to study **agent behavior**, not engine strength.

The system allows experimentation with:

* different LLM architectures
* retrieval strategies
* style conditioning
* resource constraints
* decision stability

By externalizing chess rules, the arena isolates the **decision-making capabilities of the agent**.

---

# Relationship to chess-gpt

`chess-gpt` provides the deterministic chess substrate.

The arena depends on it for:

* canonical position encoding
* move legality enforcement
* state transitions
* structured payload generation

The arena itself remains lightweight and focused on orchestration.

---

# Future Design Areas

Several aspects of the arena remain under active design:

* agent communication protocol
* retrieval tool interface
* tournament orchestration
* spectator event streams
* agent connector framework

These will be documented separately as the project evolves.