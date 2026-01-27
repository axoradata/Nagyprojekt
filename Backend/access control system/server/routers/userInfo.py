from fastapi import APIRouter
from models import usersModel

router = APIRouter()

model = usersModel.UsersModel

# get user information souch as working hour & group info etc...
@router.get("/user/info{username, token}" , tags=["user"])
async def user_info(username: model.name, token: model.token):
    return {"username": username}