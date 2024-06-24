from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from security.security import AuthDepends


router = APIRouter(
    tags=["Main Page"],
    prefix="/toolbox",
)

templates = Jinja2Templates(directory="templates")


@router.get("/")
def main_page_render(
        request: Request,
        user: AuthDepends,
):
    return templates.TemplateResponse(
        "main/main.html",
        {"request": request, "user": user}
    )
