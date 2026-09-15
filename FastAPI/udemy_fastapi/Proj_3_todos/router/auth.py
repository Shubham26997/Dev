from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from starlette import status
from models import Users
from database import SessionDep, bcrypt_context
from datetime import timedelta
import sys
import os
sys.path.append(os.path.join(os.getcwd() + "/router"))
from utils import generate_token

router = APIRouter()

@router.post("/create_user/", status_code=status.HTTP_201_CREATED)
async def create_user(user_req: Users, db: SessionDep):
    new_user = Users(**user_req.model_dump())
    new_user.password = bcrypt_context.hash(new_user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/get_all_users/", status_code=status.HTTP_200_OK)
async def get_users(db: SessionDep):

    all_users = db.exec(select(Users)).all()
    return all_users if all_users else HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.delete("/user/", status_code=status.HTTP_204_NO_CONTENT)
async def user_delete(db: SessionDep, user_id: int = Query(ge = 1)):

    user_rec = db.exec(select(Users).where(Users.id == user_id)).first()
    if user_rec:
        db.delete(user_rec)
        db.commit()
        return "USER Deleted"
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")

@router.post("/token/", status_code=status.HTTP_200_OK)
async def login_user_access(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                            db: SessionDep):
    user_username = db.exec(select(Users).where(Users.username == form_data.username)).first()
    if not user_username:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, \
                            detail="Username is invalid")
    if not bcrypt_context.verify(form_data.password, user_username.password):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, \
                            detail="Password is invalid")
    return {'access_token': generate_token(form_data.username, user_username.id, user_username.role, time_expire = timedelta(minutes=20))
            ,'token_type': 'bearer'}
            