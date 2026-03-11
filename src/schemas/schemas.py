from __future__ import annotations
from pydantic import BaseModel

class AdminLoginPayload(BaseModel):
    username: str
    password: str