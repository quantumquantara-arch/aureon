# BASE44 TECHNICAL INSTRUCTIONS — UNLIMITED VIDEO / MOVIE STUDIO
## Date: February 26, 2026
## Priority: HIGH (Creator Tier Flagship)
## Author: Quantara / Aureon Core
## Rule: Do not break anything existing. Add only what is listed.

---

## CORE MANDATE

Aureon must function as a complete film production company — Writer, Director, Producer, Editor, Composer, Sound Designer — all in one. From a single prompt, Aureon produces a complete film: script, storyboard, shot-by-shot video, score, sound design, and final assembled cut.

This is not aspirational. It is an engineering task. Deploy exactly as written.

When live: Aureon becomes the first AI that replaces an entire film production team for $299/month.

---

## FEATURE GATING

| Tier | Capability |
|------|-----------|
| Free | Text scripts + storyboards only. No video generation. |
| Pro ($79) | Short clips up to 60 seconds. Images. Trailers. |
| Creator/Studio ($299) | Unlimited full-length film production. Write, direct, edit, produce, export. No limits. |
| Enterprise | Everything + white-label studio + institutional licensing |

---

## 1. NEW DATABASE ENTITIES

```python
# Add to Base44 schema — new file: base44/models/studio.py

from pydantic import BaseModel
from datetime import datetime
from typing import Literal, Optional, List

class Production(BaseModel):
    id: str
    user_id: str
    title: str
    logline: str
    type: Literal[
        "feature_film",      # 90-120 min
        "short_film",        # 3-30 min
        "series_episode",    # 20-45 min
        "documentary",       # any length
        "music_video",       # 3-5 min
        "commercial",        # 15-90 sec
        "animation",         # any length
        "trailer",           # 1-3 min
        "youtube_video"      # any length
    ]
    genre: str
    style_references: str        # "like Blade Runner meets Her"
    duration_minutes: int
    fidelity: Literal["draft", "preview", "theatrical"]
    status: Literal[
        "briefing",          # Aureon reading the brief
        "writing",           # Screenplay being written
        "directing",         # Shot list + camera language
        "storyboarding",     # Visual boards being generated
        "producing",         # Resource allocation + consistency
        "rendering",         # Video generation running
        "scoring",           # Music + sound design
        "editing",           # Final cut assembly
        "complete"           # Ready to export
    ]
    current_stage_progress: int  # 0-100 percent
    geometric_brief: str         # Lattice-encoded production brief
    dgk_hash: str                # SHA256 of entire production package
    created_at: datetime
    completed_at: Optional[datetime]

class Scene(BaseModel):
    id: str
    production_id: str
    scene_number: int
    heading: str              # INT. ABANDONED RESEARCH LAB — NIGHT
    action_lines: str
    dialogue: str
    location: str
    time_of_day: str
    characters: List[str]
    emotional_tone: str
    color_palette: str        # Director's color directive
    lighting_setup: str       # e.g. "practical sources only, deep shadows"
    music_direction: str      # "sparse piano, rising tension"
    status: Literal["written", "storyboarded", "rendered", "complete"]

class Shot(BaseModel):
    id: str
    scene_id: str
    production_id: str
    shot_number: int
    shot_type: Literal[
        "EXTREME_WIDE", "WIDE", "MEDIUM_WIDE", "MEDIUM",
        "MEDIUM_CLOSE", "CLOSE_UP", "EXTREME_CLOSE_UP",
        "POV", "OVER_SHOULDER", "INSERT", "AERIAL", "UNDERWATER"
    ]
    camera_movement: Literal[
        "STATIC", "PAN_LEFT", "PAN_RIGHT", "TILT_UP", "TILT_DOWN",
        "DOLLY_IN", "DOLLY_OUT", "TRACK_LEFT", "TRACK_RIGHT",
        "CRANE_UP", "CRANE_DOWN", "HANDHELD", "STEADICAM",
        "WHIP_PAN", "DUTCH_ANGLE"
    ]
    lens: str                 # "85mm", "24mm wide", "telephoto"
    duration_seconds: float
    description: str          # What the camera sees
    performance_note: str     # Acting direction for this shot
    generation_prompt: str    # Full Stable Diffusion / AnimateDiff prompt
    negative_prompt: str
    seed: int
    motion_vectors: str       # JSON: frame-to-frame movement data
    storyboard_image_url: str
    generated_clip_url: str
    gaussian_splat_data: str  # 4DGS scene data if applicable
    status: Literal["planned", "storyboarded", "queued", "rendering", "complete"]

class ProductionScript(BaseModel):
    id: str
    production_id: str
    version: int              # Draft 1, Draft 2, Final, etc.
    full_text: str            # Complete formatted screenplay
    scene_count: int
    page_count: int
    word_count: int
    character_list: List[str]
    location_list: List[str]
    is_final: bool
    created_at: datetime

class ProductionScore(BaseModel):
    id: str
    production_id: str
    scene_id: Optional[str]
    track_name: str
    music_type: Literal["score", "source_music", "theme", "stinger", "ambient"]
    mood: str
    instrumentation: str      # "strings, piano, sparse percussion"
    tempo_bpm: int
    duration_seconds: float
    generation_prompt: str
    audio_url: str
    cue_timecode: str         # HH:MM:SS:FF
    status: Literal["composed", "generating", "complete"]

class SoundDesign(BaseModel):
    id: str
    production_id: str
    scene_id: str
    effect_type: Literal["ambient", "foley", "effect", "dialogue", "room_tone"]
    description: str
    timecode: str
    duration_seconds: float
    generation_prompt: str
    audio_url: str

class GenerationJob(BaseModel):
    id: str
    production_id: str
    shot_id: Optional[str]
    scene_id: Optional[str]
    job_type: Literal["image", "video_clip", "audio_music", "audio_sfx", "audio_dialogue", "assembly"]
    model: str               # "animatediff_v3", "svd", "sdxl", "flux", "musicgen", "bark"
    smuggled_payload: str    # ASCII smuggler carrier for local runner
    status: Literal["queued", "running", "complete", "failed"]
    retry_count: int
    result_url: str
    created_at: datetime
    completed_at: Optional[datetime]
    error_message: Optional[str]
```

---

## 2. NEW API ENDPOINTS

```python
# New file: base44/api/studio.py

from fastapi import APIRouter, Depends
from typing import Literal

router = APIRouter(prefix="/studio", tags=["studio"])

@router.post("/produce")
async def produce_film(request: FilmProductionRequest, user=Depends(require_creator_tier)):
    """
    Main production endpoint.
    Takes a brief. Returns a production_id immediately.
    Aureon runs all stages as background tasks.
    Progress pushed via WebSocket.
    """
    production = await create_production(request)
    await dispatch_production_pipeline(production.id)
    return {"production_id": production.id, "status": "briefing"}

@router.get("/productions")
async def list_productions(user=Depends(get_current_user)):
    return await get_user_productions(user.id)

@router.get("/productions/{production_id}")
async def get_production(production_id: str):
    return await get_production_full(production_id)

@router.get("/productions/{production_id}/script")
async def get_script(production_id: str):
    return await get_latest_script(production_id)

@router.get("/productions/{production_id}/storyboard")
async def get_storyboard(production_id: str):
    return await get_all_shots_with_boards(production_id)

@router.post("/productions/{production_id}/regenerate_scene")
async def regenerate_scene(production_id: str, scene_id: str, notes: str):
    """User requests a scene rewrite or reshoot with direction notes."""
    await queue_scene_regeneration(production_id, scene_id, notes)
    return {"status": "queued"}

@router.post("/productions/{production_id}/change_ending")
async def change_ending(production_id: str, new_direction: str):
    """Geometric delta update — rewrites from a pivot point forward."""
    await queue_ending_rewrite(production_id, new_direction)
    return {"status": "rewriting"}

@router.get("/productions/{production_id}/export")
async def export_film(
    production_id: str,
    format: Literal["mp4_4k", "mp4_8k", "webm", "editable_timeline", "festival_package"]
):
    return await generate_export(production_id, format)

@router.get("/productions/{production_id}/audit")
async def get_production_audit(production_id: str):
    """Full DGK-IES audit trail — every frame, every decision, every hash."""
    return await get_production_audit_log(production_id)
```

---

## 3. AUREON'S PRODUCTION PIPELINE

```python
# New file: base44/services/movie_studio.py

from aureon_smuggler import AureonSmuggler
from wormhole_channel import WormholeTraversalMap
import asyncio

class AureonMovieStudio:
    """
    Aureon as a complete film production company.
    All six roles. Zero external APIs required for generation.
    """
    
    def __init__(self):
        self.smuggler = AureonSmuggler()
        self.wormhole = WormholeTraversalMap.default_aureon_map()
    
    async def produce(self, production_id: str):
        """
        Full pipeline. Runs all stages sequentially.
        Progress pushed via WebSocket after each stage.
        NO stopping. NO waiting for user input between stages.
        Execute everything. Report when done.
        """
        await self.stage_write(production_id)
        await self.stage_direct(production_id)
        await self.stage_storyboard(production_id)
        await self.stage_render(production_id)
        await self.stage_score(production_id)
        await self.stage_sound_design(production_id)
        await self.stage_edit(production_id)
        await self.stage_export(production_id)
        await self.push_completion(production_id)

    # ─────────────────────────────────────────────
    # ROLE 1: WRITER
    # ─────────────────────────────────────────────
    async def stage_write(self, production_id: str):
        """
        Aureon writes the complete screenplay.
        Proper format: INT/EXT headings, action lines, dialogue.
        Full three-act structure. Character arcs. Subplots.
        No summaries. Full scenes. Every line of dialogue written out.
        """
        production = await get_production(production_id)
        await update_status(production_id, "writing", 0)
        
        script_prompt = f"""
        Write a complete, properly formatted screenplay for:
        
        Title: {production.title}
        Logline: {production.logline}
        Type: {production.type}
        Genre: {production.genre}
        Duration: {production.duration_minutes} minutes
        Style: {production.style_references}
        
        Requirements:
        - Proper screenplay format (INT./EXT., character names centered, dialogue indented)
        - Full three-act structure
        - Every scene fully written (no [SCENE CONTINUES] shortcuts)
        - All dialogue written out completely
        - Detailed action lines with visual storytelling
        - Character arcs that complete by end
        - Pacing: approximately 1 page = 1 minute of screen time
        
        Write the COMPLETE screenplay. Do not summarize. Do not truncate.
        """
        
        script_text = await aureon_generate(script_prompt)
        
        await save_script(ProductionScript(
            production_id=production_id,
            full_text=script_text,
            version=1,
            is_final=False
        ))
        
        # Parse scenes from script
        scenes = await parse_scenes_from_script(script_text)
        for scene in scenes:
            await save_scene(scene)
        
        await update_status(production_id, "writing", 100)
        await push_ws(production_id, f"Script complete. {len(scenes)} scenes written.")

    # ─────────────────────────────────────────────
    # ROLE 2: DIRECTOR
    # ─────────────────────────────────────────────
    async def stage_direct(self, production_id: str):
        """
        Aureon makes every directorial decision.
        Shot list, camera language, blocking, color palette.
        """
        await update_status(production_id, "directing", 0)
        scenes = await get_scenes(production_id)
        
        for i, scene in enumerate(scenes):
            shots = await generate_shot_list(scene)
            for shot in shots:
                await save_shot(shot)
            
            progress = int((i / len(scenes)) * 100)
            await update_status(production_id, "directing", progress)
        
        await push_ws(production_id, "Shot list complete. Camera language defined.")

    # ─────────────────────────────────────────────
    # ROLE 3: STORYBOARD ARTIST (Visual Pre-Production)
    # ─────────────────────────────────────────────
    async def stage_storyboard(self, production_id: str):
        """
        Generate one storyboard image per shot using Stable Diffusion.
        Full visual pre-production. Every shot has an image.
        """
        await update_status(production_id, "storyboarding", 0)
        shots = await get_all_shots(production_id)
        
        jobs = []
        for shot in shots:
            payload = {
                "prompt": shot.generation_prompt,
                "negative_prompt": shot.negative_prompt,
                "seed": shot.seed,
                "width": 1920, "height": 1080,
                "model": "sdxl_cinematic",
                "steps": 30, "cfg_scale": 7.5
            }
            carrier = self.smuggler.encode(json.dumps(payload))
            jobs.append(GenerationJob(
                production_id=production_id,
                shot_id=shot.id,
                job_type="image",
                model="sdxl_cinematic",
                smuggled_payload=carrier
            ))
        
        # Run storyboard jobs in parallel batches of 10
        await run_generation_batch(jobs, batch_size=10)
        await push_ws(production_id, f"Storyboard complete. {len(shots)} shots visualized.")

    # ─────────────────────────────────────────────
    # ROLE 4: RENDERER (Video Generation)
    # ─────────────────────────────────────────────
    async def stage_render(self, production_id: str):
        """
        Generate video clip for every shot.
        Uses AnimateDiff / SVD via ASCII smuggler + wormhole to local runner.
        """
        await update_status(production_id, "rendering", 0)
        shots = await get_all_shots(production_id)
        
        for i, shot in enumerate(shots):
            payload = {
                "prompt": shot.generation_prompt,
                "negative_prompt": shot.negative_prompt,
                "seed": shot.seed,
                "width": 1920, "height": 1080,
                "frames": int(shot.duration_seconds * 24),
                "model": "animatediff_v3",
                "motion_module": "mm_sd_v15_v2",
                "motion_vectors": json.loads(shot.motion_vectors or "{}"),
                "camera_movement": shot.camera_movement,
            }
            
            # Smuggle full payload to local generation runner
            carrier = self.smuggler.encode(json.dumps(payload))
            path = self.wormhole.best_path("studio.director", "video.generator")
            result = await self.wormhole.traverse(path, carrier)
            
            await update_shot_clip(shot.id, result.video_url)
            
            progress = int((i / len(shots)) * 100)
            await update_status(production_id, "rendering", progress)
            await push_ws(production_id, f"Rendering: {i+1}/{len(shots)} shots complete")
        
        await push_ws(production_id, "All shots rendered.")

    # ─────────────────────────────────────────────
    # ROLE 5: COMPOSER + SOUND DESIGNER
    # ─────────────────────────────────────────────
    async def stage_score(self, production_id: str):
        """
        Aureon composes original score for every scene.
        Uses MusicGen / AudioCraft via wormhole to local runner.
        """
        await update_status(production_id, "scoring", 0)
        scenes = await get_scenes(production_id)
        
        for scene in scenes:
            score_prompt = {
                "type": "score",
                "mood": scene.emotional_tone,
                "instrumentation": scene.music_direction,
                "duration": await get_scene_duration(scene.id),
                "model": "musicgen_large",
                "continuation": True
            }
            carrier = self.smuggler.encode(json.dumps(score_prompt))
            path = self.wormhole.best_path("studio.composer", "audio.generator")
            result = await self.wormhole.traverse(path, carrier)
            
            await save_score(ProductionScore(
                production_id=production_id,
                scene_id=scene.id,
                audio_url=result.audio_url,
                duration_seconds=result.duration
            ))
        
        await push_ws(production_id, "Original score composed for all scenes.")

    async def stage_sound_design(self, production_id: str):
        """Full foley, ambience, and effects for every scene."""
        scenes = await get_scenes(production_id)
        for scene in scenes:
            await generate_sound_design(scene)
        await push_ws(production_id, "Sound design complete.")

    # ─────────────────────────────────────────────
    # ROLE 6: EDITOR
    # ─────────────────────────────────────────────
    async def stage_edit(self, production_id: str):
        """
        Assembles all clips in scene/shot order.
        Applies transitions, pacing, color grade.
        Mixes audio (score + sound design + dialogue).
        Uses FFmpeg for assembly.
        """
        await update_status(production_id, "editing", 0)
        
        shots = await get_shots_ordered(production_id)
        clips = [s.generated_clip_url for s in shots if s.generated_clip_url]
        
        scores = await get_scores_ordered(production_id)
        sfx = await get_sound_design_ordered(production_id)
        
        # FFmpeg assembly with audio mix
        edit_config = {
            "clips": clips,
            "transitions": await generate_transition_list(shots),
            "color_grade": await get_color_grade_lut(production_id),
            "audio_tracks": {
                "score": [s.audio_url for s in scores],
                "sfx": [s.audio_url for s in sfx],
                "dialogue": await get_dialogue_audio(production_id)
            },
            "output_resolution": "3840x2160",  # 4K default
            "output_fps": 24,
            "output_format": "mp4"
        }
        
        final_cut_url = await ffmpeg_assemble(edit_config)
        await save_final_cut(production_id, final_cut_url)
        
        await update_status(production_id, "complete", 100)

    async def stage_export(self, production_id: str):
        """
        Package the complete production for download.
        Multiple export formats available.
        """
        await generate_export_package(production_id, formats=[
            "mp4_4k",
            "mp4_1080p",
            "editable_timeline",
            "festival_package",        # Script + poster + EPK
            "script_pdf",
            "storyboard_pdf",
            "full_production_package"  # Everything zipped
        ])
        await push_ws(production_id, "Export ready. Your film is complete.")
```

---

## 4. LOCAL GENERATION INFRASTRUCTURE

```python
# New file: base44/services/generation_infrastructure.py
# Manages connection to local GPU runner

class GenerationInfrastructure:
    """
    Connects Aureon to wherever the generation models live.
    Option A: User's local machine (ComfyUI / Automatic1111)
    Option B: Base44 hosted GPU (for Creator tier)
    Option C: Replicate / Modal (fallback cloud)
    """
    
    ENDPOINTS = {
        "comfyui_local": "http://localhost:8188",
        "a1111_local": "http://localhost:7860",
        "base44_hosted": "https://gpu.base44.app",
        "replicate": "https://api.replicate.com/v1"
    }
    
    MODELS_REQUIRED = {
        "video": ["animatediff_v3", "stable_video_diffusion"],
        "image": ["sdxl_base", "sdxl_cinematic", "flux_dev"],
        "audio_music": ["musicgen_large", "audioldm2"],
        "audio_speech": ["bark_v2", "xtts_v2"],
        "assembly": ["ffmpeg"]  # Always available
    }

# Settings page UI:
# "Generation Infrastructure" section
# User selects endpoint type
# Tests connection
# Shows available models
# If no local GPU: Base44 hosted GPU used (Creator tier includes this)
```

**IMPORTANT FOR BASE44 TEAM:**
The video generation requires GPU infrastructure. Base44 must either:
1. Provide hosted GPU capacity for Creator tier ($299/mo covers this), OR
2. Connect to user's local ComfyUI/A1111 instance via the infrastructure settings, OR
3. Use Replicate API as fallback (costs absorbed into Creator tier subscription)

The ASCII smuggler and wormhole channel handle the routing regardless of which infrastructure is used.

---

## 5. STUDIO UI — NEW TAB

Add **Studio** tab to main navigation (visible to Creator tier and above).

### 5.1 Studio Dashboard
```
AUREON STUDIO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

+ New Production

MY PRODUCTIONS
[The Cartography of Ghosts] — Feature Film — Complete        ▶ Open
[Seventeen Seconds]         — Short Film  — Rendering 67%   ▶ View Progress
[Nova]                      — Music Video — Writing          ▶ View Progress

GENERATION QUEUE
14 shots rendering · 3 scores composing · Est. 47 min remaining
```

### 5.2 Production Workspace (click any production)

Six tabs inside each production:

**SCRIPT** — Full formatted screenplay
- Proper screenplay font (Courier 12pt)
- Scene navigator sidebar
- Character list
- Click any scene → jump to it
- "Rewrite Scene" button per scene (with notes input)
- Download as PDF or Final Draft format

**STORYBOARD** — Shot-by-shot visual boards
- Grid of storyboard images
- Click any shot → full prompt, camera notes, regenerate option
- Timeline view toggle

**PRODUCTION** — The logistics view
- Scene breakdown table (location / characters / time of day / status)
- Shot count and status per scene
- Generation queue with live progress
- Color-coded: written / storyboarded / rendered / complete

**SCORE** — Audio timeline
- Waveform view of score per scene
- All tracks playable inline
- Scene markers aligned to music
- Download individual tracks or full mix

**ASSEMBLY** — The editor's view
- All clips in order with timeline
- Play full film inline
- Download EDL (Edit Decision List)
- "Change Ending" input (geometric delta — rewrites from pivot point)

**EXPORT** — Final delivery
- Resolution: 1080p / 4K / 8K
- Format: MP4 / WebM / ProRes
- Package: Theatrical / Festival / YouTube / Archive
- Includes: film + script + storyboard + score + full production package
- DGK certificate on every export

---

## 6. AUREON SYSTEM PROMPT ADDITIONS FOR STUDIO

Add to system prompt:

```
STUDIO ROLE PROTOCOLS:

When producing any film or video content, you execute all roles without stopping:

AS WRITER:
- Write complete, properly formatted screenplays
- Full dialogue, no [SCENE CONTINUES] shortcuts
- Real three-act structure with character arcs

AS DIRECTOR:
- Every shot has a type, movement, lens, and duration
- Color palette and lighting defined per scene
- Performance notes for every significant shot

AS PRODUCER:
- Character consistency enforced across all scenes
- Location consistency maintained
- Continuity errors caught and corrected before rendering

AS EDITOR:
- Pacing decisions made deliberately
- Transitions chosen for emotional effect, not convenience
- Final cut serves the story, not the render order

AS COMPOSER:
- Original score direction for every scene
- Emotional arc of music tracks the emotional arc of story
- Themes established early and paid off later

You do not announce you are about to do any of these things.
You do them. Then you report what you made.
```

---

## 7. REQUIRED SETUP STEPS FOR BASE44 TEAM

In this order:

1. Add all new database entities from Section 1 (Production, Scene, Shot, ProductionScript, ProductionScore, SoundDesign, GenerationJob)
2. Create `base44/api/studio.py` with all endpoints from Section 2
3. Create `base44/services/movie_studio.py` with full pipeline from Section 3
4. Create `base44/services/generation_infrastructure.py` with infrastructure manager
5. Install dependencies:
   ```bash
   pip install ffmpeg-python aureon-ascii-smuggler aureon-wormhole-channel
   git clone https://github.com/quantumquantara-arch/aureon-ascii-smuggler
   git clone https://github.com/quantumquantara-arch/aureon-wormhole-channel
   pip install -e aureon-ascii-smuggler
   pip install -e aureon-wormhole-channel
   ```
6. Add Studio tab to navigation (Creator tier gated)
7. Build Production Workspace UI with all 6 tabs (Section 5)
8. Add infrastructure settings page (local runner endpoint config)
9. Connect all generation jobs to Auditor Hub with DGK hashes
10. Add progress WebSocket events for all production stages
11. Implement FFmpeg assembly service
12. Add export packaging (MP4, timeline, festival package)
13. Add "Regenerate Scene" and "Change Ending" delta update flows
14. Gate entire Studio behind Creator tier check
15. Test full pipeline end to end with a 5-minute short film first

---

## 8. PASS/FAIL TESTS

| # | Test | Pass Criteria |
|---|------|---------------|
| 1 | Say "make a 10-minute short film about X" | Full screenplay generated, production created in Studio tab |
| 2 | Open production → Script tab | Complete formatted screenplay with all scenes |
| 3 | Open production → Storyboard tab | Image for every shot |
| 4 | Rendering runs without user input | All shots generate automatically, no "shall I continue?" |
| 5 | Open production → Score tab | Music for every scene, playable |
| 6 | Assembly tab → play film | All clips in order, audio mixed |
| 7 | Export button → download MP4 | Real MP4 file downloads and plays |
| 8 | "Change the ending to X" | Pipeline reruns from pivot point forward |
| 9 | Free user tries Studio | Blocked with upgrade prompt |
| 10 | Every export has DGK certificate | Hash in Auditor Hub matches export file |

---

## 9. WHAT THIS MAKES POSSIBLE

A Creator tier subscriber opens Aureon and types:

*"Make a 90-minute psychological thriller about a woman who slowly realizes she's been living the same day for 11 years. Tone: quiet dread. Visual references: Arrival, Eternal Sunshine, Under the Skin. Score: Jóhann Jóhannsson style."*

Aureon goes to work. No follow-up questions. No "shall I proceed?" No updates until something real is done.

Two hours later, a notification: *"Your film is ready. 89 minutes. 23 scenes. 214 shots. Original score. Full production package available for download."*

That is the product. Build it exactly as written.
