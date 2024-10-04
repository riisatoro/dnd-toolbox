from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette import status

from database.caching import get_sheet


router = APIRouter(tags=["Combat Consumables"], prefix="/consumables")
templates = Jinja2Templates(directory="templates")


@router.get("/")
def get_character_sheet(
        request: Request,
        character_id: str,
):
    sheet = get_sheet(character_id)
    return templates.TemplateResponse(
        "consumables/list.html", 
        {
            "request": request,
            "data": sheet.render(),
        }
    )


@router.get("/new")
def get_new_consumable_form(request: Request, character_id: str):
    sheet = get_sheet(character_id)
    return templates.TemplateResponse("consumables/new_consumable.html", {"request": request, "data": sheet.render()})


@router.post("/new")
def create_consumable(
        request: Request,
        character_id: str,
        name: str = Form(...),
        total: int = Form(...),
        value: int = Form(...),
        reset_rule: str | None = Form(...),
):
    sheet = get_sheet(character_id)
    sheet.add_edit_consumable(name, {"total": total, "value": value, "reset_rule": reset_rule})
    return RedirectResponse(f"/characters/{character_id}/consumables/", status_code=status.HTTP_302_FOUND)


@router.get("/{consumable_key}/edit")
def get_edit_consumable_form(
    request: Request,
    character_id: str,
    consumable_key: str,
):
    sheet = get_sheet(character_id)
    render = sheet.render()
    return templates.TemplateResponse(
        "consumables/edit_consumable.html", 
        {"request": request, "data": sheet.render(), "key": consumable_key, "form": render["consumables"][consumable_key]}
    )


@router.post("/edit")
def edit_consumable(
        request: Request,
        character_id: str,
        name: str = Form(...),
        total: int = Form(...),
        value: int = Form(...),
        reset_rule: str | None = Form(...),
):
    sheet = get_sheet(character_id)
    sheet.add_edit_consumable(name, {"total": total, "value": value, "reset_rule": reset_rule})
    return RedirectResponse(f"/characters/{character_id}/consumables/", status_code=status.HTTP_302_FOUND)


@router.post("/{consumable}/delete")
def delete_consumable(
        request: Request,
        character_id: str,
        consumable: str,
):
    sheet = get_sheet(character_id)
    sheet.delete_consumable(consumable)
    return RedirectResponse(f"/characters/{character_id}/consumables/", status_code=status.HTTP_302_FOUND)
