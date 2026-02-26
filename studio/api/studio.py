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
