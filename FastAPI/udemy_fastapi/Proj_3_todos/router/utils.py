from jose import JWTError, jwt
from typing import Annotated
from fastapi import Depends, HTTPException
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone

# SECRET_KEY = "4f3520850838432ee21a82626122b8a47cbb0c0ae4eb24bb62c24e85f31b6b3a"
SECRET_KEY = "2d601a9b6765f100af22ea6e7f87b63dff2927bac744b888c909fb4fd1e67e87034ebf4513ea3938e5587a20a868cb873da125f92858dc408be9f4d21c2f6a614276371a27ade02d9ea774bbf0448aa1aeab7c93477ecbd9db2c33166f028b6ea7dd661df38ed46d571570265e907a88f746240df4d008574284a398aa5e256d1636187aed876575238eb17dca259b7b3722bd5e107dfb0655392e49d9557efe99764d11ae0689117ae71388c5891b95e344e499c2a5d5da2e9f3fe3afd0bdc6d3874a8aa58a771e1f590ee6ad26cf4e889f221a6dadd5f562dd6ffd4860fca6b95625c956ba09f72b105974587ba7396165f13c66a549559caa394a0fb50425"
ALGORITHIM = "HS256"

jwt_validate = OAuth2PasswordBearer(tokenUrl='/auth/token')
def generate_token(username: str, user_id: int, role: str, time_expire: timedelta):

    encode_dict = {
        "sub": username,
        "id": user_id,
        "user_role": role,
        "exp": datetime.now(timezone.utc) + time_expire
    }
    return jwt.encode(encode_dict, SECRET_KEY, algorithm=ALGORITHIM)

async def validate_token(token: Annotated[str, Depends(jwt_validate)]):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHIM])
        print(payload)
        username = payload.get("sub")
        user_id = payload.get("id")
        user_role = payload.get("user_role")
        if not user_id or not username:
            print("Yaha se aaya")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
        return {
            "username": username,
            "id": user_id,
            "role": user_role
        }
    except JWTError as e:
            print(token)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Token Error {e}")

token_validate = Annotated[str, Depends(validate_token)]