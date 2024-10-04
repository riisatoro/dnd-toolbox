from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette import status

from database.caching import get_sheet


router = APIRouter(tags=["Health"])
templates = Jinja2Templates(directory="templates")


@router.post("/add_health")
def add_character_health(
        request: Request,
        character_id: str,
        health: int = Form(...),
):
    sheet = get_sheet(character_id)
    sheet.add_health(health)
    return RedirectResponse(f"/characters/{character_id}/combat", status_code=status.HTTP_302_FOUND)


@router.post("/add_damage")
def add_character_damage(
        request: Request,
        character_id: str,
        health: int = Form(...),
):
    sheet = get_sheet(character_id)
    sheet.add_damage(health)
    return RedirectResponse(f"/characters/{character_id}/combat", status_code=status.HTTP_302_FOUND)


@router.post("/add_temporary_hp")
def add_character_temporary_hp(
        request: Request,
        character_id: str,
        health: int = Form(...),
):
    sheet = get_sheet(character_id)
    sheet.add_temporary(health)
    return RedirectResponse(f"/characters/{character_id}/combat", status_code=status.HTTP_302_FOUND)
