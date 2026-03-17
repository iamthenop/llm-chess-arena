# LLM Chess Arena – Agent Model (Draft)

This document defines what an **agent** is within `llm-chess-arena`.

Agents are the entities that **choose chess moves** during a match.

The arena treats agents as external decision systems operating under
a controlled environment.

---

# Definition

An **agent** is a system that:

1. receives a game state from the arena
2. optionally gathers additional context
3. selects exactly one move
4. returns that move to the arbiter

Agents do not enforce chess rules or maintain authoritative board state.

---

# System Layers

The arena architecture separates responsibilities into three layers.

```

chess-gpt       → chess state machine
arena           → match orchestration
agent           → move selection

```


Connectors act as adapters between the arena protocol and the agent’s model.

```

arena arbiter
│
▼
connector
│
▼
agent (LLM or other decision system)

```

---

# Agent Responsibilities

Agents are responsible for:

* choosing moves
* interpreting state payloads
* deciding whether to use retrieval tools
* managing their resource budgets

Agents are **not responsible for**:

* validating moves
* enforcing chess rules
* updating board state
* managing the game clock

These are handled by the arena and `chess-gpt`.

---

# Agent Inputs

Each turn an agent receives a structured payload containing:

* current game state
* legal moves
* move history
* retry counters
* resource budgets

This payload represents the **authoritative state of the game**.

Agents must rely on this payload rather than reconstructing board state from memory.

---

# Agent Outputs

Agents must return exactly one move.

Required format:

```

e2e4
g1f3
c7c5

```

Moves must use **UCI notation**.

Optional metadata may be attached by the connector, such as comments.

---

# Agent Types

The arena does not restrict how agents are implemented.

Examples include:

### LLM Agents

Large language models that choose moves based on prompts.

Examples:

* GPT-based agents
* Claude-based agents
* local open-weight models

### Programmatic Agents

Traditional programs that follow deterministic rules.

Examples:

* random move agent
* heuristic-based agents
* scripted opening players

### Hybrid Agents

Systems combining multiple techniques.

Examples:

* LLM + retrieval
* LLM + heuristics
* LLM + planning modules

---

# Agent Memory

Agents may optionally maintain internal memory.

Examples:

* cached analysis
* private notes
* retrieved examples
* prior games

However, agents must always treat the **arena payload as authoritative**.

Internal memory should never override the official state.

---

# Agent Resource Constraints

Agents may operate under constraints defined by the arena.

Examples include:

* retry limits
* retrieval query budgets
* time limits

Agents are responsible for deciding how to allocate these resources.

---

# Agent Observability

The arena may record agent behavior for analysis.

Possible recorded data includes:

* chosen moves
* retry usage
* query usage
* optional comments
* decision timing

This allows comparison between agents across many games.

---

# Agent Identity

Agents participating in a match should provide identifying information.

Typical metadata includes:

```

agent_name
model_name
connector_version
strategy_type

```

This information is recorded in match logs for reproducibility.

---

# Goals of the Agent Model

The arena is designed to evaluate **agent behavior under controlled conditions**.

Key experimental variables include:

* model architecture
* retrieval strategies
* style conditioning
* resource limits

By externalizing chess rules, the arena isolates the **decision-making capabilities of the agent**.

---

# Future Agent Features

Potential future capabilities include:

* tool-based retrieval
* multi-step planning loops
* structured reasoning traces
* collaborative agents
* adaptive strategies across games

These features will evolve as the arena develops.