from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette import status

from database.caching import get_sheet


router = APIRouter(tags=["New character"], prefix="/new-character")
templates = Jinja2Templates(directory="templates")


@router.get("/")
def get_new_character_form(request: Request):
    return templates.TemplateResponse("new_character/form.html", {"request": request})


@router.post("/add")
def create_new_character(
        request: Request,
        name: str = Form(...),
        class_: str = Form(...),
        level: int = Form(...),
        alignment: str = Form(...),
        background: str = Form(...),
        str_: int = Form(...),
        dex_: int = Form(...),
        con_: int = Form(...),
        int_: int = Form(...),
        wis_: int = Form(...),
        cha_: int = Form(...),
        str_save: bool = Form(...),
        dex_save: bool = Form(...),
        con_save: bool = Form(...),
        int_save: bool = Form(...),
        wis_save: bool = Form(...),
        cha_save: bool = Form(...),
        
):
    return
