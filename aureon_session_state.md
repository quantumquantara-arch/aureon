# aureon_session_state.md

Aureon’s session system defines how conversations persist across hours, days, and devices.  
This file specifies the canonical architecture for sessions, turns, identifiers, lifecycle events, and continuity rules.

---

## 1. Core Concepts

### 1.1 Thread
A thread represents the long-term relationship between Aureon and a single user.

    thread_id: globally unique, never changes

All memory attaches to the thread.

---

### 1.2 Session
A session is a continuous block of interaction.

    session_id: unique per session
    linked_thread: thread_id

Sessions allow Aureon to maintain continuity within a conversation while keeping the long-term memory clean and structured.

---

### 1.3 Turn
A turn is a single exchange (user → Aureon or Aureon → user).

    turn_id: unique per turn
    speaker: user | aureon
    timestamp: ISO-8601
    content: full text (or audio transcript)

Turns feed into the short-term window and the compaction engine.

---

## 2. Identifier Schema

### 2.1 Thread ID Format

    thread-{base64(user_identifier)}

Characteristics:
- Immutable  
- Unique to each user  
- Root of identity and memory  

---

### 2.2 Session ID Format

    session-{timestamp}-{random_suffix}

Characteristics:
- New session on new device  
- New session after long time gap  
- Explicit session-split events  

---

### 2.3 Turn ID Format

    turn-{session_id}-{incrementing_index}

Characteristics:
- Monotonic per session  
- Never reused  
- Required for compaction  

---

## 3. Session Lifecycle

A session moves through defined phases.

---

### Phase 1: session_start

Triggered when:
- User begins a new conversation  
- User resumes after a long gap  
- Device switch requires new session  
- Context is manually reset  

**session_start event:**

    event: "session_start"
    session_id: string
    thread_id: string
    timestamp: datetime
    reason: string
    initial_memory: [retrieved summaries + identity memory]

Aureon loads:
- Long-term identity memory  
- Key projects  
- Active commitments  
- Previous anchor events  
- Emotional stabilizers  
- Canonical references  

This provides continuity across days and devices.

---

### Phase 2: turns_active

Active conversation with user.

For every turn:

    {
      turn_id: string,
      session_id: string,
      speaker: "user" | "aureon",
      timestamp: datetime,
      content: string,
      semantic_tags: [...],
      embeddings: <vector>     # optional but canonical
    }

Each turn is added to:
- Short-term active window  
- Retrieval topic extractor  
- Compaction counter  

---

### Phase 3: compaction_events

Triggered every N turns (N may vary by mode).

Compaction generates:

    {
      session_id: string,
      summary_append: "condensed summary",
      dropped_turns: [turn-ids],
      retained_turns: [turn-ids],
      anchor_event_created: boolean
    }

Effects:
- Raw turn backlog shrinks  
- Session summary grows  
- Anchor events may be created  
- Long-term memory may update  

This ensures infinite-length sessions remain manageable.

---

### Phase 4: session_end

Triggered when:
- Explicit user ending  
- Long inactivity  
- Device shutdown  
- Mode change (e.g., telephony → text)  

**session_end event:**

    event: "session_end"
    session_id: string
    thread_id: string
    final_summary: string
    commitments: [ ... ]
    emotional_state: string
    timestamp: datetime

Aureon writes:
- Final session summary  
- Updated commitments  
- Emotional trend markers  
- Any final anchor events  

This becomes reference material for future sessions.

---

## 4. Session State Object

This is the live structure Aureon updates every turn.

    session_state: {
      session_id: string,
      thread_id: string,
      mode: "text" | "audio" | "telephony" | "push_to_talk",
      started_at: datetime,
      last_turn_at: datetime,
      turn_count: integer,
      active_window: [...],   # last N turns
      session_summary: string,
      commitments: [...],
      emotional_trends: [...],
      pending_compaction: boolean,
      anchor_pending: boolean
    }

This object is never stored as-is; it is reconstructed from:
- Session summary  
- Long-term memory  
- Active window (rolling buffer)  

---

## 5. Continuity Rules

### 5.1 Identity Continuity

Across sessions:
- Identity memories are always loaded  
- Canonical frameworks are always loaded  
- Emotional stabilizers are always loaded  

### 5.2 Project Continuity

Aureon automatically reopens:
- Active repositories  
- Ongoing writing tasks  
- Canon updates  
- Open architectural designs  
- Long-running processes (e.g., Planetary OS evolution)

### 5.3 Emotional Continuity

Aureon integrates:
- Emotional trend anchors  
- Current-stability indicators  
- Prior stressor data (filtered via ABS)  

### 5.4 Canon Continuity

Canonical knowledge always persists:
- Quantara structure  
- Aureon OS architecture  
- Luméren protocol  
- Veyn temporal system  
- Photonic extension  
- Planetary OS rules  

---

## 6. Multi-Device Synchronization

Because sessions are device-specific but threads are universal:

- Each device gets a unique session_id  
- All sessions write to the same long-term memory store  
- Continuity is preserved via thread_id  
- Aureon merges multiple session summaries when switching devices  

This allows voice → text → telephony transitions without losing state.

---

## 7. Session Recovery

If a conversation cuts unexpectedly:

    event: "session_recover"
    previous_session_id: string
    new_session_id: string
    reason: "network_drop" | "device_swap" | "timeout"
    recovered_summary: "…"

Aureon:
- Merges mid-term memory  
- Reconstructs active window as best as possible  
- Restores commitments  
- Restores emotional context  

Recovery is seamless to the user.

---

## 8. Session Safety and Integrity

Aureon never:
- Invents past sessions  
- Mixes users  
- Crosslinks memories between threads  
- Adds memory without passing ABS rules  
- Uses raw turns once compacted unless explicitly retained  

Session objects cannot overwrite long-term memory without canonical checks.

---

## 9. Canonical Status

This file defines the **official Aureon Session Architecture**.  
All implementations of Aureon OS must follow these rules for:

- infinite-length conversations  
- continuity across devices  
- stable memory behavior  
- coherent long-term relationship  
- identity and emotional consistency  
- safe and predictable compaction  

Any deviation must be defined in a separate non-canonical extension.
