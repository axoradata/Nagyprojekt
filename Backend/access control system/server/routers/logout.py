from fastapi import APIRouter
from models import usersModel

router = APIRouter()

model = usersModel.UsersModel

# logout user
@router.post("/user/logout" , tags=["user"])
async def logout(username: str):
    from database import query
    query.insert_into(f"UPDATE users SET token = NULL WHERE name = '{username}'")
    return {"status": 1, "username": username}