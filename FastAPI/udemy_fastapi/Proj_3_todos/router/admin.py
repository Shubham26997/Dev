from fastapi import APIRouter, HTTPException
from models import Users
from database import SessionDep, bcrypt_context
from starlette import status
from sqlmodel import select
import sys
import os
sys.path.append(os.path.join(os.getcwd() + "/router"))
from utils import token_validate

router = APIRouter()

@router.get("/get_user_details/", status_code=status.HTTP_200_OK)
async def get_user_details(user: token_validate, db: SessionDep):
    if not user or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,\
                            detail="Authentication Error")
    user_data = db.exec(select(Users).where(Users.id == user.get('id'))).fetchall()
    if user_data:
        print(user_data)
        return user_data
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="No records found in the db")

@router.put("/update_password/", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_password(user:token_validate, db:SessionDep, old_password: str, new_password: str):
    if not user or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,\
                            detail="Authentication Error")
    
    user_data = db.exec(select(Users).where(Users.id == user.get('id'))).first()
    if user_data:
        if not bcrypt_context.verify(old_password, user_data.password):
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, \
                            detail="Password is invalid")
        user_data.password = bcrypt_context.hash(new_password)
        db.commit()
        return {"detail": "Password updated successfully"}  # 204 has no content body
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="No records found in the db")