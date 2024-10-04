from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette import status

from database.caching import get_sheet


router = APIRouter(tags=["Melee attacks"])
templates = Jinja2Templates(directory="templates")


@router.get("/melee")
def get_character_sheet(
        request: Request,
        character_id: str,
):
    sheet = get_sheet(character_id)
    return templates.TemplateResponse("melee/list.html", {"request": request, "data": sheet.render()})


@router.get("/melee/new")
def add_new_melee(
        request: Request,
        character_id: str,
):
    sheet = get_sheet(character_id)
    return templates.TemplateResponse("melee/new_melee.html", {"request": request, "data": sheet.render()})


@router.post("/melee/new")
def add_melee_weapon(
    request: Request,
    character_id: str,
    name: str = Form(...),
    hit_bonus: int = Form(...),
    damage_bonus: int = Form(...),
    hit_dice: str = Form(...),
    distance: str = Form(...),
    damage_type: str = Form(...),
):
    sheet = get_sheet(character_id)
    sheet.add_edit_melee(
        name, 
        {
            "hit_bonus": hit_bonus,
            "damage_bonus": damage_bonus,
            "damage": hit_dice,
            "damage_type": damage_type,
            "distance": distance
        }
    )
    return RedirectResponse(f"/characters/{character_id}/combat", status_code=status.HTTP_302_FOUND)


@router.get("/melee/{melee_key}/edit")
def add_new_melee(
        request: Request,
        character_id: str,
        melee_key: str,
):
    sheet = get_sheet(character_id)
    render = sheet.render()
    return templates.TemplateResponse(
        "melee/edit_melee.html", 
        {
            "request": request,
            "data": render,
            "key": melee_key,
            "form": render["melee"][melee_key]
        },
    )


@router.post("/melee/edit")
def add_melee_weapon(
    request: Request,
    character_id: str,
    name: str = Form(...),
    hit_bonus: int = Form(...),
    damage_bonus: int = Form(...),
    hit_dice: str = Form(...),
    distance: str = Form(...),
    damage_type: str = Form(...),
):
    sheet = get_sheet(character_id)
    sheet.add_edit_melee(
        name, 
        {
            "hit_bonus": hit_bonus,
            "damage_bonus": damage_bonus,
            "damage": hit_dice,
            "damage_type": damage_type,
            "distance": distance
        }
    )
    return RedirectResponse(f"/characters/{character_id}/combat", status_code=status.HTTP_302_FOUND)


@router.post("/melee/{melee_key}/delete")
def delete_melee_weapon(
    request: Request,
    character_id: str,
    melee_key: str,
):
    sheet = get_sheet(character_id)
    sheet.delete_melee(melee_key)
    return RedirectResponse(f"/characters/{character_id}/combat", status_code=status.HTTP_302_FOUND)
