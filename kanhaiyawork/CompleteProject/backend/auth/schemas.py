# backend/auth/schemas.py

from pydantic import BaseModel, EmailStr

class RegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class ResetSchema(BaseModel):
    email: EmailStr
    new_password: str
