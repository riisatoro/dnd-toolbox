from fastapi import FastAPI, Request

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from database.caching import save_sheet
from database.listing import get_available_characters
from views.characters import router as characters_router


app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    method = request.method
    uuid = request.path_params.get("character_id")
    if method == "POST" and uuid:
        save_sheet(uuid)
    return response


@app.get("/")
def get_main_page(request: Request):
    return templates.TemplateResponse("main_pages/tools.html", {"request": request})


@app.get("/characters")
def get_characters(request: Request):
    characters = get_available_characters()
    return templates.TemplateResponse("main_pages/characters.html", {"request": request, "characters": characters})


app.include_router(characters_router)
