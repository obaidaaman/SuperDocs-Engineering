from fastapi import Request, HTTPException, status, Depends
import jwt

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database import AsyncSessionLocal
from src.models.db_models import User
from src.auth.controller.auth_controller import ALGORITHM, SECRET_KEY

# Ye wohi dependency hai jo humne routes me banayi thi. Isko yahan rakh diya taaki poori app isko share kar sake.
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)) -> User:
    """
    Ye function Access Token ko cookie se nikal kar verify karega.
    Aur agar valid hua, toh database se User object return karega.
    """
    
    # 1. Pehle Cookie se token check karo
    token = request.cookies.get("access_token")
    
    # 2. (Optional) Agar mobile app/Postman use ho raha hai, toh Header me bhi check karlo fallback ke liye
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please log in.",
        )
        
    try:
        # 3. Token Decode karo
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        if payload.get("type") != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
            
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
            
        user_id = int(user_id_str)
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token expired. Please refresh token.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")
        
    # 4. Database me check karo user exist karta hai ya nahi
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User no longer exists.")
        
    return user
