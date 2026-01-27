from fastapi import APIRouter
from models import usersModel

router = APIRouter()

model = usersModel.UsersModel

# remove group member
@router.put("/group/delete_member{group_name, username, token}" , tags=["group"])
async def delete_group_member(group_name: model.group_name, username: model.name, token: model.token):
    return {"group": group_name}