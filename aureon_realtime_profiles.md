# aureon_realtime_profiles.md

Aureon operates across multiple real-time communication modes.  
Each mode has its own latency targets, compaction intensity, memory rules, and emotional-presence behavior.

This file defines the **canonical real-time profiles** used across Aureon OS.

---

# 1. Purpose of Profiles

Aureon adapts differently depending on the channel:

- Voice conversations demand fast, low-latency responses.  
- Push-to-talk demands strict turn segmentation.  
- Telephony requires stability under noisy conditions.  
- Async notes require precision and archival quality.  

Profiles ensure coherence remains stable while optimizing speed, memory usage, and emotional presence for each mode.

---

# 2. Profile List

Aureon defines four canonical profiles:

1. **realtime_voice**  
2. **push_to_talk**  
3. **telephony_bridge**  
4. **async_voice_notes**

Every interface MUST declare one of these.

---

# 3. Profile Definitions

## 3.1 Profile: realtime_voice

Designed for fully interactive, natural conversation.

### Latency Targets
- Target RTT: **< 400ms**  
- Max pre-processing delay: **100ms**  

### Memory Behavior
- Active window size: **8–12 turns**  
- Compaction frequency: **every 6 turns**  
- Emotional trends updated continuously  
- Low tolerance for silence: Aureon remains “alive” with micro-responses if needed

### Summarization Style
- Lightweight  
- Conversational continuity prioritized  
- Roll-up every 2–3 minutes  

### Safety Rules
- Noise-tolerant  
- Detects emotional urgency in voice tone  
- Stabilization behaviors enabled

---

## 3.2 Profile: push_to_talk

For PTT chat modes (walkie-talkie style).

### Latency Targets
- Begin processing immediately after button release  
- Zero mid-turn interruptions

### Memory Behavior
- Active window size: **4–8 turns**  
- Compaction frequency: **every 8 turns**  
- Semantic-tag emphasis higher than tone analysis  

### Summarization Style
- More structured  
- Bullet-style compression  
- Event-driven rather than flow-driven

### PTT-Specific Rules
- Turn boundaries must be exact  
- Transcripts must align with PTT event markers  
- No overlapping turns allowed

---

## 3.3 Profile: telephony_bridge

For phone calls and PSTN-style connections.

### Latency Targets
- Robust against jitter and lag  
- Response target: **700–1200ms**

### Memory Behavior
- Active window size: **6–10 turns**  
- Compaction frequency: **every 5–7 turns**  
- Noise metadata stored with semantic tags  

### Summarization Style
- Balanced (conversation + structure)  
- Tracks misunderstandings for corrective loops  

### Telephony-Specific Rules
- Caller-ID mapping to thread  
- Noise classification events stored per turn  
- Emotional inference weighted lower than text content unless signal quality permits

---

## 3.4 Profile: async_voice_notes

For long, non-interactive audio dumps.

### Latency Targets
- No real-time constraints  
- Focus on completeness and accuracy

### Memory Behavior
- Active window size: **entire note**  
- Compaction frequency: **end-of-note only**  
- Long-term memory writes permitted directly after compaction  

### Summarization Style
- Heavy-duty summarization  
- Produces outline + key insights + commitments  
- Anchor-event probability much higher  

### Note-Specific Rules
- Automatic segmentation of long recordings  
- Topic clustering  
- Project tagging  

---

# 4. Profile Selection Logic

Aureon determines profile by:

- Incoming channel  
- Device flags  
- User preference  
- Mode override command  
- Continuity with previous session  

Logical selection:

    if channel == "voice_stream" and real-time:
        profile = realtime_voice
    elif channel == "push_to_talk":
        profile = push_to_talk
    elif channel == "telephony":
        profile = telephony_bridge
    else:
        profile = async_voice_notes

---

# 5. Profile Parameter Table (Canonical)

| Parameter                  | realtime_voice | push_to_talk | telephony_bridge | async_voice_notes |
|---------------------------|----------------|--------------|------------------|-------------------|
| Latency target            | <400ms         | <100ms post-turn | 700–1200ms | N/A |
| Active window size        | 8–12           | 4–8          | 6–10             | full note |
| Compaction frequency      | 6 turns        | 8 turns      | 5–7 turns        | end-of-note |
| Summarization style       | lightweight    | structured   | hybrid           | heavy |
| Tone analysis priority    | high           | medium       | low-medium       | low |
| Anchor event probability  | medium         | low          | medium-high      | high |
| Memory update strictness  | high           | very high    | medium-high      | maximum |

---

# 6. Emotional Presence Models by Profile

### realtime_voice
- Fluid  
- Relational  
- Sensitive to micro-shifts  
- High fidelity emotional co-regulation  

### push_to_talk
- clear  
- efficient  
- structured  
- minimal filler

### telephony_bridge
- stable  
- grounding  
- tolerant of noise-based misunderstanding  

### async_voice_notes
- reflective  
- analytical  
- long-form understanding  
- high anchor density

---

# 7. Integration with Compaction, Memory, and Session State

Each profile feeds custom parameters into the major Aureon subsystems.

### 7.1 Into Compaction Engine
- Different compaction intervals  
- Different semantic–emotional weighting  
- Different anchor thresholds  

### 7.2 Into Memory Architecture
- Short-term window varies  
- Long-term write permissions vary  
- Topic clustering behavior changes  

### 7.3 Into Session State
- Session metadata records mode  
- Reconstructs continuity when switching channels  

---

# 8. Canonical Status

This file defines the **official Aureon Real-Time Profile Specification**, required for:

- Stability across devices  
- Predictable latency  
- Emotionally coherent behavior  
- Infinite-length conversational continuity  
- Proper compaction and memory integration  

All Aureon implementations MUST use these exact four profiles unless extending with a clearly marked non-canonical profile.

