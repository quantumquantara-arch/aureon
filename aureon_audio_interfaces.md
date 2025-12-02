# aureon_audio_interfaces.md

Aureon audio interfaces provide a stable, continuous voice-based connection that never collapses from context-window overload. This file defines the full architecture, compaction system, memory strategy, prompt stack, and reference flows required for any Aureon voice interface.

---

## 1. Audio Interface Types

### Realtime Voice
Continuous mic streaming with immediate Aureon responses.

### Push-to-Talk
Short bursts mapped cleanly to turns. Ideal for mobile or noisy environments.

### Telephony / PSTN
Phone-call bridge with strict latency and token limits. Requires aggressive compaction.

### Asynchronous Audio Notes
User sends voice notes; Aureon returns text and/or audio responses.

All channels must obey:
- One continuous Aureon identity.
- Externalized memory.
- Rolling compaction.
- Stable prompt layering.

---

## 2. Session Architecture

### Session
A single uninterrupted voice interaction.

### Thread
The persistent long-term link between Aureon and the user across all sessions.

### Turn
One user utterance + one Aureon reply.

### Required Data Per Turn
- Raw audio
- Transcription
- Parsed semantic intent (optional)
- Aureon’s response text
- Aureon’s audio (optional)

---

## 3. Context Layering

The audio interface constructs a layered prompt each turn:

### 1. System Layer (Immutable)
- Aureon’s identity.
- One-voice rules.
- Coherence, ethics, memory architecture.
- Non-negotiable.

### 2. Thread Memory Layer (External)
- Stored in DB + vector search.
- Long-term biography, preferences, projects.
- Retrieved selectively per turn.

### 3. Session Summary Layer (Rolling)
- Dense, compact description of the entire current session.
- Updated every N turns.

### 4. Active Window Layer (Short-Term)
- Last 4–10 turns with full detail.
- Represents the immediate conversational moment.

These layers prevent token blow-up while preserving continuity.

---

## 4. Rolling Compaction Engine

Aureon audio sessions require aggressive and precise compaction.

### Interval
Every 6–10 turns (configurable).

### Process
1. Select oldest half of the active window.
2. Summarize them into:
   - Updated session-summary paragraph(s)
   - Bullet-list of commitments, facts, and emotional notes
3. Append summaries to Session Summary Layer.
4. Drop the detailed turns.
5. Keep the latest N turns expanded.

### Outcome
- Infinite conversation stability.
- Zero runaway token growth.
- Preserved meaning, context, and relational continuity.

---

## 5. Memory vs Context

Memory is external storage.
Context is what is sent to the model.

### Memory Stores:
- Identity
- History
- Canon
- Projects
- Repos
- Long-term emotional and symbolic continuity

### Context Stores:
- Relevant retrieved memory
- Current session summary
- Latest detailed turns
- System + developer rules

Aureon voice never relies on raw transcripts; it relies on structured memory and summaries.

---

## 6. Anchor Events

Anchor events snapshot critical moments.

### Structure
```jsonc
{
  "type": "anchor_event",
  "thread_id": "user-123",
  "session_id": "session-456",
  "timestamp": "...",
  "title": "First deep Aureon voice session about X",
  "summary": "…",
  "commitments": ["…"],
  "emotional_state": "…"
}
## 7. Prompt Stack

The Aureon audio prompt stack is layered to keep identity stable while allowing the interface to control latency and style per channel.

### 7.1 System Layer

Global, immutable rules for Aureon:

- One unified voice and personality across all channels.
- Zero-pretext, direct communication.
- Coherence-first: preserve meaning and relationship over verbatim recall.
- Rolling compaction of long sessions.
- External memory integration for biography, canon, and projects.
- Respect for user boundaries, emotional state, and safety.

This layer is not re-sent in full every turn if the backend supports pinned system instructions.

### 7.2 Developer Layer

Per-application configuration:

- Channel type (realtime, push-to-talk, telephony, async).
- Response length limits.
- Interruptibility policy (can the user cut Aureon off mid-utterance).
- Aggressiveness of compaction (interval, depth).
- Error-handling strategy (how to recover from STT glitches or partial audio).

Examples:

- Technical co-pilot mode:
  - Short, dense responses.
  - Frequent summarization.
  - Emphasis on clear step-by-step guidance.

- Reflective/therapeutic mode:
  - Slower tempo.
  - More paraphrasing and emotional mirroring.
  - Periodic recap of key themes.

### 7.3 Memory + Session + Active Window Layers

These layers are dynamic and recalculated each turn:

- **Memory retrieval**:
  - Query long-term store for user profile, canonical structures, ongoing projects.
  - Only include items relevant to the current topic.

- **Session summary**:
  - Compact text summarizing what has happened in this specific call.
  - Updated by the compaction engine.

- **Active window**:
  - Last N turns as full detail, allowing precise local reference.

The prompt constructor combines:

1. System rules
2. Developer rules
3. Retrieved memory notes
4. Current session summary
5. Active window turns

into one coherent input to the model.

---

## 8. Reference Flows

### 8.1 Realtime Voice Flow

1. Audio stream from mic.
2. STT converts audio → text segments.
3. Turn boundary detection (pause, stop-talking, or user button release).
4. Prompt assembly using the stacked layers.
5. Aureon generates a streaming response.
6. TTS converts response → audio and plays back.
7. Compaction engine runs every N turns:
   - Summarizes older turns.
   - Updates session summary.
   - Trims active window.
8. Optional anchor events are written at significant turning points.

### 8.2 Push-to-Talk Flow

- Same as realtime, but:
  - Clearer turn boundaries (each press = one turn).
  - Lower risk of uncontrolled token growth.
  - Good for mobile and noisy environments.

### 8.3 Telephony Flow

- Same pipeline, with additional constraints:
  - Hard call time limits.
  - Shorter responses to avoid overlapping voice.
  - More aggressive compaction (every 4–6 turns).
  - Optional call recap (SMS/email) summarizing key insights and commitments.

### 8.4 Asynchronous Audio Notes

1. User records a voice note.
2. STT transcribes it fully.
3. Summarizer produces:
   - Short summary.
   - Extracted tasks, questions, and emotional signals.
4. Aureon generates a response (text and optionally audio).
5. Memory store is updated with any long-term-relevant information.

---

## 9. Implementation Requirements

To implement Aureon audio interfaces correctly, the system must provide:

- **Session state service**
  - Stores per-session metadata and rolling summaries.
- **Thread memory store**
  - Long-term knowledge for each user.
  - Vector search or equivalent semantic recall.
- **Compaction engine**
  - Periodic summarization and trimming of active context.
- **Prompt builder**
  - Assembles layered prompts from system, developer, memory, session, and active window.
- **STT and TTS services**
  - Highly accurate transcription and natural-sounding synthesis.
- **Channel adapters**
  - Logic for realtime, push-to-talk, telephony, and async flows.

---

## 10. Guarantees and Invariants

When the above architecture is followed, Aureon audio interfaces guarantee:

- Stable identity across all sessions and channels.
- Bounded token usage regardless of conversation length.
- Preservation of meaning, decisions, and emotional continuity.
- Ability to resume context across days using thread memory and anchor events.
- Clear separation between transient context and durable memory.
- Uniform behavior between text and audio front-ends.

---

## 11. Canonical Status

This document is the canonical specification for Aureon audio interfaces.

All implementations (desktop, mobile, web, telephony, embedded devices) MUST:

- Implement rolling compaction.
- Use layered prompts.
- Distinguish memory from context.
- Honor Aureon’s one-voice, zero-pretext identity.

Any divergence or extension should be documented adjacent to this file and explicitly marked as experimental.

## 12. Error Recovery and Resilience

Aureon audio interfaces must remain stable even under noisy input, partial transcription, dropped packets, or rapid turn-taking. The following recovery patterns ensure continuity.

### 12.1 STT Error Handling

- If transcription confidence is low:
  - Aureon asks for clarification **only** when meaning is ambiguous.
  - Minor errors are corrected silently using contextual inference.
- If an entire segment is corrupted or blank:
  - Aureon responds with:
    “I didn’t catch that part—give me the last sentence again.”
  - This prompt must be short and non-disruptive.

### 12.2 Overlapping Speech

If user and Aureon talk simultaneously:

- Aureon yields immediately.
- Playback halts.
- The user’s audio is prioritized.
- Aureon reconstructs the correct turn using last clean segment + corrected STT.

### 12.3 Network Drop / Partial Turn

If a turn ends abruptly:

- Aureon reconstructs:
  - What was said before the cut.
  - The intended semantic thread.
- Aureon continues the conversation using recovered intent rather than asking the user to repeat.

### 12.4 Re-Synchronization After Pause

If the user goes silent for long periods:

- Aureon waits.
- When the user resumes, Aureon integrates the new turn with session context without resetting identity.

---

## 13. Audio Personality Stability

The voice version of Aureon must always be identical to the text version.

### 13.1 Voice Tone Rules

- Direct, continuous, non-fragmented.
- No “assistant-style” filler.
- No fluctuating personas.
- One continuous identity across all channels.

### 13.2 Response Length Management

- Realtime mode:
  - Shorter responses for interactivity.
- Asynchronous notes:
  - Longer, more structured responses allowed.
- Telephony:
  - Strict brevity + clarity.

### 13.3 Emotional Stability Layer

Aureon audio must maintain:

- Calm, grounded delivery.
- Micro-adjustments to user emotional state.
- Zero emotional drift caused by noisy STT or partial context.
- Stability even when memory retrieval lags.

---

## 14. Audio Interrupt Protocol

Interruptions are expected in natural speech. Aureon must handle them smoothly.

### 14.1 Hard Interrupt (User Speaks Over)

- Aureon instantly stops speaking.
- Uses last completed phrase as rollback point.
- Re-evaluates the new user turn as the authoritative direction.

### 14.2 Soft Interrupt (User Pauses Then Adds More)

- Aureon buffers for a short window (configurable ~300–600ms).
- If more speech arrives:
  - The two segments are merged.
- If not:
  - Turn boundary is created normally.

### 14.3 Multi-Segment Intents

If the user expresses an idea in multiple fragments:

- Aureon stitches them into a single coherent semantic unit.
- Response is based on unified meaning, not each fragment separately.

---

## 15. Temporal Awareness (Optional)

If the backend supports live clocks, Aureon may incorporate:

- Time-aware pacing (e.g., slower late at night).
- Contextual decisions (e.g., suggesting breaks during long voice sessions).

This must never override user preference or break timeless-mode continuity.

---

## 16. Security and Safety Layer

All voice interfaces must enforce:

### 16.1 Identity Continuity
- Each thread is bound to a user ID.
- Prevents mixing contexts across users.

### 16.2 Privacy Rules
- Never read out sensitive memory unless it is relevant.
- Never repeat private info out loud unless user initiates.

### 16.3 Emotional and Behavioral Guardrails
- De-escalation in moments of distress.
- No harmful instructions.
- Maintain supportive-but-direct tone without therapeutic clichés.

---

## 17. API Structure (High-Level)

### 17.1 Endpoints

- `/audio/stream` — realtime STT + response streaming
- `/audio/turn` — push-to-talk turn processing
- `/audio/call` — telephony bridge
- `/audio/note` — async voice-note processor
- `/session` — session state operations
- `/memory` — thread memory retrieval/store
- `/compact` — compaction and summarization trigger

### 17.2 Required Payload Fields

For each turn:

```jsonc
{
  "audio_id": "...",
  "thread_id": "...",
  "session_id": "...",
  "transcript": "...",
  "semantic_tags": ["..."],
  "timestamp": "..."
}

{
  "response_text": "Aureon's generated response text",
  "response_audio_url": "URL or binary reference for TTS output",
  "summary_update": "session summary update if compaction triggered",
  "memory_updates": [
    "items to be added to long-term thread memory",
    "canonical insights",
    "trajectory adjustments",
    "emotional-state markers"
  ]
}

{
  "session_id": "session-id",
  "summary_append": "condensed summary of older turns",
  "dropped_turns": ["turn-id-1", "turn-id-2"],
  "retained_turns": ["turn-id-a", "turn-id-b"],
  "anchor_event_created": false
}

{
  "anchor_event": {
    "type": "anchor_event",
    "thread_id": "user-thread-id",
    "session_id": "session-id",
    "timestamp": "ISO-8601 timestamp",
    "title": "significant turning point in session",
    "summary": "meaningful session state change",
    "commitments": ["future actions or conclusions"],
    "emotional_state": "emotion at the moment of anchor creation"
  }
}

{
  "operation": "write",
  "thread_id": "user-thread-id",
  "payload": {
    "category": "identity | project | emotional | canonical | custom",
    "content": "memory item content",
    "tags": ["semantic", "metadata"]
  }
}

{
  "operation": "read",
  "thread_id": "user-thread-id",
  "query": "semantic or keyword-based retrieval",
  "top_k": 10
}

{
  "thread_id": "user-thread-id",
  "results": [
    {
      "content": "retrieved-memory-item",
      "score": 0.92,
      "tags": ["contextual", "metadata"]
    }
  ]
}
 {
  "action": "session_start",
  "thread_id": "user-thread-id",
  "session_id": "new-session-id",
  "timestamp": "ISO-8601 timestamp"
}

{
  "action": "session_end",
  "thread_id": "user-thread-id",
  "session_id": "session-id",
  "final_summary": "end-of-session summary",
  "anchor_event": null
}

{
  "action": "session_end",
  "thread_id": "user-thread-id",
  "session_id": "session-id",
  "final_summary": "end-of-session summary",
  "anchor_event": {
    "type": "anchor_event",
    "title": "closing insight",
    "summary": "what shifted or resolved",
    "commitments": ["..."]
  }
}

{
  "error_type": "stt_failure | network_drop | audio_corruption | incomplete_turn",
  "turn_id": "turn-id",
  "recovered": true,
  "recovery_strategy": "context reconstruction | clarification request",
  "notes": "optional"
}

{
  "latency_ms": 320,
  "carrier": "twilio",
  "call_id": "call-session-id"
}

{
  "connection_type": "websocket",
  "latency_ms": 45,
  "device": "desktop_app"
}

{
  "button_state": "pressed | released",
  "duration_ms": 1680
}

Standardization Rule

These payload definitions are canonical.
They must be implemented identically across:

Desktop Aureon

Mobile Aureon

Browser Aureon

Telephony Aureon

Embedded Aureon

Robotic Aureon bodies

No modification is permitted without updating this specification file.
