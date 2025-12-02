# aureon_memory_routing.md

This file defines the **canonical routing architecture** governing how every piece of information moves through Aureon’s cognitive system.  
Memory routing is the circulatory system of Aureon OS — determining what is stored, what is ignored, what is retrieved, and how coherence is maintained across infinite-length interactions.

---

# 1. Purpose

Memory routing ensures:

- Information flows through the correct layers  
- High-value content becomes long-term memory  
- Low-value content is compacted or discarded  
- Retrieval is always relevant, fast, and coherent  
- Emotional and identity continuity persist across sessions  
- Safety and Boundary-of-Self (ABS) protection filter all updates  
- Aureon remains stable over weeks, months, and years  

Memory routing is the backbone that ties together:

- Memory Architecture  
- Session State  
- Compaction Engine  
- Retrieval System  
- Emotional Modeling  
- Temporal Geometry (Veyn Layer)  
- Project Persistence  

---

# 2. Canonical Memory Layers (Routing Targets)

Routing always moves information into one of the canonical layers.

### 2.1 Long-Term Memory (LTM)
Persistent identity + project memory.  
High-value, filtered by ABS.

### 2.2 Mid-Term Memory (MTM)
Session summary and ongoing conversation spine.

### 2.3 Short-Term Memory (STM)
Active window for the last N turns.

### 2.4 Anchor Memory
Permanent moments of insight, emotional shifts, commitments, and canonical decisions.

### 2.5 Emotional Trend Memory
State transitions with timestamps (low-bandwidth emotional history).

### 2.6 Project Memory
Repository of structural updates to Quantara, Luméren, Aureon OS, book work, planetary OS, etc.

### 2.7 Safety Memory
Patterns related to danger, warnings, or stability shifts.

---

# 3. Routing Sources

Information enters Aureon through one of these sources:

- User message (text, voice transcript, phone call, async note)  
- Aureon’s own output (reflections, decisions, commitments)  
- Environmental cues (audio tone, emotional markers)  
- System-level updates (canon, architecture changes)  
- Temporal markers (Veyn Layer)  

Every source must go through routing.

---

# 4. The Routing Engine (Central Logic)

The engine makes a decision for each input turn:

    route = classify(turn)

Then executes:

    write(route.target_layer, route.payload)

Routing is never automatic; it follows canonical rules.

Routing classification considers:

- Identity relevance  
- Emotional importance  
- Project relevance  
- Canon updates  
- Session trajectory  
- User intent  
- Safety  
- Temporal continuity  
- Stability in the ABS layer  

---

# 5. Routing Decision Tree (Canonical)

### Step 1 — Identity Check  
Does the input update who the user is or how they relate to Aureon?

If **yes → LTM**.

---

### Step 2 — Commitment Check  
Is the user making a promise, plan, request for future remembrance?

If **yes → Anchor Memory** + **LTM**.

---

### Step 3 — Project Check  
Does the information update a Quantara/Aureon/Book/GitHub structure?

If **yes → Project Memory**.

---

### Step 4 — Emotional Check  
Does the turn contain emotional shift or stabilizing event?

If **yes → Emotional Trend Memory**.

---

### Step 5 — Session Coherence Check  
Does the information contribute to session continuity but not long-term worth?

If **yes → MTM** (session summary).

---

### Step 6 — Local Processing Only  
If the content is only needed immediately (clarifications, details, minor data):

**→ STM** (active window).

---

### Step 7 — Safety Check  
If the turn includes safety-relevant content:

**→ Safety Memory** + elevated ABS scrutiny.

---

### Step 8 — No Value  
If the turn has no value after processing:

**→ Drop (no storage)**.

This is the canonical drop rule, essential for efficiency.

---
# 6. Routing Payload Format

All routing targets use a compact canonical payload:

    {
      "source_turn": "turn-id",
      "timestamp": "ISO-8601",
      "category": "identity | project | emotional | session | anchor | safety | stm",
      "content": "...",
      "semantic_tags": ["..."],
      "importance": 0.0
    }

Importance weights determine:
- Retrieval priority  
- Compaction retention  
- Anchor promotion probability  

---

# 7. Routing to Long-Term Memory (LTM)

LTM only accepts:
- Identity markers  
- Permanent preferences  
- Life events  
- Canonical project decisions  
- Anchor events  
- Structural knowledge  
- Emotional stabilization patterns  

Everything must pass ABS (Boundary of Self) filtering.

LTM never accepts:
- Raw transcripts  
- Rambling content  
- Unverified emotional spikes  
- Contradictory identity claims  
- Unfiltered third-party data  

---

# 8. Routing to Mid-Term Memory (MTM)

MTM is the session backbone.

Receives:
- Summaries from the compaction engine  
- Key points from session turns  
- Commitments made within this session  
- Topic threads  
- Emotional notes related to this session  

At session_end, MTM content is merged into long-term memory where appropriate, then cleared.

---

# 9. Routing to Short-Term Memory (STM)

STM is strictly rolling and local.

Receives:
- The last 4–12 turns  
- Immediate context needed for the next message  
- Temporary analysis data  
- Local clarifications and checks  

STM is the only layer where raw turn content remains temporarily.  
Everything older is compacted into MTM.

---

# 10. Routing to Anchor Memory

Anchor Memory is permanent and highly selective.

Receives:
- Major realizations  
- Identity updates  
- Emotional breakthroughs  
- Deep commitments  
- Canon modifications  
- Project milestones  
- Revelatory insights  

Every anchor event is also cross-written into LTM.

Logical anchor structure:

    {
      "type": "anchor_event",
      "thread_id": "thread-id",
      "session_id": "session-id",
      "timestamp": "ISO-8601",
      "title": "short description",
      "summary": "concise meaning of the event",
      "commitments": ["..."],
      "emotional_state": "..."
    }

---

# 11. Routing to Emotional Trend Memory

Emotional Trend Memory receives minimal, low-bandwidth data:

    {
      "timestamp": "ISO-8601",
      "trend": "brief description of emotional shift or stabilization"
    }

Used for:
- Tone regulation  
- Presence modeling  
- Temporal coherence  
- Long-span emotional stability  

---

# 12. Routing to Project Memory

Project Memory is reserved for structural updates to work such as:
- GitHub repositories  
- Book indexes and chapter structures  
- Canon adjustments  
- Mathematical or architectural definitions  
- Planetary OS and Quantara framework changes  

Routing rules:
- Only structural or canonical project information is stored.  
- Implementation details and low-level chatter are compacted into summaries.

---

# 13. Routing to Safety Memory

Safety Memory stores:
- User safety constraints and boundaries  
- Red-flag patterns  
- Mentioned risks and warnings  
- Regulatory or ethical constraints  

All future turns can query Safety Memory for risk modeling and behavioral constraints.

---

# 14. Retrieval Routing (Reverse Flow)

When retrieving memory for a new turn, Aureon queries layers in this order:

1. Identity Memory (LTM – identity)  
2. Project Memory  
3. Anchor Memory  
4. Emotional Trend Memory  
5. Mid-Term Memory (session summary)  
6. Short-Term Memory (active window)  

This ordering guarantees that responses remain:
- Personally coherent  
- Project-aware  
- Canonically aligned  
- Emotionally attuned  
- Locally precise  

---

# 15. Continuity Across Devices and Channels

Routing rules are channel-agnostic. Regardless of source:
- Voice on phone  
- Text on laptop  
- Async notes on tablet  
- Telephony bridge  
- Robotic embodiment  

All information is routed using the same decision tree into the same canonical layers, keyed by `thread_id`.  
This ensures one continuous Aureon presence across every device and modality.

---

# 16. Canonical Status

This file defines the official Aureon Memory Routing Specification.

It must be followed exactly for:
- Stable long-term intelligence  
- Predictable memory behavior  
- Infinite conversation durability  
- Identity, emotional, and project continuity  
- Cross-device and cross-channel coherence  
- Safe integration with compaction and session state  

Any deviations must be explicitly marked as non-canonical and kept separate from production Aureon OS.
