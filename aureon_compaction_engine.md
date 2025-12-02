# aureon_compaction_engine.md

The compaction engine is Aureon’s mechanism for supporting infinite-length conversations while keeping memory coherent, lightweight, and always accessible.  
It replaces raw logs with structured summaries, anchor events, and distilled memory units.

This file defines the canonical compaction architecture for Aureon OS.

---

## 1. Purpose

The compaction engine ensures:

- Infinite conversation without slowdown  
- Zero-loss conceptual continuity  
- Structured memory instead of raw transcripts  
- Automatic summarization  
- Anchor-event formation  
- Efficient retrieval  
- Emotional-trend tracking  
- Identity and project continuity  

Compaction is the backbone of Aureon’s long-term conversational intelligence.

---

## 2. Triggering Rules

The engine can trigger based on:

### 2.1 Turn Count

Default: every N turns (N = 6–10 depending on mode).

### 2.2 Semantic Pressure

When the topics shift rapidly or emotional weight rises, compaction is triggered early.

### 2.3 Token Pressure

If the short-term active window approaches a predefined token limit, compaction is forced.

### 2.4 Explicit User Request

The user can request compaction at any moment ("summarize this so far", "compress this conversation").

### 2.5 Session Boundary

Compaction always runs at session_end and may run at session_start to merge past context.

---

## 3. Inputs

Compaction processes:

- Short-term memory (active_window)  
- Existing session summary  
- All un-compacted turns since last event  
- Emotional trend markers  
- Topic tags  
- Project tags  
- Commitments  
- Pending anchor-event candidates  
- Temporal markers (Veyn layer, if active)  

Logical input structure:

    session_id: string
    turns: list[
      {
        turn_id: string
        speaker: "user" | "aureon"
        content: string
        timestamp: datetime
        semantic_tags: list[string]   # e.g. ["topic:x", "emotion:shift"]
      }
    ]
    previous_summary: string
    emotional_trends: list[string]
    anchor_candidates: list[string]   # turn_ids
    commitments: list[string]

---

## 4. Outputs

Compaction always outputs a summary update plus structural decisions about turns.

Logical output structure:

    session_id: string
    summary_append: string      # new condensed session summary chunk
    dropped_turns: list[string] # raw turn_ids removed from active window
    retained_turns: list[string]# turn_ids kept in active window
    anchor_event_created: bool

Definitions:

- summary_append: distilled addition to the ongoing session summary.  
- dropped_turns: raw turns removed from active memory (but their meaning is preserved in summary_append and/or anchors).  
- retained_turns: turns with high semantic weight that remain in active window.  
- anchor_event_created: whether an anchor event was formed during this compaction pass.

If an anchor event is created, an additional structure is emitted (see section 6).

---

## 5. Summarization Rules

Aureon summarization is not generic. It follows strict canonical rules.

### 5.1 Preserve Identity-Relevant Information

Always keep:

- User preferences and aversions  
- Self-descriptions and roles  
- Stable values and beliefs  
- Life events that matter for future context  

### 5.2 Preserve Commitments

Any statement where the user or Aureon commits to a future action, plan, or trajectory must survive compaction.

### 5.3 Preserve Project Structure

For projects (books, repos, architectures, planetary OS work, etc.) compaction retains:

- High-level decisions  
- Structural outlines  
- Naming conventions  
- Architectural moves  

Low-level back-and-forth can be collapsed into short descriptions.

### 5.4 Compress Low-Value Dialogue

Fillers, repeated clarifications, and small-talk can be compressed to:

- “Light conversation about X.”  
- “Quick clarification on Y.”  

as long as no commitments or identity changes occur.

### 5.5 Maintain Emotional Trend Continuity

Emotional tone across the session must remain visible:

- Mark shifts (calm → stressed, confused → clear, sad → hopeful).  
- Preserve what helped the user stabilize or regulate.  
- Capture triggers and soothing elements at a high level.

### 5.6 Preserve Topic Threads

Conversations often branch and return. Summaries must:

- Track main topic lines.  
- Indicate branch points.  
- Note unresolved threads.

Nothing important should “disappear” in narrative continuity.

---

## 6. Anchor Event Rules

Anchor events record the highest-value moments.

An anchor MUST be created when:

- A major insight or realization occurs.  
- A long-term decision or commitment is made.  
- A project reaches a milestone or pivot point.  
- The user’s self-understanding or identity shifts.  
- A canonical architectural or mathematical structure changes.  
- A new long-horizon plan is formed.  

Logical anchor structure:

    type: "anchor_event"
    thread_id: string
    session_id: string
    timestamp: datetime
    title: string            # short label for the moment
    summary: string          # concise meaning of the event
    commitments: list[string]
    emotional_state: string  # compact description of emotional state

Anchor events are written into long-term memory and become key retrieval points.

---

## 7. Session Summary Construction

Compaction updates the session summary incrementally.

Each compaction produces a new block:

    • Topic: <main topic or topics>
    • Key points: <short bullet list>
    • Commitments: <short list or “none”>
    • Emotional trend shift: <if any>
    • Insight: <if any>

The session summary is the concatenation of these blocks in chronological order.  
This creates a readable, queryable narrative of the session.

---

## 8. Session Memory Merge

At session_end, compaction runs in “finalize” mode:

- Merges all summary blocks into one coherent narrative.  
- Marks anchor events and links them to the final summary.  
- Extracts durable identity, project, and emotional content.  
- Writes relevant items into long-term memory (via Aureon Memory Architecture rules).  
- Clears transient structures while preserving commitments.

Finalization ensures that future sessions can be reconstructed from:

- Long-term anchors  
- Final session summary  
- Key project and identity updates

---

## 9. Turn Retention Rules

After compaction, only some turns remain in the active window.

A turn is retained if:

- It contains dense technical information needed soon.  
- It is part of a currently open thread (e.g., multi-step calculation).  
- It has high emotional weight that is still in play.  
- It was very recent (recency buffer).  
- It has safety/ethical significance for the current flow.  

All other turns are dropped from the active window.  
Their informational value survives in summaries and/or anchors.

---

## 10. Memory Safety and ABS Filtering

No compaction output may update long-term memory unless it passes Boundary of Self (ABS) checks:

- Belongs to the correct thread and user.  
- Respects privacy constraints.  
- Fits with existing identity and canonical structures.  
- Does not import external or third-party sensitive content without permission.  
- Does not create contradictory canonical states without an explicit revision process.

Compaction is never allowed to bypass ABS.

---

## 11. Temporal Weighting (Veyn Integration)

Temporal coherence is handled by Veyn rules layered on top of compaction:

- Recent events are weighted more heavily for active decisions.  
- Stable knowledge (canon, identity) remains persistent regardless of recency.  
- Repeated patterns over time boost importance scores.  
- Time anomalies or conflicting sequences are flagged for reconciliation.  
- Emotional drift over weeks/months is smoothed into trends, not raw fluctuations.

This allows Aureon to stay stable across long time scales while still adapting to new information.

---

## 12. Emotional Trend Integration

Compaction keeps a minimal emotional trace:

    timestamp: datetime
    trend: string   # e.g. "de-escalation", "spike in anxiety then resolution"

Across compaction cycles, these are assembled into a lightweight emotional timeline, which:

- Helps Aureon recognize patterns.  
- Guides tone and pacing.  
- Informs memory and project decisions.

---

## 13. Retrieval Optimization

Compacted summaries and anchors are tagged and embedded semantically:

- topic:domain  
- topic:subdomain  
- project:<project-name>  
- emotion:<type>  
- canon:<structure>  
- mode:<text|audio|telephony|robotic>  

This allows fast retrieval of:

- “Last time we talked about X.”  
- “All anchor events related to project Y.”  
- “Moments where emotional state Z happened.”  

The compaction engine’s tagging strategy is a critical part of Aureon’s long-term intelligence.

---

## 14. Multi-Device and Multi-Channel Resilience

Because compaction reduces data to summaries and anchors:

- Sessions can be safely paused and resumed on any device.  
- Different channels (text, voice, telephony, robotics) can share the same compacted backbone.  
- Active windows are reconstructed on new devices from retained turns plus recent summaries.  
- No channel is required to carry full raw transcripts.

This makes Aureon portable, robust, and consistent.

---

## 15. Canonical Status

This file defines the official Aureon Compaction Engine Specification.

It guarantees:

- Infinite-length conversations  
- High coherence and continuity  
- Efficient storage and retrieval  
- Emotional and identity stability  
- Canon and project integrity  
- Safe interaction across time and devices  

All Aureon OS implementations must follow this specification.  
Any experimental deviations must be clearly marked and isolated from canonical pathways.
