from fastapi import APIRouter
from models import usersModel

router = APIRouter()

model = usersModel.UsersModel

# add new member to group
@router.put("/group/add_member{group_name, username, token}" , tags=["group"])
async def add_group_member(group_name: model.group_name, username: model.name, token: model.token):
    return {"group": group_name}