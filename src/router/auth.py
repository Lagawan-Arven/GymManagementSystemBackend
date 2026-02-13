from fastapi import APIRouter

import logging

logger = logging.getLogger(__name__)

router = APIRouter()

sample_users = [{"name":"arven","email":"sample@email.com","password":"1234"}]

#SIGNUP USER
@router.post("/signup")
def signup_User():
    return

#SIGNIN USER
@router.post("/signin")
def signin_user(email: str, password: str):
    for user in sample_users:
        if email == user["email"] and password == user['password']:
            return user['name']

    return 'User does not exit'