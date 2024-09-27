from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette import status

from database.caching import get_sheet
from database.listing import get_available_characters


router = APIRouter(prefix="/characters")
templates = Jinja2Templates(directory="templates")


@router.get("/")
def get_characters(request: Request):
    characters = get_available_characters()
    return templates.TemplateResponse("character_sheet/characters.html", {"request": request, "characters": characters})


@router.get("/{character_id}/{template}")
def get_character_sheet(
        request: Request,
        character_id: str,
        template: str,
):
    sheet = get_sheet(character_id)
    template_mapper = {
        "base": "character_sheet/base.html",
        "combat": "character_sheet/combat.html",
    }

    return templates.TemplateResponse(template_mapper[template], {"request": request, "data": sheet.to_render()})


@router.post("/{character_id}/add_health")
def add_character_health(
        request: Request,
        character_id: str,
        health: int = Form(...),
):
    sheet = get_sheet(character_id)
    sheet.add_health(health)
    return RedirectResponse(f"/characters/{character_id}/combat", status_code=status.HTTP_302_FOUND)


@router.post("/{character_id}/add_damage")
def add_character_damage(
        request: Request,
        character_id: str,
        health: int = Form(...),
):
    sheet = get_sheet(character_id)
    sheet.add_damage(health)
    return RedirectResponse(f"/characters/{character_id}/combat", status_code=status.HTTP_302_FOUND)


@router.post("/{character_id}/add_temporary_hp")
def add_character_temporary_hp(
        request: Request,
        character_id: str,
        health: int = Form(...),
):
    sheet = get_sheet(character_id)
    sheet.add_temporary_hp(health)
    return RedirectResponse(f"/characters/{character_id}/combat", status_code=status.HTTP_302_FOUND)


@router.post("/{character_id}/remove_spell_slot")
def remove_spell_slot(
        request: Request,
        character_id: str,
        level: str = Form(...),
):
    sheet = get_sheet(character_id)
    sheet.remove_spell_slot(level)
    return RedirectResponse(f"/characters/{character_id}/combat", status_code=status.HTTP_302_FOUND)


@router.post("/{character_id}/restore_spell_slots")
def restore_spell_slots(
        request: Request,
        character_id: str,
):
    sheet = get_sheet(character_id)
    sheet.restore_spell_slots()
    return RedirectResponse(f"/characters/{character_id}/combat", status_code=status.HTTP_302_FOUND)