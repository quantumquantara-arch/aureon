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
