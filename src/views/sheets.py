from typing import Annotated

from fastapi import APIRouter, Form
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from database.queries.sheets import (
    get_sheets,
    create_sheet,
    update_sheet,
    delete_sheet,
)
from database.models.sheets import CHARACTER_PERSONALITY_TEMPLATE
from security.security import AuthDepends


router = APIRouter(
    tags=["Sheets"],
    prefix="/sheets",
)

templates = Jinja2Templates(directory="templates")


@router.get("/")
def sheets_page_render(
        request: Request,
        user: AuthDepends,
):
    sheets = get_sheets(user.id)
    return templates.TemplateResponse(
        "sheets/sheets.html",
        {"request": request, "user": user, "sheets": sheets}
    )


@router.get("/{sheet_id}")
def sheet_page_render(
        request: Request,
        user: AuthDepends,
        sheet_id: int,
):
    sheet = get_sheets(user.id, sheet_id)
    return templates.TemplateResponse(
        "sheets/detail_sheet.html",
        {"request": request, "user": user, "sheet": sheet}
    )


@router.get("/new")
def create_sheet_page_render(
        request: Request,
        user: AuthDepends,
):
    return templates.TemplateResponse(
        "sheets/new.html",
        {"request": request, "user": user}
    )


@router.post("/new")
def create_sheet_template(
        request: Request,
        user: AuthDepends,
        name: Annotated[str, Form()],
        level: Annotated[int, Form()],
        race: Annotated[str, Form()],
        class_: Annotated[str, Form()],
        sheet_type: Annotated[str, Form()],
):
    personality = {
        **CHARACTER_PERSONALITY_TEMPLATE,
        "sheet_type": sheet_type,
        "class_": class_,
        "race": race,
        "level": level,
    }
    sheet = create_sheet({"personality": personality, "name": name, "user_id": user.id})
    return RedirectResponse(f"/sheets/{sheet.id}", 303)

