from fastapi import FastAPI, Request

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from database.caching import save_sheet
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
    return templates.TemplateResponse("main.html", {"request": request})


app.include_router(characters_router)
