from typing import Annotated

import bcrypt
from fastapi import APIRouter, Form
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from database.queries.users import (
    is_user_exists,
    get_user_by_email,
    create_new_user,
)

from security.security import JWTSecurity

router = APIRouter(
    tags=["Authorization"],
    prefix="/auth",
)

templates = Jinja2Templates(directory="templates")


@router.get("/signup")
def sign_up_template(request: Request):
    return templates.TemplateResponse("auth/signup.html", {"request": request})


@router.post("/signup")
def create_new_account(
        request: Request,
        username: Annotated[str, Form()],
        email: Annotated[str, Form()],
        password: Annotated[str, Form()],
        confirm_password: Annotated[str, Form()],
):
    resp_args = {
        "request": request,
    }
    if is_user_exists(email):
        resp_args["error_message"] = "User already exists."
    if password != confirm_password:
        resp_args["error_message"] = "Passwords do not match."

    if "error_message" not in resp_args:
        create_new_user({
            "username": username,
            "email": email,
            "password": password,
        })
        resp_args["success_message"] = "User created successfully."
    return templates.TemplateResponse("auth/signup.html", resp_args)


@router.get("/signin")
def sign_in_template(request: Request):
    return templates.TemplateResponse("auth/signin.html", {"request": request})


@router.post("/signin")
def login_user(
        request: Request,
        email: Annotated[str, Form()],
        password: Annotated[str, Form()]
):
    user = get_user_by_email(email)
    if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        cookie = JWTSecurity.create_token(user.id)
        response = RedirectResponse("/toolbox", 303)
        response.set_cookie(key="session", value=cookie)
        return response

    return templates.TemplateResponse(
        "auth/signin.html",
        {"request": request, "error_message": "Invalid credentials."}
    )


@router.get("/signout")
def logout_user(request: Request):
    response = RedirectResponse("/auth/signin", 303)
    response.delete_cookie("session")
    return response
