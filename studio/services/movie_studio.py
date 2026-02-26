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
