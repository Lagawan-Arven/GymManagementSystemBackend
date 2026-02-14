from __future__ import annotations
from pydantic import BaseModel

class SignupPayload(BaseModel):
    name: str
    age: int
    sex: str
    email: str
    password: str

class SigninPayload(BaseModel):
    email: str
    password: str