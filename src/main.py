import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from exceptions.authorization import NotAuthorizedError


app = FastAPI(
    title="D&N Toolbox",
    description="List of API methods for D&N Toolbox. API itself is not used, server renders the Jinja2 templates."
)

origins = os.getenv("CORS_ORIGINS", "*").split(" ")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(NotAuthorizedError)
def handle_not_authorized_error(_, __):
    return JSONResponse({"detail": "Not authorized"}, status_code=401)
