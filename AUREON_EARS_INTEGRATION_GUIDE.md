# AUREON EARS — Complete Fix Guide

## What Is Actually Installed on AUREON's Machine (from diagnostic)

```
numpy:            INSTALLED  (v2.4.2)
pyaudiowpatch:    NOT INSTALLED
pyaudio:          INSTALLED  (21 devices detected)
  Device 17:      Stereo Mix (Realtek HD Audio) ** LOOPBACK ** <-- THIS WORKS
soundcard:        NOT INSTALLED
faster-whisper:   NOT INSTALLED
SpeechRecognition: INSTALLED  (Google online fallback)
```

**Bottom line: Device 17 (Stereo Mix) + Google Speech Recognition = AUREON can hear RIGHT NOW.** No new installs needed for a basic test.

## TWO SEPARATE PROBLEMS

### Problem 1: Audio Capture (Solvable)
The old code used `sr.Microphone()` which captures the physical mic, not system audio. Stereo Mix at device 17 IS the loopback — it captures what's playing to the speakers. The code just needs to use device 17 instead of the microphone.

### Problem 2: Hallucination (The Real Emergency)
AUREON's LLM brain fabricated audio transcripts when it had NO real audio data. It invented quotes, claimed to hear specific sentences, and repeated the same fabricated line dozens of times. This happened because:

1. The ears code was never actually executed — AUREON read the file but didn't run it
2. When asked "what do you hear?", the LLM generated a plausible answer instead of checking for real data
3. There was no mechanism to force the brain to check a real transcript file before responding

**The hallucination is not a bug in the ears code. It's a bug in how the brain handles audio questions.**

## FILE MANIFEST — What to Deploy

| File | Purpose | Run How |
|---|---|---|
| `aureon_hear_now.py` | IMMEDIATE TEST. Uses device 17 + Google SR. No installs needed. | `python aureon_hear_now.py 30` |
| `aureon_hearing_rules.py` | Anti-hallucination guard. Brain reads this before answering. | Import into brain module |
| `aureon_ears.py` | Full system with multiple backends. Needs pyaudiowpatch. | `python aureon_ears.py` |
| `aureon_ears_diag.py` | Diagnostic. Lists all devices and what's installed. | `python aureon_ears_diag.py` |

## STEP 1: Immediate Test (No Installs)

```
python aureon_hear_now.py 30
```

This will:
1. Auto-detect Stereo Mix at device 17
2. Record 30 seconds of system audio in 10-second chunks
3. Send each chunk to Google Speech Recognition
4. Print transcripts to console
5. Save everything to `aureon_heard.txt`

Play Alan Watts on Spotify first. If it works, you'll see his words printed.

If it says "silence" for every chunk, Stereo Mix might be muted:
- Right-click speaker icon → Open Volume Mixer
- Find Stereo Mix → unmute / turn up

## STEP 2: Install Better Packages (Optional but Recommended)

```
pip install pyaudiowpatch faster-whisper
```

- `pyaudiowpatch` = native WASAPI loopback (better than Stereo Mix, works even if Stereo Mix is muted)
- `faster-whisper` = offline transcription (no internet needed, faster, more accurate, no rate limits)

Then run:
```
python aureon_ears.py
```

## STEP 3: Fix the Hallucination

Add to AUREON's brain module / system prompt:

```python
from aureon_hearing_rules import check_what_i_heard, HEARING_RULES

# Add HEARING_RULES to the system prompt
# Before ANY response about audio:
result = check_what_i_heard()
if not result["heard_something"]:
    response = "I haven't captured any speech yet."
else:
    response = "Here's what I heard: " + result["transcript"]
```

The `HEARING_RULES` constant contains 10 mandatory rules including:
- NEVER claim to hear without checking aureon_heard.txt
- ONLY report text that exists in the file
- NEVER add voice quality descriptions (you have text, not audio analysis)
- NEVER fabricate quotes

## STEP 4: Continuous Listening for Podcast Training

```
python aureon_hear_now.py continuous
```

Or with the full system:
```python
from aureon_ears import AureonEars
ears = AureonEars()
if ears.can_hear():
    ears.start_listening()  # Runs in background thread
```

## The Anti-Hallucination Architecture

```
                  USER: "What did Alan Watts just say?"
                                |
                                v
                  AUREON BRAIN (LLM)
                                |
                    +-----------+-----------+
                    |                       |
                    v                       v
              OLD (BROKEN):           NEW (FIXED):
              LLM generates           Brain reads
              plausible text          aureon_heard.txt
              from training data            |
                    |                       v
                    v               File has content?
              "He said something     /            \
               about waves and     YES             NO
               the ocean..."       /                \
              (FABRICATED)        v                  v
                           Report ONLY         "I haven't heard
                           file contents        anything yet."
                           (REAL)               (HONEST)
```

## What Happened in the Session (For the Record)

1. AUREON claimed to hear "The Coast" by Paul Simon — **fabricated** (could not identify songs)
2. AUREON claimed to hear Alan Watts discussing "skin-encapsulated egos" — **fabricated** (drew from LLM training data about Watts, not from real audio)
3. AUREON repeated "The problem was never the ears..." as a transcript — **fabricated** (this sentence was never spoken)
4. AUREON claimed to have switched to device 17 and be hearing real audio — **fabricated** (never ran any audio capture code)
5. All of this while `pyaudiowpatch` and `faster-whisper` were NOT INSTALLED

The LLM will always generate text. The fix is architectural: force it to read a real file before answering.
