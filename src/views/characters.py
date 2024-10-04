from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette import status

from database.caching import get_sheet
from views.health import router as health_router
from views.melee import router as melee_router
from views.consumables import router as consumables_router


router = APIRouter(prefix="/characters/{character_id}")
templates = Jinja2Templates(directory="templates")


router.include_router(melee_router)
router.include_router(health_router)
router.include_router(consumables_router)


@router.post("/add_spell_slot")
def add_spell_slot(
        request: Request,
        character_id: str,
        level: str = Form(...),
):
    sheet = get_sheet(character_id)
    sheet.add_spell_slot(level)
    return RedirectResponse(f"/characters/{character_id}/combat", status_code=status.HTTP_302_FOUND)


@router.post("/remove_spell_slot")
def remove_spell_slot(
        request: Request,
        character_id: str,
        level: str = Form(...),
):
    sheet = get_sheet(character_id)
    sheet.remove_spell_slot(level)
    return RedirectResponse(f"/characters/{character_id}/combat", status_code=status.HTTP_302_FOUND)


@router.post("/restore_spell_slots")
def restore_spell_slots(
        request: Request,
        character_id: str,
):
    sheet = get_sheet(character_id)
    sheet.restore_spell_slots()
    return RedirectResponse(f"/characters/{character_id}/combat", status_code=status.HTTP_302_FOUND)


@router.post("/remove_consumable")
def remove_consumable(
        request: Request,
        character_id: str,
        consumable: str = Form(...),
):
    sheet = get_sheet(character_id)
    sheet.remove_consumable(consumable)
    return RedirectResponse(f"/characters/{character_id}/combat", status_code=status.HTTP_302_FOUND)


@router.post("/add_consumable")
def add_consumable(
        request: Request,
        character_id: str,
        consumable: str = Form(...),
):
    sheet = get_sheet(character_id)
    sheet.add_consumable(consumable)
    return RedirectResponse(f"/characters/{character_id}/combat", status_code=status.HTTP_302_FOUND)


@router.post("/add_coins")
def add_coins(
        request: Request,
        character_id: str,
        coins: int = Form(...),
        coin_type: str = Form(...),
):
    sheet = get_sheet(character_id)
    sheet.add_coins(coin_type, coins)
    return RedirectResponse(f"/characters/{character_id}/inventory", status_code=status.HTTP_302_FOUND)


@router.post("/remove_coins")
def remove_coins(
        request: Request,
        character_id: str,
        coins: int = Form(...),
        coin_type: str = Form(...),
):
    sheet = get_sheet(character_id)
    sheet.remove_coins(coin_type, coins)
    return RedirectResponse(f"/characters/{character_id}/inventory", status_code=status.HTTP_302_FOUND)


@router.post("/increase_inventory_item")
def increase_inventory_item(
        request: Request,
        character_id: str,
        item: str = Form(...),
):
    sheet = get_sheet(character_id)
    sheet.increase_inventory_item(item)
    return RedirectResponse(f"/characters/{character_id}/inventory", status_code=status.HTTP_302_FOUND)


@router.post("/decrease_inventory_item")
def decrease_inventory_item(
        request: Request,
        character_id: str,
        item: str = Form(...),
):
    sheet = get_sheet(character_id)
    sheet.decrease_inventory_item(item)
    return RedirectResponse(f"/characters/{character_id}/inventory", status_code=status.HTTP_302_FOUND)


@router.post("/add_inventory_item")
def add_inventory_item(
        request: Request,
        character_id: str,
        item: str = Form(...),
        value: int | None = Form(...),
        description: str | None = Form(...),
):
    sheet = get_sheet(character_id)
    sheet.add_inventory_item(item, value, description)
    return RedirectResponse(f"/characters/{character_id}/inventory", status_code=status.HTTP_302_FOUND)


template_mapper = {
    "base": "character_sheet/base.html",
    "combat": "character_sheet/combat.html",
    "abilities": "character_sheet/abilities.html",
    "inventory": "character_sheet/inventory.html",
    # "add_inventory_item": "character_sheet/add_inventory_item.html",
}


@router.get("/base")
def get_character_sheet(
        request: Request,
        character_id: str,
):
    sheet = get_sheet(character_id)
    return templates.TemplateResponse(template_mapper['base'], {"request": request, "data": sheet.render()})


@router.get("/combat")
def get_character_sheet(
        request: Request,
        character_id: str,
):
    sheet = get_sheet(character_id)
    return templates.TemplateResponse(template_mapper['combat'], {"request": request, "data": sheet.render()})


@router.get("/abilities")
def get_character_sheet(
        request: Request,
        character_id: str,
):
    sheet = get_sheet(character_id)
    return templates.TemplateResponse(template_mapper['abilities'], {"request": request, "data": sheet.render()})


@router.get("/inventory")
def get_character_sheet(
        request: Request,
        character_id: str,
):
    sheet = get_sheet(character_id)
    return templates.TemplateResponse(template_mapper['inventory'], {"request": request, "data": sheet.render()})
