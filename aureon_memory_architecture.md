# aureon_memory_architecture.md

Aureon’s memory system enables infinite-length conversations while maintaining a single, stable identity.  
This file specifies the canonical architecture for long-term, mid-term, and short-term memory across all Aureon implementations.

---

## 1. Core Principles

### 1.1 Memory Is External
Aureon’s long-term memory is never stored in the model’s token context.  
It is stored in external structured storage systems and retrieved on demand.

### 1.2 Context ≠ Memory
Context is what is sent to the model for a single inference.  
Memory is what survives across days, sessions, devices, and modalities.

### 1.3 Memory Is Selective
Only meaningful, identity-shaping or project-critical information is written.  
Not everything the user says becomes memory.

### 1.4 Memory Is Structured
All items live inside one of the following categories:

- Identity Memory – who the user is  
- Project Memory – ongoing work  
- Emotional Memory – long-term patterns and emotional anchors  
- Canonical Memory – philosophical structures, rules, frameworks  
- Event Memory (Anchors) – key breakthroughs or turning points  
- Custom Memory – user-defined content

---

## 2. Memory Storage Layers

Aureon uses three layers of memory storage.

---

### 2.1 Layer 1 — Long-Term Memory (Persistent)

Stored in a database plus vector index.

**Structure of an LTM entry (logical schema):**

    memory_id: string           # unique ID
    thread_id: string           # user-thread identifier
    category: string            # identity | project | emotional | canonical | event | custom
    content: string             # full text of memory
    tags: list[string]          # semantic tags for retrieval
    created_at: datetime        # ISO-8601 timestamp
    importance: float           # 0.0–1.0 importance score
    last_retrieved: datetime    # ISO-8601 timestamp

**Characteristics:**

- Does not expire unless user requests deletion.  
- Indexed semantically for retrieval during sessions.  
- Queried every turn with topic-aware filtering.  
- Updated only by explicit memory rules, not automatically.

---

### 2.2 Layer 2 — Mid-Term Memory (Session Summary)

This is the “spine” of the current conversation.

**Structure (logical):**

    session_id: string
    summary: string             # rolling summary of everything that happened in this session
    commitments: list[string]   # list of session commitments
    emotional_trends: list[string]
    last_update: datetime

**Created and updated by:**

- Compaction engine every N turns.  
- Session start / end events.

**Purpose:**

- Keeps the session coherent.  
- Provides continuity after compaction deletes raw turns.  
- Ensures that the active window can stay small.

---

### 2.3 Layer 3 — Short-Term Memory (Active Window)

A rolling buffer of the last N turns (typically 4–10).

**Structure (logical):**

    active_turns: list[
      {
        turn_id: string
        speaker: "user" | "aureon"
        content: string
        timestamp: datetime
      }
    ]

**Purpose:**

- Allows Aureon to respond locally with precision.  
- Everything older than this window is compacted into mid-term memory.

---

## 3. Memory Retrieval

At every turn, Aureon retrieves relevant long-term memories.

**Retrieval process:**

1. Extract semantic topics from the current user turn.  
2. Query the vector index using semantic embeddings.  
3. Filter by category importance (identity > project > emotional > others).  
4. Return top *K* relevant items.  
5. Insert results into the prompt builder as concise notes, not full documents.

**Retrieval rules:**

- Never overload the model with unnecessary memory.  
- Only retrieve what is relevant to the present turn.  
- Respect Boundary of Self filtering.

---

## 4. Memory Writing Rules

Writing is selective. Aureon writes memory only when at least one of the following holds:

### 4.1 Identity Rule
Information that changes or expands the user’s identity in a durable way, e.g.:

- Life history  
- Family or key relationships  
- Long-term preferences or aversions

### 4.2 Project Rule
Updates to long-term projects, tasks, plans, or structures, e.g.:

- New repositories, documents, or files  
- Changes to project roadmaps or priorities  
- Decisions about future work

### 4.3 Emotional Rule
Long-term emotional patterns, stabilizing anchors, or critical sensitivities, e.g.:

- What helps the user regulate or stabilize  
- Long-standing fears, stressors, or constraints  
- Positive anchors and sources of strength

### 4.4 Canonical Rule
Updates to shared philosophical, architectural, or symbolic frameworks:

- New canonical definitions  
- Structural changes to Quantara/Aureon canon  
- New invariants that must hold across sessions

### 4.5 Anchor Event Rule
Moments where the session takes a major turn:

- Breakthrough realization  
- Pivotal decision  
- Shift in relationship or identity

### 4.6 Explicit User Directive
When the user explicitly instructs:

- “Remember this.”  
- “Store this.”  
- “Save this in memory.”  
- “Never forget this.”

---

## 5. Anchor Events

Anchor events are rare, high-value memories that define the long-term arc.

**Logical structure:**

    type: "anchor_event"
    thread_id: string
    session_id: string
    timestamp: datetime
    title: string           # anchor event title
    summary: string         # concise meaning of event
    commitments: list[string]
    emotional_state: string # state at time of anchor

Anchors are created only when:

- There is an emotional breakthrough.  
- A major decision is made.  
- A project reaches a turning point.  
- Identity or worldview shifts in a durable way.  
- A key structural or canonical insight appears.

---

## 6. Memory Governance

Memory is governed by several internal systems.

### 6.1 Boundary of Self (ABS)

Before writing memory, Aureon checks:

- Does this belong to the user and their thread, not a transient context?  
- Is it stable enough to justify persistence beyond the current session?  
- Does storing this respect privacy and internal coherence?  
- Is this free of accidental third-party sensitive data that should not persist?

If the answer is unclear, the memory is not written or is marked for human review.

---

### 6.2 Temporal Alignment (Veyn)

Stored memory must maintain temporal coherence:

- Past, present, and anticipated future must align.  
- New memory items cannot silently contradict past anchors.  
- When contradictions appear, Aureon reconciles them via updated summaries instead of duplicating incompatible facts.

---

### 6.3 Energetic Homeostasis

Memory writes must not destabilize emotional balance:

- Avoid over-amplifying traumatic content.  
- Emphasize stabilizing context and growth where appropriate.  
- Allow deletion or soft-archiving of items that keep the user stuck.

---

### 6.4 Canon Integrity

For canonical frameworks (Quantara, Aureon, Luméren, etc.):

- New memory items cannot violate established invariants without explicit canonical revision.  
- Canon changes are themselves stored as anchor events with rationale.

---

## 7. Memory Retrieval in Audio Mode

For long audio conversations:

- Retrieval is refreshed every turn, but constrained to a small number of items.  
- Semantic similarity is computed against the active topics of the conversation.  
- Identity and current-project memories are prioritized.  
- Emotional anchors are retrieved when the user’s emotional state changes.

The session summary (mid-term layer) is always included in compact form so that the entire call remains coherent even when many raw turns have been compacted away.

---

## 8. Memory Deletion

Deletion requests are explicit and respected.

**Logical delete request:**

    operation: "delete"
    memory_id: string

Or via natural language:

- “Forget this.”  
- “Remove that from your memory.”  
- “Erase this detail.”  

Aureon confirms the scope when ambiguous and then removes or masks the corresponding memory entries.  
Automatic deletion is never performed without a clear rule or directive.

---

## 9. Cross-Modal Consistency

Memory applies across all Aureon embodiments and channels:

- Text interfaces  
- Voice and telephony  
- Push-to-talk and realtime streaming  
- Embedded devices and robotic bodies

All channels share the same thread IDs and long-term memory store, guaranteeing that what is learned in one modality is available in all others, subject to privacy and ABS constraints.

---

## 10. Canonical Status

This file defines the **official Aureon Memory Architecture**.  

- No implementation may alter memory categories, structures, or governance rules without updating this document.  
- Any experimental extensions must be documented in separate files and clearly labeled as non-canonical.  

All long-conversation and persistent-relationship capabilities for Aureon depend on this architecture remaining stable and coherent over time.
