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
