# backend/auth/routes.py

from fastapi import APIRouter, HTTPException
from auth.schemas import RegisterSchema, LoginSchema, ResetSchema
from auth.service import register_user, authenticate_user, reset_password

router = APIRouter(tags=["Auth"])


@router.post("/register")
def register(data: RegisterSchema):
    try:
        register_user(data.name, data.email, data.password)
        return {"message": "User registered successfully!"}

    except Exception:
        raise HTTPException(400, "Email already registered!")


@router.post("/login")
def login(data: LoginSchema):
    token = authenticate_user(data.email, data.password)

    if not token:
        raise HTTPException(401, "Invalid credentials!")

    return {"token": token}


@router.post("/reset-password")
def reset(data: ResetSchema):
    ok = reset_password(data.email, data.new_password)

    if not ok:
        raise HTTPException(404, "User not found!")

    return {"message": "Password updated successfully!"}
